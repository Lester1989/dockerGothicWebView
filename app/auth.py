import os

from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader


api_key_header = APIKeyHeader(name="access_token", auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == os.environ.get("API_KEY", "ABC"):
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )

async def get_bot_key(api_key: str = Security(api_key_header)):
    if api_key == os.environ.get("SECRET_KEY", "XYZ"):
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
        )
