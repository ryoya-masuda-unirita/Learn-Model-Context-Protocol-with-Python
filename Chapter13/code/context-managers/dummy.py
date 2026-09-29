"""MCP のクライアントのコードを、ダミーのクラスで動かしてみるサンプル。

非同期のコンテキストマネージャー（async with）の仕組みを確認するのに使う。
"""
from types import TracebackType
from typing import Any

class DummyStream:
    """読み書きのストリームのダミー。"""

    async def read(self) -> None:
        """何もしない。"""
        pass
    async def write(self, data: Any) -> None:
        """何もしない。

        Parameters
        ----------
        data : Any
            書き込むデータ（使わない）。
        """
        pass

class DummyClientSession:
    """async with で使う、MCP の ClientSession のダミー。"""

    def __init__(self, read_stream: DummyStream, write_stream: DummyStream) -> None:
        """ストリームを受け取ってセッションを作る。

        Parameters
        ----------
        read_stream : DummyStream
            読み込み用のストリーム。
        write_stream : DummyStream
            書き込み用のストリーム。
        """
        self.read_stream = read_stream
        self.write_stream = write_stream

    async def __aenter__(self) -> "DummyClientSession":
        """セッションを開始する。

        Returns
        -------
        DummyClientSession
            開始したセッション自身。
        """
        print("セッションを開始しました")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        """セッションを閉じる。

        Parameters
        ----------
        exc_type : type[BaseException] | None
            async with ブロック内で発生した例外の型。発生していなければ None。
        exc : BaseException | None
            async with ブロック内で発生した例外。発生していなければ None。
        tb : TracebackType | None
            例外のトレースバック。発生していなければ None。
        """
        print("セッションを閉じました")

    async def initialize(self) -> None:
        """セッションを初期化する。"""
        print("セッションを初期化しています...")

    async def list_tools(self) -> Any:
        """ダミーの tool の一覧を返す。

        Returns
        -------
        Any
            tools 属性に Tool のリストを持つオブジェクト。
        """
        class Tool:
            """tool のダミー。"""

            def __init__(self, name: str) -> None:
                """名前を受け取って tool を作る。

                Parameters
                ----------
                name : str
                    tool の名前。
                """
                self.name = name
        return type("ToolList", (), {"tools": [Tool("ToolA"), Tool("ToolB")]})()

async def streamablehttp_client(url: str) -> tuple[DummyStream, DummyStream, None]:
    """MCP SDK の streamablehttp_client のダミー。

    Parameters
    ----------
    url : str
        接続先の URL。

    Returns
    -------
    tuple[DummyStream, DummyStream, None]
        読み込み用と書き込み用のストリーム、およびセッション ID を返す関数の代わりの None。
    """
    print(f"{url} に接続しています")
    return DummyStream(), DummyStream(), None

# メインの非同期関数
async def main() -> None:
    """ダミーのクライアントで、MCP のクライアントの流れ（接続、初期化、tool の一覧取得）を再現する。"""
    read_stream, write_stream, _ = await streamablehttp_client("http://localhost:8000/mcp")
    async with DummyClientSession(read_stream, write_stream) as session:
        await session.initialize()
        tools = await session.list_tools()
        print(f"使える tool: {[tool.name for tool in tools.tools]}")

# 非同期関数を実行する
import asyncio
asyncio.run(main())
