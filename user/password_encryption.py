import hashlib
import os

"""
パスワードの暗号化を行う

- ハッシュ関数の値オブジェクトを定義
- パスワードの暗号化による手続き
"""


class HashName:
    ALLOWED_VALUES = {"256", "384", "512"}

    def __init__(self, value: str) -> None:
        if value not in self.ALLOWED_VALUES:
            raise ValueError(f"Invalid hash name: {value}")

        self._value = value

    @property
    def value(self): return self._value


class PasswordEncryption:
    def __init__(self, password: str, hash_name: HashName = HashName("256"), char_code='utf-8') -> None:
        self._password = password
        self._hash_name = hash_name
        self._char_code = char_code

    def hash_password(self):
        encode_password = self._hash_name.value.encode(self._char_code)

        if self._hash_name.value == "256":
            return hashlib.sha256(encode_password).hexdigest()

        elif self._hash_name.value == "384":
            return hashlib.sha384(encode_password).hexdigest()

        elif self._hash_name.value == "512":
            return hashlib.sha512(encode_password).hexdigest()

        else:
            raise ValueError(f'文字コードが正しく指定されていません: value={self._hash_name}')


