# client.py
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession
import asyncio
import mcp.types as types
from mcp.shared.session import RequestResponder
import requests
import logging
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("TOKEN")
if not token:
    print(".env ファイルに TOKEN が見つかりません。util.py を実行して生成してください。")
    raise ValueError(".env ファイルに TOKEN が見つかりません")

# ログを設定する
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('mcp_client')

class LoggingCollector:
    def __init__(self):
        self.log_messages: list[types.LoggingMessageNotificationParams] = []
    async def __call__(self, params: types.LoggingMessageNotificationParams) -> None:
        self.log_messages.append(params)
        logger.info("MCP ログ: %s - %s", params.level, params.data)

logging_collector = LoggingCollector()
port = 8000

async def message_handler(
    message: RequestResponder[types.ServerRequest, types.ClientResult]
    | types.ServerNotification
    | Exception,
) -> None:
    logger.info("メッセージを受信: %s", message)
    if isinstance(message, Exception):
        logger.error("例外を受信しました！")
        raise message
    elif isinstance(message, types.ServerNotification):
        logger.info("通知: %s", message)
    elif isinstance(message, RequestResponder):
        logger.info("リクエストへの応答: %s", message)
    else:
        logger.info("サーバーからのメッセージ: %s", message)

async def main():
    logger.info("クライアントを起動しています...")
    async with streamablehttp_client(
        url = f"http://localhost:{port}/mcp",
        headers = {"Authorization": f"Bearer {token}"}
    ) as (
        read_stream,
        write_stream,
        session_callback,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
            logging_callback=logging_collector,
            message_handler=message_handler
        ) as session:
            id_before = session_callback()
            logger.info("初期化前のセッション ID: %s", id_before)
            await session.initialize()
            id_after = session_callback()
            logger.info("初期化後のセッション ID: %s", id_after)
            logger.info("セッションを初期化しました。tool を呼び出せます。")
            tool_result = await session.call_tool("get_time", {})
            logger.info("tool の結果: %s", tool_result)
            if logging_collector.log_messages:
                logger.info("収集したログメッセージ:")
                for log in logging_collector.log_messages:
                    logger.info("ログ: %s", log)

def stream_progress(message="こんにちは", url="http://localhost:8000/stream"):
    params = {"message": message}
    logger.info("%s に接続しています（メッセージ: %s）", url, message)
    try:
        with requests.get(url, params=params, stream=True, timeout=10) as r:
            r.raise_for_status()
            logger.info("--- ストリーミングの進捗 ---")
            for line in r.iter_lines():
                if line:
                    # 見やすさのため、ストリームの内容を stdout にも表示する
                    decoded_line = line.decode().strip()
                    print(decoded_line)
                    logger.debug("ストリームの内容: %s", decoded_line)
            logger.info("--- ストリーム終了 ---")
    except requests.RequestException as e:
        logger.error("ストリーミング中にエラーが発生しました: %s", e)

if __name__ == "__main__":
    import sys

    logger.info("MCP クライアントを実行しています...")
    asyncio.run(main())

        
    # デフォルトでは両方を実行しない。どちらのモードにするかはユーザーに選ばせる