import os
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from RescuAI.backend.app.api.deps import get_db
from RescuAI.backend.app.models.sos import SOSRequest, DispatchCard, InputType, SOSStatus
from RescuAI.backend.app.schemas.sos import SOSTextCreate, SOSResponse
from RescuAI.backend.app.services.gemini_service import gemini_service, AVAILABLE_GEMINI_MODELS
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


@router.get("/map-data", status_code=status.HTTP_200_OK)
def get_map_data(db: Session = Depends(get_db)):
    sos_records = db.query(SOSRequest).filter(
        SOSRequest.latitude.isnot(None), 
        SOSRequest.longitude.isnot(None)
    ).all()
    
    return [
        {
            "id": req.id,
            "latitude": req.latitude,
            "longitude": req.longitude,
            "urgency_level": req.urgency_level,
            "status": req.status,
            "category": req.category
        }
        for req in sos_records
    ]


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


IMAGE_UPLOADS_DIR = "uploads/images"
os.makedirs(IMAGE_UPLOADS_DIR, exist_ok=True)

@router.post("/image", response_model=SOSResponse, status_code=status.HTTP_201_CREATED)
async def submit_sos_image(
    file: UploadFile = File(...),
    latitude: Optional[float] = Form(None),
    longitude: Optional[float] = Form(None),
    db: Session = Depends(get_db)
):
    valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in valid_extensions:
        raise HTTPException(status_code=400, detail=f"Unsupported image file format. Allowed: {valid_extensions}")

    image_bytes = await file.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded image file is empty.")

    file_id = str(uuid.uuid4())
    saved_filename = f"{file_id}{ext}"
    file_path = os.path.join(IMAGE_UPLOADS_DIR, saved_filename)
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    mime_type = "image/jpeg"
    if ext == ".png":
        mime_type = "image/png"
    elif ext == ".webp":
        mime_type = "image/webp"

    extraction = gemini_service.process_image(
        image_bytes=image_bytes,
        mime_type=mime_type,
        user_lat=latitude,
        user_long=longitude
    )

    cluster_id = find_or_create_cluster(
        db=db,
        location=extraction.extracted_location,
        category=extraction.category,
        lat=extraction.latitude,
        lon=extraction.longitude
    )

    sos_record = SOSRequest(
        input_type=InputType.IMAGE,
        image_file_path=file_path,
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

from fastapi.responses import Response

@router.post("/webhook/twilio", status_code=status.HTTP_200_OK)
def twilio_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    db: Session = Depends(get_db)
):
    # Process text through Gemini 1.5 Flash
    extraction = gemini_service.process_text(
        text=Body,
        user_lat=None,
        user_long=None
    )

    cluster_id = find_or_create_cluster(
        db=db,
        location=extraction.extracted_location,
        category=extraction.category,
        lat=extraction.latitude,
        lon=extraction.longitude
    )

    sos_record = SOSRequest(
        input_type=InputType.TEXT,
        raw_text=Body,
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

    if not sos_record.is_spam_or_fake:
        dispatch_card = DispatchCard(
            sos_id=sos_record.id,
            assigned_team="Unassigned",
            supplies_needed=f"Category: {sos_record.category.value}. Medical: {sos_record.medical_details or 'None'}",
            notes=sos_record.action_summary
        )
        db.add(dispatch_card)
        db.commit()

    twiml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Message>Your SOS request has been received. Help is on the way. Urgency: {extraction.urgency_level.value}</Message>
</Response>"""
    return Response(content=twiml_response, media_type="application/xml")

class FirstAidQuery(BaseModel):
    query: str

@router.post("/first-aid", status_code=status.HTTP_200_OK)
def first_aid_chatbot(payload: FirstAidQuery):
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    prompt = f"You are a medical first-aid assistant for disaster situations. Provide concise and clear first-aid instructions for the following query: {payload.query}"
    
    if gemini_service.client:
        for model_name in AVAILABLE_GEMINI_MODELS:
            try:
                response = gemini_service.client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                return {"response": response.text}
            except Exception as e:
                pass
                
    # Offline Fallback Dictionary if API Key is invalid
    query_lower = payload.query.lower()
    if 'how can you help' in query_lower or 'what is this' in query_lower:
        ans = "I am an offline First-Aid AI. I can give emergency advice for burns, cuts, snake bites, fractures, and CPR."
    elif 'hindi' in query_lower:
        ans = "Haan, main Hindi samajh sakta hoon. Apni medical emergency bataiye."
    elif 'snake' in query_lower or 'bite' in query_lower:
        ans = "Keep the person calm and still. Immobilize the bitten area lower than the heart. Do NOT suck the venom. Seek immediate medical help."
    elif 'burn' in query_lower or 'fire' in query_lower:
        ans = "Cool the burn under cold running water for at least 10 minutes. Do not apply ice or butter. Cover with a sterile, non-fluffy dressing."
    elif 'cut' in query_lower or 'bleed' in query_lower:
        ans = "Apply firm, direct pressure to the wound using a clean cloth. Elevate the injured area above the heart if possible."
    elif 'fracture' in query_lower or 'bone' in query_lower or 'break' in query_lower:
        ans = "Do not move the injured part. Immobilize it using a splint or padding. Apply an ice pack wrapped in cloth to reduce swelling."
    elif 'cpr' in query_lower or 'heart' in query_lower or 'breathe' in query_lower:
        ans = "Call for emergency help immediately. Place the heel of your hand on the center of the chest and push hard and fast (100-120 compressions per minute)."
    else:
        ans = "[Offline Mode]: Wash any wounds with clean water. Keep the patient calm. Elevate injuries to reduce bleeding, and wait for emergency responders."
        
    return {"response": ans}
