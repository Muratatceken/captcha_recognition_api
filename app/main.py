from fastapi import FastAPI
from app.routes import captcha_routes

app = FastAPI(
    title="Captcha Recognition API",
    description="An API for recognizing text in captcha images using a pretrained TrOCR model.",
    version="1.0.0"
)

app.include_router(captcha_routes.router)
