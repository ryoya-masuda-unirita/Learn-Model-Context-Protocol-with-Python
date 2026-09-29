"""MCP サーバーを SDK を使わずに作るためのメモ（未実装）。"""
# 独自のサーバーを作る必要がある

# POST /MCP を処理すべき。具体的には
#  initialize を処理して capabilities を返す
#  次のメッセージとして initialized を受け取る想定
#  その後で tools/list を処理する
# さらに処理すべきもの：