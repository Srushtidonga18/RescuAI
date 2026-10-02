from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from RescuAI.backend.app.models.sos import InputType, UrgencyLevel, SOSCategory, SOSStatus


class SOSTextCreate(BaseModel):
    raw_text: str = Field(..., description="Raw text distress message from citizen")
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class GeminiExtractionResult(BaseModel):
    transcribed_text: str = Field(default="", description="Full verbatim text or transcript")
    urgency_level: UrgencyLevel = Field(default=UrgencyLevel.MODERATE, description="CRITICAL | MODERATE | LOW")
    category: SOSCategory = Field(default=SOSCategory.GENERAL, description="MEDICAL | TRAPPED | FOOD_WATER | INFANT_ELDERLY | GENERAL")
    extracted_location: Optional[str] = Field(default="Unknown", description="Landmark or address extracted")
    latitude: Optional[float] = Field(default=None, description="Latitude coordinate if extracted")
    longitude: Optional[float] = Field(default=None, description="Longitude coordinate if extracted")
    trapped_count: int = Field(default=1, description="Estimated count of trapped individuals")
    medical_details: Optional[str] = Field(default=None, description="Specific medical condition or needs")
    action_summary: str = Field(default="", description="1-2 sentence operational response plan")
    is_spam_or_fake: bool = Field(default=False, description="Flag for nonsensical or spam messages")


class DispatchCardResponse(BaseModel):
    id: str
    sos_id: str
    assigned_team: str
    supplies_needed: Optional[str] = None
    notes: Optional[str] = None
    updated_at: datetime

    class Config:
        from_attributes = True


class SOSResponse(BaseModel):
    id: str
    input_type: InputType
    raw_text: Optional[str] = None
    audio_file_path: Optional[str] = None
    transcribed_text: Optional[str] = None
    urgency_level: UrgencyLevel
    category: SOSCategory
    extracted_location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    trapped_count: int
    medical_details: Optional[str] = None
    action_summary: Optional[str] = None
    is_spam_or_fake: bool
    cluster_id: Optional[str] = None
    status: SOSStatus
    created_at: datetime
    dispatch_card: Optional[DispatchCardResponse] = None

    class Config:
        from_attributes = True


class StatusUpdatePayload(BaseModel):
    status: SOSStatus
    assigned_team: Optional[str] = "Team Alpha"
    supplies_needed: Optional[str] = None
    notes: Optional[str] = None
