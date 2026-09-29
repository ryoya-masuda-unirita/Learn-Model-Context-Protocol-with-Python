"""サーバーで公開する tool の一覧。tool 名をキーにした辞書として提供する。"""
from typing import Any

from .add import tool_add

tools: dict[str, dict[str, Any]] = {
  tool_add["name"] : tool_add
}
