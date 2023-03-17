from .password_encryption import PasswordEncryption


""" アプリケーションユーザーオブジェクトの定義
- emailサーバーの認証に必要なユーザー情報を持つ
"""


class ApplicationEmailUser:
    def __init__(self, username: str, password: PasswordEncryption) -> None:
        self._username = username
        self._password = password

    @property
    def username(self) -> str: return self._username

    @property
    def password(self) -> str: return self._password

    def encrypt_password(self):
        return self._password.hash_password()






