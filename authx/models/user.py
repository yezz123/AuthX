from datetime import datetime, timedelta
from string import ascii_letters
from typing import List, Optional, Union

from pydantic import BaseModel, EmailStr, validator

from authx.core.config import (
    PASSWORD_CHARS,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    TIME_DELTA,
    USERNAME_CHARS,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    WRONG_USERNAMES,
)
from authx.models.common import DefaultModel, set_created_at, set_last_login


def check_username(v: str) -> str:
    v = v.strip()
    if len(v) < USERNAME_MIN_LENGTH or len(v) > USERNAME_MAX_LENGTH:
        raise ValueError("username length")
    for letter in v:
        if letter not in USERNAME_CHARS:
            raise ValueError("username special characters")
    if v in WRONG_USERNAMES:
        raise ValueError("username wrong")
    if any(letter not in ascii_letters for letter in v):
        raise ValueError("username different letters")
    return v


def check_password(v: str, values) -> str:
    if " " in v:
        raise ValueError("password space")
    if len(v) < PASSWORD_MIN_LENGTH or len(v) > PASSWORD_MAX_LENGTH:
        raise ValueError("password length")
    if v != values.get("password1"):
        raise ValueError("password mismatch")
    for letter in v:
        if letter not in PASSWORD_CHARS:
            raise ValueError("password special")
    return v


class UserInRegister(BaseModel):
    """Class to check the user in the register"""

    email: EmailStr
    username: str
    password1: str
    password2: str

    _check_username = validator("username", allow_reuse=True)(check_username)

    _check_password2 = validator("password2", allow_reuse=True)(check_password)


class UserInCreate(BaseModel):
    """Class to check the user in the create."""

    email: EmailStr
    username: str
    password: str
    active: bool = True
    confirmed: bool = False
    permissions: List[str] = []
    info: list = []
    created_at: Optional[datetime] = None
    last_login: Optional[datetime] = None

    _created_at = validator("created_at", pre=True, always=True, allow_reuse=True)(
        set_created_at
    )
    _last_login = validator("last_login", pre=True, always=True, allow_reuse=True)(
        set_last_login
    )


class UserInLogin(BaseModel):
    """Class to check the user in the login."""

    login: Union[EmailStr, str]
    password: str


class UserInForgotPassword(BaseModel):
    """Class to check the user in the forgot password."""

    email: EmailStr


class UserPayload(BaseModel):
    """Class to check the user payload."""

    id: int
    username: str
    permissions: List[str] = []


class UserInSetPassword(DefaultModel):
    """Class to check the user in the set password."""

    password1: str
    password2: str

    _check_password = validator("password2", allow_reuse=True)(check_password)


class UserInChangePassword(UserInSetPassword):
    """Class to check the user in the change password."""

    old_password: str

    @validator("old_password")
    def check_old_password(cls, v, values):
        if v == values.get("password1"):
            raise ValueError("password same")
        return v


class UserInChangeUsername(DefaultModel):
    """Class to check the user in the change username."""

    username: str

    _check_username = validator("username", allow_reuse=True)(check_username)


class UserPrivateInfo(DefaultModel):
    """Class to check the user private info."""

    id: int
    username: str
    email: str
    active: bool
    sid: Optional[str] = None
    provider: Optional[str] = None
    confirmed: bool
    created_at: datetime
    last_login: datetime

    @validator("created_at", "last_login")
    def set_format(cls, v):
        d = v + timedelta(hours=TIME_DELTA)
        return d.strftime("%-d %B %Y, %H:%M")
