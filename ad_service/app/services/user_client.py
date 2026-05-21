import logging

import httpx
from fastapi import HTTPException, status

from app.core.config import settings

logger = logging.getLogger(__name__)


class UserServiceClient:
    """REST client for cross-service user validation via user_service."""

    def __init__(self) -> None:
        base = settings.USER_SERVICE_BASE_URL.rstrip("/")
        self._user_url_template = f"{base}{settings.API_V1_STR}/users/{{user_id}}"

    async def ensure_user_exists(self, user_id: int) -> None:
        url = self._user_url_template.format(user_id=user_id)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=5.0)
        except httpx.ConnectError as exc:
            logger.error("User service unavailable (user_id=%s): %s", user_id, exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User service is temporarily unavailable (fault tolerance simulation)",
            ) from exc
        except httpx.HTTPError as exc:
            logger.error("User service HTTP error (user_id=%s): %s", user_id, exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User service is temporarily unavailable (fault tolerance simulation)",
            ) from exc

        if response.status_code == status.HTTP_404_NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User does not exist",
            )
        if response.status_code != status.HTTP_200_OK:
            logger.warning(
                "Unexpected user service status %s for user_id=%s",
                response.status_code,
                user_id,
            )
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="User service is temporarily unavailable (fault tolerance simulation)",
            )


user_service_client = UserServiceClient()
