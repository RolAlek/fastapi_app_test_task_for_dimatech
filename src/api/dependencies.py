from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import AuthSettings, get_settings
from src.infrastructure.database.dependencies import create_session_dependency
from src.infrastructure.database.models.user import User
from src.repositories.token import _TokenRepository

http_bearer = HTTPBearer(auto_error=False)


async def current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    session: AsyncSession = Depends(create_session_dependency),
):
    settings: AuthSettings = get_settings(AuthSettings)
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token is required.",
        )

    token_data = credentials.credentials
    token_repo = _TokenRepository(session)

    token = await token_repo.get_by_attr("token", token_data)

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
        )

    try:
        payload = jwt.decode(
            token=token.token,
            key=settings.secret_key,
            algorithms=[settings.algorithm],
        )

    except ExpiredSignatureError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
        ) from exception

    except JWTError as exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
        ) from exception

    expire = payload.get("exp")
    user_id = int(payload.get("sub"))

    if (user_id is None or user_id != token.user_id) or expire is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid access token.",
        )

    return token.user


def current_superuser(user: User = Depends(current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied.",
        )

    return user
