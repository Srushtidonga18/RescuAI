import os
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from RescuAI.backend.app.api.deps import get_db
from RescuAI.backend.app.models.sos import SOSRequest, DispatchCard, InputType, SOSStatus
from RescuAI.backend.app.schemas.sos import SOSTextCreate, SOSResponse
from RescuAI.backend.app.services.gemini_service import gemini_service
from RescuAI.backend.app.services.deduplication_service import find_or_create_cluster

router = APIRouter()

UPLOADS_DIR = "uploads/audio"
os.makedirs(UPLOADS_DIR, exist_ok=True)


@router.post("/text", response_model=SOSResponse, status_code=status.HTTP_201_CREATED)
def submit_sos_text(
    payload: SOSTextCreate,
    db: Session = Depends(get_db)
):
    if not payload.raw_text.strip():
        raise HTTPException(status_code=400, detail="Distress message text cannot be empty.")

    # 1. Process text through Gemini 1.5 Flash
    extraction = gemini_service.process_text(
        text=payload.raw_text,
        user_lat=payload.latitude,
        user_long=payload.longitude
    )

    # 2. Check for matching cluster / deduplication
    cluster_id = find_or_create_cluster(
        db=db,
        location=extraction.extracted_location,
        category=extraction.category,
        lat=extraction.latitude,
        lon=extraction.longitude
    )

    # 3. Store SOS record in Database
    sos_record = SOSRequest(
        input_type=InputType.TEXT,
        raw_text=payload.raw_text,
        transcribed_text=extraction.transcribed_text,
        urgency_level=extraction.urgency_level,
        category=extraction.category,
        extracted_location=extraction.extracted_location,
        latitude=extraction.latitude,
        longitude=extraction.longitude,
        trapped_count=extraction.trapped_count,
        medical_details=extraction.medical_details,
        action_summary=extraction.action_summary,
        is_spam_or_fake=extraction.is_spam_or_fake,
        cluster_id=cluster_id,
        status=SOSStatus.PENDING
    )

    db.add(sos_record)
    db.commit()
    db.refresh(sos_record)

    # 4. Create initial DispatchCard if not spam
    if not sos_record.is_spam_or_fake:
        dispatch_card = DispatchCard(
            sos_id=sos_record.id,
            assigned_team="Unassigned",
            supplies_needed=f"Category: {sos_record.category.value}. Medical: {sos_record.medical_details or 'None'}",
            notes=sos_record.action_summary
        )
        db.add(dispatch_card)
        db.commit()
        db.refresh(sos_record)

    return sos_record


@router.post("/audio", response_model=SOSResponse, status_code=status.HTTP_201_CREATED)
async def submit_sos_audio(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    db: Session = Depends(get_db)
):
    valid_extensions = [".mp3", ".wav", ".m4a", ".ogg", ".webm"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in valid_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported audio file format. Allowed: {valid_extensions}")

    audio_bytes = await file.read()
    if len(audio_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded audio file is empty.")

    # Save audio file locally for record keeping
    file_id = str(uuid.uuid4())
    saved_filename = f"{file_id}{ext}"
    file_path = os.path.join(UPLOADS_DIR, saved_filename)
    with open(file_path, "wb") as f:
        f.write(audio_bytes)

    # Determine MIME type
    mime_type = "audio/mp3"
    if ext == ".wav":
        mime_type = "audio/wav"
    elif ext == ".m4a":
        mime_type = "audio/m4a"

    # 1. Process audio natively using Gemini 1.5 Flash
    extraction = gemini_service.process_audio(
        audio_bytes=audio_bytes,
        mime_type=mime_type,
        user_lat=latitude,
        user_long=longitude
    )

    # 2. Check for matching cluster / deduplication
    cluster_id = find_or_create_cluster(
        db=db,
        location=extraction.extracted_location,
        category=extraction.category,
        lat=extraction.latitude,
        lon=extraction.longitude
    )

    # 3. Store SOS record in Database
    sos_record = SOSRequest(
        input_type=InputType.AUDIO,
        audio_file_path=file_path,
        transcribed_text=extraction.transcribed_text,
        urgency_level=extraction.urgency_level,
        category=extraction.category,
        extracted_location=extraction.extracted_location,
        latitude=extraction.latitude,
        longitude=extraction.longitude,
        trapped_count=extraction.trapped_count,
        medical_details=extraction.medical_details,
        action_summary=extraction.action_summary,
        is_spam_or_fake=extraction.is_spam_or_fake,
        cluster_id=cluster_id,
        status=SOSStatus.PENDING
    )

    db.add(sos_record)
    db.commit()
    db.refresh(sos_record)

    # 4. Create initial DispatchCard if not spam
    if not sos_record.is_spam_or_fake:
        dispatch_card = DispatchCard(
            sos_id=sos_record.id,
            assigned_team="Unassigned",
            supplies_needed=f"Category: {sos_record.category.value}. Medical: {sos_record.medical_details or 'None'}",
            notes=sos_record.action_summary
        )
        db.add(dispatch_card)
        db.commit()
        db.refresh(sos_record)

    return sos_record
