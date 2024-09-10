from fastapi import Request, HTTPException, Depends
from fastapi.security import APIKeyHeader
from typing import Optional
from app.utils.yaml_loader import load_config

# Load configuration
config = load_config('app/config/config.yml')
STATIC_TOKEN = config['auth']['token']

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

def validate_token(api_key: Optional[str] = Depends(api_key_header)):
    # The token should start with 'Bearer ' if you are using a Bearer token scheme.
    if api_key is None or not api_key.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = api_key[len("Bearer "):]  # Extract the actual token after 'Bearer '
    
    if token != STATIC_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return api_key