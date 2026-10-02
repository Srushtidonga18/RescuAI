import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Float, Integer, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from RescuAI.backend.app.core.database import Base


class InputType(str, enum.Enum):
    TEXT = "TEXT"
    AUDIO = "AUDIO"
    IMAGE = "IMAGE"


class UrgencyLevel(str, enum.Enum):
    CRITICAL = "CRITICAL"
    MODERATE = "MODERATE"
    LOW = "LOW"


class SOSCategory(str, enum.Enum):
    MEDICAL = "MEDICAL"
    TRAPPED = "TRAPPED"
    FOOD_WATER = "FOOD_WATER"
    INFANT_ELDERLY = "INFANT_ELDERLY"
    GENERAL = "GENERAL"


class SOSStatus(str, enum.Enum):
    PENDING = "PENDING"
    DISPATCHED = "DISPATCHED"
    RESCUED = "RESCUED"


class SOSRequest(Base):
    __tablename__ = "sos_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    input_type = Column(SQLEnum(InputType), nullable=False, default=InputType.TEXT)
    raw_text = Column(Text, nullable=True)
    audio_file_path = Column(String(500), nullable=True)
    image_file_path = Column(String(500), nullable=True)
    transcribed_text = Column(Text, nullable=True)
    urgency_level = Column(SQLEnum(UrgencyLevel), nullable=False, default=UrgencyLevel.MODERATE)
    category = Column(SQLEnum(SOSCategory), nullable=False, default=SOSCategory.GENERAL)
    extracted_location = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    trapped_count = Column(Integer, default=1)
    medical_details = Column(Text, nullable=True)
    action_summary = Column(Text, nullable=True)
    is_spam_or_fake = Column(Boolean, default=False)
    cluster_id = Column(String(36), nullable=True, index=True)
    status = Column(SQLEnum(SOSStatus), nullable=False, default=SOSStatus.PENDING)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    dispatch_card = relationship("DispatchCard", back_populates="sos_request", uselist=False, cascade="all, delete-orphan")


class DispatchCard(Base):
    __tablename__ = "dispatch_cards"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    sos_id = Column(String(36), ForeignKey("sos_requests.id", ondelete="CASCADE"), nullable=False, unique=True)
    assigned_team = Column(String(255), default="Unassigned")
    supplies_needed = Column(Text, nullable=True)  # JSON formatted array or text string
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    sos_request = relationship("SOSRequest", back_populates="dispatch_card")
