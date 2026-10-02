import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from RescuAI.backend.app.core.config import settings
from RescuAI.backend.app.core.database import engine, Base, SessionLocal
from RescuAI.backend.app.core.security import get_password_hash
from RescuAI.backend.app.models.user import User, UserRole
from RescuAI.backend.app.models.inventory import ResourceItem, Volunteer
from RescuAI.backend.app.api.api import api_router

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("rescuai.main")

# Create Database Tables automatically on startup
Base.metadata.create_all(bind=engine)

# Rate Limiter setup
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="RescuAI - Multimodal Generative AI Emergency SOS Aggregator & Disaster Triage System"
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Robust CORS Middleware Configuration (Allows localhost:5173, 127.0.0.1:5173, etc.)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
def seed_default_responder():
    """Seeds a default responder user for easy out-of-the-box testing."""
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == "responder@rescuai.org").first()
        if not existing_user:
            default_user = User(
                email="responder@rescuai.org",
                hashed_password=get_password_hash("admin123"),
                full_name="Default Emergency Responder",
                role=UserRole.RESPONDER,
                is_active=True
            )
            db.add(default_user)
            db.commit()
            logger.info("Default responder created: responder@rescuai.org / admin123")
    except Exception as e:
        logger.error(f"Error seeding default user: {e}")
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "status": "operational",
        "docs_url": "/docs",
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
