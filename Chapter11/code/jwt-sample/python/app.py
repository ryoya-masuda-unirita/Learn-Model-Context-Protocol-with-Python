"""PyJWT で JWT を作成し、検証するサンプル。"""
# pip install PyJWT

# トークンを作る
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import datetime
from typing import Any

# JWT の署名に使う秘密鍵
secret_key: str = 'your-secret-key'

header: dict[str, str] = {
    "alg": "HS256",
    "typ": "JWT"
}

# ユーザー情報と、その claim と有効期限
payload: dict[str, Any] = {
    "sub": "1234567890",               # サブジェクト（ユーザー ID）
    "name": "User Userson",                # カスタム claim
    "admin": True,                     # カスタム claim
    "iat": datetime.datetime.utcnow(),# 発行日時
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 有効期限
}

# エンコードする
encoded_jwt: str = jwt.encode(payload, secret_key, algorithm="HS256", headers=header)

print("エンコードした JWT:", encoded_jwt) 

# トークンを検証する
try:
    decoded = jwt.decode(encoded_jwt, secret_key, algorithms=["HS256"])
    print("✅ トークンは有効です。")
    print("デコードした claim:")
    for key, value in decoded.items():
        print(f"  {key}: {value}")
except ExpiredSignatureError:
    print("❌ トークンの有効期限が切れています。")
except InvalidTokenError as e:
    print(f"❌ トークンが無効です: {e}")

