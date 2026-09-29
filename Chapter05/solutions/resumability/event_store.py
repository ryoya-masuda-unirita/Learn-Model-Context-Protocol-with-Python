"""
resumability の機能を示すためのインメモリのイベントストア。

サンプルやテスト向けのシンプルな実装であり、本番環境向けではない。
本番環境では永続化ストレージを使う方が適切。
"""

import logging
from collections import deque
from dataclasses import dataclass
from uuid import uuid4

from mcp.server.streamable_http import EventCallback, EventId, EventMessage, EventStore, StreamId
from mcp.types import JSONRPCMessage

logger: logging.Logger = logging.getLogger(__name__)


@dataclass
class EventEntry:
    """
    イベントストア内の1件のイベントを表す。

    Attributes
    ----------
    event_id : EventId
        イベントの一意な ID。
    stream_id : StreamId
        イベントが属するストリームの ID。
    message : JSONRPCMessage
        イベントとして送った JSON-RPC メッセージ。
    """

    event_id: EventId
    stream_id: StreamId
    message: JSONRPCMessage


class InMemoryEventStore(EventStore):
    """
    EventStore インターフェースの、resumability のためのシンプルなインメモリ実装。

    主にサンプルやテスト向けであり、本番環境向けではない。
    本番環境では永続化ストレージを使う方が適切。

    メモリを節約するため、ストリームごとに直近 N 件のイベントだけを保持する。

    Attributes
    ----------
    max_events_per_stream : int
        ストリームごとに保持するイベントの最大数。
    streams : dict[StreamId, deque[EventEntry]]
        ストリーム ID ごとのイベントの deque。
    event_index : dict[EventId, EventEntry]
        イベント ID からイベントを素早く引くための索引。
    """

    def __init__(self, max_events_per_stream: int = 100) -> None:
        """イベントストアを初期化する。

        Parameters
        ----------
        max_events_per_stream : int, optional
            ストリームごとに保持するイベントの最大数。デフォルトは 100。
        """
        self.max_events_per_stream = max_events_per_stream
        # ストリームごとに直近 N 件のイベントを保持する
        self.streams: dict[StreamId, deque[EventEntry]] = {}
        # event_id -> EventEntry（素早く検索するため）
        self.event_index: dict[EventId, EventEntry] = {}

    async def store_event(self, stream_id: StreamId, message: JSONRPCMessage) -> EventId:
        """生成したイベント ID と一緒にイベントを保存する。

        Parameters
        ----------
        stream_id : StreamId
            イベントを保存するストリームの ID。
        message : JSONRPCMessage
            保存する JSON-RPC メッセージ。

        Returns
        -------
        EventId
            生成したイベント ID。
        """
        event_id = str(uuid4())
        event_entry = EventEntry(event_id=event_id, stream_id=stream_id, message=message)

        # このストリーム用の deque を取得する（なければ作る）
        if stream_id not in self.streams:
            self.streams[stream_id] = deque(maxlen=self.max_events_per_stream)

        # deque がいっぱいなら、一番古いイベントは自動的に削除される
        # そのため event_index からも削除する必要がある
        if len(self.streams[stream_id]) == self.max_events_per_stream:
            oldest_event = self.streams[stream_id][0]
            self.event_index.pop(oldest_event.event_id, None)

        # 新しいイベントを追加する
        self.streams[stream_id].append(event_entry)
        self.event_index[event_id] = event_entry

        return event_id

    async def replay_events_after(
        self,
        last_event_id: EventId,
        send_callback: EventCallback,
    ) -> StreamId | None:
        """指定したイベント ID より後に発生したイベントを再生する。

        Parameters
        ----------
        last_event_id : EventId
            クライアントが最後に受け取ったイベントの ID。
        send_callback : EventCallback
            再生する各イベントを送るためのコールバック。

        Returns
        -------
        StreamId | None
            イベントを再生したストリームの ID。last_event_id が見つからなければ None。
        """
        if last_event_id not in self.event_index:
            logger.warning(f"イベント ID {last_event_id} がストアに見つかりません")
            return None

        # ストリームを取得し、最後に受け取ったイベントより後のイベントを探す
        last_event = self.event_index[last_event_id]
        stream_id = last_event.stream_id
        stream_events = self.streams.get(last_event.stream_id, deque())

        # deque 内のイベントはすでに時系列順に並んでいる
        found_last = False
        for event in stream_events:
            if found_last:
                await send_callback(EventMessage(event.message, event.event_id))
            elif event.event_id == last_event_id:
                found_last = True

        return stream_id