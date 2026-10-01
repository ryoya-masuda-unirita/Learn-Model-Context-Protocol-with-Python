"""OAuth 2.1 の認可コードフローをシミュレートする認可サーバー（Flask）。

/authorize、/token、/introspect、/logout を提供する。`python auth-server.py` でポート 5050 で起動する。
"""
from typing import Any

from flask import Flask, Response, request, redirect, jsonify
from werkzeug.wrappers import Response as WerkzeugResponse
import uuid
import requests

app: Flask = Flask(__name__)

# インメモリのストア
# サーバーを再起動すると、発行した認可コードやアクセストークンはすべて無効になる
auth_codes: dict[str, dict[str, Any]] = {}
access_tokens: dict[str, dict[str, str]] = {}


@app.route("/introspect", methods=["POST"])
def introspect() -> Response:
    """トークンが有効かを調べ、その情報を返す（トークン introspection）。

    Returns
    -------
    Response
        トークンが有効なら active=True とユーザー情報、無効なら active=False の JSON。
    """
    # リソースサーバーは、受け取ったトークンが本物かを自分では判断できないので、発行した認可サーバーに問い合わせる。
    # （JWT のように署名を自分で検証できるトークンなら、この問い合わせは不要になる）
    token = request.form.get("token")
    # token が送られてこなかった場合は、無効なトークンとして扱う
    token_data = access_tokens.get(token) if token is not None else None

    if not token_data:
        return jsonify({"active": False})

    return jsonify({
        "active": True,
        "scope": "read",
        "username": token_data["user"],
        "client_id": "abc",
        "token_type": "access_token",
        "exp": 9999999999,
        "sub": "user123"
    })


@app.route("/authorize")
def authorize() -> WerkzeugResponse:
    """ログインと同意をシミュレートし、認可コードを付けてリダイレクトする。

    Returns
    -------
    WerkzeugResponse
        redirect_uri に code と state を付けたリダイレクトのレスポンス。
    """
    client_id = request.args.get("client_id")
    redirect_uri = request.args.get("redirect_uri")
    state = request.args.get("state")
    code_challenge = request.args.get("code_challenge")

    # ログインと同意をシミュレートする
    # 本来はここでログイン画面と「このアプリに許可しますか？」の同意画面を出す。
    # 認可コードは、ユーザーのブラウザを経由してクライアントに渡される（だから短命・1回限りにする）
    code = str(uuid.uuid4())
    auth_codes[code] = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "code_challenge": code_challenge
    }

    return redirect(f"{redirect_uri}?code={code}&state={state}")

@app.route("/token", methods=["POST"])
def token() -> Response | tuple[Response, int]:
    """認可コードをアクセストークンと交換する。

    Returns
    -------
    Response | tuple[Response, int]
        成功すればアクセストークンの JSON。認可コードや code_verifier が不正なら、エラーの JSON とステータスコード 400。
    """
    code = request.form.get("code")
    code_verifier = request.form.get("code_verifier")

    if code is None or code not in auth_codes:
        return jsonify({"error": "invalid_code"}), 400

    # 認可コードは1回しか使えない。取り出すと同時にストアから消すことで、盗まれたコードを使い回されないようにする
    auth_code = auth_codes.pop(code)

    # 簡略化した PKCE のチェック
    # PKCE は、認可コードを盗んだ第三者がトークンと交換できないようにする仕組み。最初に code_challenge を送った本人しか
    # 元の code_verifier を知らない。OAuth 2.1 では code_verifier を SHA-256 にかけた値（S256）と比べるが、
    # ここでは簡略化のため、そのまま（plain）比べている
    if auth_code["code_challenge"] != code_verifier:
        return jsonify({"error": "invalid_code_verifier"}), 400

    access_token = str(uuid.uuid4())
    access_tokens[access_token] = {"user": "chris"}

    return jsonify({
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600
    })

@app.route("/logout")
def logout() -> tuple[str, int]:
    """ログアウトをシミュレートする。

    Returns
    -------
    tuple[str, int]
        ログアウトしたことを伝えるメッセージと、ステータスコード 200。
    """
    return "ログアウトしました（シミュレーション）", 200

if __name__ == "__main__":
    PORT = 5050
    print(f"認可サーバーをポート {PORT} で起動しました")
    app.run(port=PORT)
