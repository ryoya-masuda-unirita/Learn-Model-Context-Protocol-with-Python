"""テスト用の JWT を生成・検証するユーティリティ。

`python util.py` で実行すると、生成したトークンを .env に書き出す。
"""
# pip install PyJWT

# トークンを作る
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import datetime
from typing import Any

# JWT の署名に使う秘密鍵
secret_key: str = 'your-secret-key'

def generate_token() -> str:
    """テスト用の JWT を生成する。

    Returns
    -------
    str
        HS256 で署名した、有効期限1時間の JWT。
    """
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    # ユーザー情報と、その claim と有効期限
    payload = {
        "sub": "1234567890",               # サブジェクト（ユーザー ID）
        "name": "User Userson",                # カスタム claim
        "admin": True,                     # カスタム claim
        "iat": datetime.datetime.utcnow(),# 発行日時
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),  # 有効期限
        "scopes": ["Admin.Write", "User.Read"]  # scope（権限）用のカスタム claim
    }

    # エンコードする
    encoded_jwt = jwt.encode(payload, secret_key, algorithm="HS256", headers=header)
    print("エンコードした JWT:", encoded_jwt)
    return encoded_jwt   

def validate_token(token: str) -> dict[str, Any] | None:
    """JWT を検証してデコードする。

    Parameters
    ----------
    token : str
        検証する JWT。

    Returns
    -------
    dict[str, Any] | None
        デコードした claim。有効期限切れや不正なトークンなら None。
    """
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        # print("✅ トークンは有効です。")
        # print("デコードした claim:")
        # for key, value in decoded.items():
        #     print(f"  {key}: {value}")
        return decoded
    except ExpiredSignatureError:
        print("❌ トークンの有効期限が切れています。")
    except InvalidTokenError as e:
        print(f"❌ トークンが無効です: {e}")
    return None

if __name__ == "__main__":
    token = generate_token()
    # .env ファイルに書き出す
    with open(".env", "w") as f:
        f.write(f"TOKEN={token}")
    print(token)
    # validate_token(token)