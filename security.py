from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from config import settings
from loguru import logger

API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == settings.API_SECRET_KEY:
        return api_key_header
    
    logger.warning(f"Unauthorized API request attempt! Invalid or missing API KEY: {api_key_header}")
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, 
        detail="غير مصرح لك بالوصول: مفتاح الـ API غير صحيح أو مفقود"
    )
