from typing import Callable

from fastapi import APIRouter, Depends, Request

from authx.backend import UsersRepo
from authx.core.jwt import JWTBackend
from authx.core.user import User
from authx.services import PasswordService


def get_router(
    repo: UsersRepo,
    auth_backend: JWTBackend,
    get_authenticated_user: Callable,
    debug: bool,
    base_url: str,
    site: str,
    recaptcha_secret: str,
    smtp_username: str,
    smtp_password: str,
    smtp_host: str,
    smtp_tls: int,
    display_name: str,
):
    """Setup The Password requirements Router, for handling password related requests, such as resetting passwords,
    changing passwords, etc."""
    PasswordService.setup(
        repo,
        auth_backend,
        debug,
        base_url,
        site,
        recaptcha_secret,
        smtp_username,
        smtp_password,
        smtp_host,
        smtp_tls,
        display_name,
    )

    router = APIRouter()

    @router.post("/forgot_password", name="auth:forgot_password")
    async def forgot_password(*, request: Request):
        data = await request.json()
        ip = request.client.host
        service = PasswordService()
        return await service.forgot_password(data, ip)

    @router.get("/password", name="auth:password_status")
    async def password_status(*, user: User = Depends(get_authenticated_user)):
        service = PasswordService(user)
        return await service.password_status()

    @router.post("/password", name="auth:password_set")
    async def password_set(
        *, request: Request, user: User = Depends(get_authenticated_user)
    ):
        data = await request.json()
        service = PasswordService(user)
        return await service.password_set(data)

    @router.post("/password/{token}", name="auth:password_reset")
    async def password_reset(*, token: str, request: Request):
        data = await request.json()
        service = PasswordService()
        return await service.password_reset(data, token)

    @router.put("/password", name="auth:password_change")
    async def password_change(
        *, request: Request, user: User = Depends(get_authenticated_user)
    ):
        data = await request.json()
        service = PasswordService(user)
        return await service.password_change(data)

    return router
