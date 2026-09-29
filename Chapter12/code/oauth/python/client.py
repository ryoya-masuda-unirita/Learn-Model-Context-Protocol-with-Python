"""OAuth 2.1 の認可コードフローを、認可サーバーとリソースサーバーに対して順に実行するクライアント。"""
import requests
from urllib.parse import urlparse, parse_qs

# 設定
AUTH_SERVER: str = "http://localhost:5050"
RESOURCE_SERVER: str = "http://localhost:5051"
CLIENT_ID: str = "abc"
REDIRECT_URI: str = "http://localhost:3000/callback"
STATE: str = "xyz"
CODE_CHALLENGE: str = "123"
CODE_VERIFIER: str = "123"


# TODO: 1a. 既存のトークンがある場合の処理を追加する
# 有効なトークンを持っていれば /introspect を呼び出すコードを追加する
# 2a. 問題がなければそのまま続ける
# 2b. トークンが無効なら 1b に進む

# 1b. 既存のトークンがないので、/authorize から始める

# ステップ 1: /authorize へのブラウザのリダイレクトをシミュレートする
authorize_url = f"{AUTH_SERVER}/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&state={STATE}&code_challenge={CODE_CHALLENGE}&code_challenge_method=plain"
print(f"認可をリクエストしています: {authorize_url}")
response = requests.get(authorize_url, allow_redirects=False)

# ステップ 2: リダイレクトから認可コードを取り出す
redirect_location = response.headers.get("Location")
if not redirect_location:
    print("認可サーバーがリダイレクトしませんでした。起動していますか？")
    exit(1)

parsed_url = urlparse(redirect_location)
query_params = parse_qs(parsed_url.query)
auth_code = query_params.get("code", [None])[0]
print(f"認可コードを受け取りました: {auth_code}")

# ステップ 3: 認可コードをアクセストークンと交換する
token_response = requests.post(f"{AUTH_SERVER}/token", data={
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "code_verifier": CODE_VERIFIER
})
token_data = token_response.json()
access_token = token_data.get("access_token")
print(f"アクセストークン: {access_token}")

# ステップ 4: リソースサーバーを呼び出す
resource_response = requests.get(f"{RESOURCE_SERVER}/userinfo", headers={
    "Authorization": f"Bearer {access_token}"
})
print("ユーザー情報の応答:")
print(resource_response.json())