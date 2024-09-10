from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from typing import Optional
from app.model.model import TrOCRModel
from app.utils.yaml_loader import load_config
from fastapi.security import HTTPBasicCredentials
from app.security.auth import validate_token
from app.constants.status_codes import STATUS_CODES


router = APIRouter()
config = load_config('app/config/config.yml')
trocr_model = TrOCRModel(config)

@router.post("/recognize", response_model=dict)
async def recognize_captcha(
    file: Optional[UploadFile] = File(None),
    api_key: str = Depends(validate_token)
):
    if file is None:
        return {"status": 1, "details": STATUS_CODES[1]}
    
    if file.content_type not in ['image/png', 'image/jpeg']:
        return {"status": 1, "details": STATUS_CODES[2]}
    
    try:
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        predicted_text = trocr_model.recognize_text(file_path)
        return {"status": 0, "details": {"recognized_text": predicted_text}}
    
    except Exception as e:
        return {"status": 1, "details": STATUS_CODES[4]}