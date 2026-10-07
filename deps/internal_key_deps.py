from fastapi import Header, HTTPException, status

from configs.config import settings


async def require_internal_keys(
        internal_keys: str | None = Header(default=None, alias="X-Internal-Key")
)-> None:
    if internal_keys != settings.INTERNAL_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid interval key"
        )