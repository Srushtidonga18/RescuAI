from fastapi import APIRouter
from RescuAI.backend.app.api.v1 import auth, responder
from RescuAI.backend.app.api.v1 import sos

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(sos.router, prefix="/sos", tags=["Citizen SOS Ingestion"])
api_router.include_router(responder.router, prefix="/responder", tags=["Responder Command Center"])
