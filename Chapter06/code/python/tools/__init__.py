"""サーバーで公開する tool の一覧。tool 名をキーにした辞書として提供する。"""
from typing import Any

from .add import tool_add

# tool 名で引けるように辞書にしておく。tool を増やすときは、ファイルを足してここに1行追加するだけでよい
tools: dict[str, dict[str, Any]] = {
  tool_add["name"] : tool_add
}
