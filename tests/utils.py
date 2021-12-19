from datetime import datetime, timedelta
from typing import Iterable, Optional, Tuple, Union

import jwt

with open("tests/key/private_key", "rb") as f:
    private_key = f.read()

with open("tests/key/public_key", "rb") as f:
    public_key = f.read()

ACCESS_COOKIE_NAME = "access"
REFRESH_COOKIE_NAME = "refresh"


class User:
    """
    Setup a user object with the given id, username and admin status.
    """

    def __init__(self, id: int, username: str, admin: bool):
        self.id = id
        self.username = username
        self.is_admin = admin
        self.data = {"id": id, "username": username}


def mock_get_authenticated_user():
    """
    Mock the get_authenticated_user function to return a user object.

    Returns:
        User: A user object.
    """

    class User:
        def __init__(self):
            """
            Setup a user object with the given id, username and admin status.
            """
            self.id = 2
            self.username = "user"
            self.is_admin = False
            self.data = {"id": self.id, "username": self.username}

    return User()


class MockDatabaseBackend:
    """
    Mock the get_authenticated_user function to return a user object.
    """

    def __init__(self, database_name):
        self._incr = 5
        self._users = [
            {
                "id": 1,
                "email": "admin@gmail.com",
                "username": "admin",
                "password": "12345678",
                "active": True,
                "confirmed": True,
                "permissions": ["admin"],
            },
            {
                "id": 2,
                "email": "user@gmail.com",
                "username": "user",
                "password": "12345678",
                "active": True,
                "confirmed": True,
                "permissions": [],
            },
            {
                "id": 3,
                "email": "anotheruser@gmail.com",
                "username": "anotheruser",
                "password": "12345678",
                "active": True,
                "confirmed": False,
                "permissions": [],
            },
            {
                "id": 4,
                "email": "inactiveuser@gmail.com",
                "username": "inactiveuser",
                "password": "12345678",
                "active": False,
                "confirmed": True,
                "permissions": [],
            },
            {
                "id": 5,
                "email": "socialuser@gmail.com",
                "username": "socialuser",
                "provider": "google",
                "sid": "8888",
                "active": False,
                "confirmed": True,
                "permissions": [],
            },
        ]
        self._email_confirmations = []

    def _increment_id(self) -> int:
        self._incr += 1
        return self._incr

    def _get(self, field: str, value) -> Optional[dict]:
        for item in self._users:
            if item.get(field) == value:
                return item

        return None

    async def get(self, id: int) -> Optional[dict]:
        return self._get("id", id)

    async def get_by_email(self, email: str) -> Optional[dict]:
        return self._get("email", email)

    async def get_by_username(self, username: str) -> Optional[dict]:
        return self._get("username", username)

    async def get_by_social(self, provider: str, sid: str) -> Optional[dict]:
        for item in self._users:
            if item.get("provider") == provider and item.get("sid") == sid:
                return item

        return None

    async def create(self, obj: dict) -> int:
        id = self._increment_id()
        obj["id"] = id
        self._users.append(obj)
        return id

    async def update(self, id: int, obj: dict) -> bool:
        for i, item in enumerate(self._users):
            if item.get("id") == id:
                self._users[i].update(obj)
                return True

        return False

    async def delete(self, id: int) -> bool:
        """
        Delete a user.

        Args:
            id (int): The user id to delete.

        Returns:
            bool: True if the user was deleted, False otherwise.
        """
        for i, item in enumerate(self._users):
            if item.get("id") == id:
                del self._users[i]
                return True

        return False

    async def count(self, query) -> int:
        return 42

    async def request_email_confirmation(self, email: str, token_hash: str) -> None:
        """
        Add a new email confirmation to the list.

        Args:
            email (str): The email address to confirm.
            token_hash (str): The token hash to confirm.

        Returns:
            None
        """
        for i, item in enumerate(self._email_confirmations):
            if item.get("email") == email:
                self._email_confirmations[i].update({"token": token_hash})
                return None
        self._email_confirmations.append({"email": email, "token": token_hash})

    async def confirm_email(self, token_hash: str) -> bool:
        """
        Confirm an email address.

        Args:
            token_hash (str): The token hash to confirm.

        Returns:
            bool: True if the email was confirmed, False otherwise.
        """
        for item in self._email_confirmations:
            if item.get("token") == token_hash:
                user = self._get("email", item.get("email"))
                await self.update(user.get("id"), {"confirmed": True})
                return True
        return False

    async def get_blacklist(self) -> Iterable[dict]:
        """
        Get the blacklist.

        Returns:
            Iterable[dict]: The blacklist.
        """
        return [item for item in self._users if not item.get("active")]

    async def search(self) -> Tuple[dict, int]:
        return self._users, 1


class MockCacheBackend:
    """
    mock the cache backend.
    """

    def __init__(self) -> None:
        self._db = {}

    async def get(self, key: str) -> Optional[str]:
        return self._db.get(key)

    async def delete(self, key: str) -> None:
        try:
            self._db.pop(key)
        except KeyError:
            pass

    async def keys(self, match: str) -> Iterable[str]:
        return {}

    async def set(self, key: str, value: Union[str, bytes, int], expire: int) -> None:
        self._db[key] = value

    async def setnx(self, key: str, value: Union[str, bytes, int], expire: int) -> None:
        v = self._db.get(key)
        if v is None:
            self._db[key] = value

    async def incr(self, key: str) -> str:
        v = self._db.get(key)
        if v is not None:
            self._db[key] = int(v) + 1

    async def dispatch_action(self, channel: str, action: str, payload: str) -> None:
        print("Dispatching action")
        print(action)
        print(payload)


class MockAuthBackend:
    @classmethod
    def create(
        cls,
        jwt_algorithm: str,
        private_key: bytes,
        public_key: bytes,
        access_expiration: int,
        refresh_expiration: int,
    ) -> None:
        pass

    def __init__(
        self,
        jwt_algorithm: str,
        private_key: bytes,
        public_key: bytes,
        access_expiration: int = 60 * 5,
        refresh_expiration: int = 60 * 10,
    ):
        self._jwt_algorithm = jwt_algorithm
        self._private_key = private_key
        self._public_key = public_key
        self._access_expiration = access_expiration
        self._refresh_expiration = refresh_expiration
        self._private_key = private_key
        self._public_key = public_key

    async def decode_token(self, token: str, leeway: int = 0) -> Optional[dict]:
        """
        Decode a JWT token.

        Args:
            token (str): The JWT token to decode.
            leeway (int, optional): The leeway to use when decoding the token. Defaults to 0.

        Returns:
            Optional[dict]: The decoded token.
        """
        if token:
            return jwt.decode(token, key=self._public_key, algorithms="RS256")
        return None

    def _create_token(
        self, payload: dict, token_type: str, expiration_delta: Optional[int] = None
    ) -> str:
        iat = datetime.utcnow()
        if expiration_delta:
            exp = datetime.utcnow() + timedelta(seconds=expiration_delta)
        else:
            exp = datetime.utcnow() + timedelta(seconds=60)

        payload.update({"iat": iat, "exp": exp, "type": token_type})

        token = jwt.encode(payload, self._private_key, algorithm=self._jwt_algorithm)
        if isinstance(token, bytes):
            # For PyJWT <= 1.7.1
            return token.decode("utf-8")
        # For PyJWT >= 2.0.0a1
        return token

    def create_access_token(self, payload: dict) -> str:
        return self._create_token(payload, "access", 60 * 5)

    def create_refresh_token(self, payload: dict) -> str:
        return self._create_token(payload, "refresh", 60 * 10)

    def create_tokens(self, payload: dict) -> dict:
        access = self.create_access_token(payload)
        refresh = self.create_refresh_token(payload)
        return {"access": access, "refresh": refresh}


class MockEmailClient:
    def __init__(self, *args):
        pass

    async def send_confirmation_email(self, *args):
        """
        Send a confirmation email.
        """

    async def send_forgot_password_email(self, *args):
        """
        Send a forgot password email.
        """


def mock_verify_password(password: str, db_password: str) -> bool:
    return password == db_password


def mock_admin_required():
    pass
