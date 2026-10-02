from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import case
from RescuAI.backend.app.api.deps import get_db, get_current_user
from RescuAI.backend.app.models.user import User
from RescuAI.backend.app.models.sos import SOSRequest, DispatchCard, UrgencyLevel, SOSCategory, SOSStatus
from RescuAI.backend.app.schemas.sos import SOSResponse, DispatchCardResponse, StatusUpdatePayload

router = APIRouter()


@router.get("/dashboard", response_model=List[SOSResponse])
def get_responder_dashboard(
    urgency: Optional[UrgencyLevel] = None,
    category: Optional[SOSCategory] = None,
    status_filter: Optional[SOSStatus] = Query(None, alias="status"),
    search_location: Optional[str] = None,
    hide_spam: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Responder Emergency Command Center Dashboard.
    Sorted by Urgency Level (CRITICAL -> MODERATE -> LOW) and newest first.
    """
    query = db.query(SOSRequest)

    if hide_spam:
        query = query.filter(SOSRequest.is_spam_or_fake == False)

    if urgency:
        query = query.filter(SOSRequest.urgency_level == urgency)

    if category:
        query = query.filter(SOSRequest.category == category)

    if status_filter:
        query = query.filter(SOSRequest.status == status_filter)

    if search_location:
        query = query.filter(SOSRequest.extracted_location.ilike(f"%{search_location}%"))

    # Custom order: CRITICAL first, then MODERATE, then LOW
    urgency_order = case(
        (SOSRequest.urgency_level == UrgencyLevel.CRITICAL, 1),
        (SOSRequest.urgency_level == UrgencyLevel.MODERATE, 2),
        (SOSRequest.urgency_level == UrgencyLevel.LOW, 3),
        else_=4
    )

    results = query.order_by(urgency_order, SOSRequest.created_at.desc()).all()
    return results


@router.patch("/sos/{sos_id}/status", response_model=SOSResponse)
def update_sos_status(
    sos_id: str,
    payload: StatusUpdatePayload,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update status (PENDING -> DISPATCHED -> RESCUED) and update Dispatch Card."""
    sos_record = db.query(SOSRequest).filter(SOSRequest.id == sos_id).first()
    if not sos_record:
        raise HTTPException(status_code=404, detail="SOS Request not found.")

    sos_record.status = payload.status
    db.add(sos_record)

    # Update or create DispatchCard
    dispatch_card = db.query(DispatchCard).filter(DispatchCard.sos_id == sos_id).first()
    if not dispatch_card:
        dispatch_card = DispatchCard(
            sos_id=sos_id,
            assigned_team=payload.assigned_team or "Team Alpha",
            supplies_needed=payload.supplies_needed,
            notes=payload.notes or sos_record.action_summary
        )
    else:
        if payload.assigned_team:
            dispatch_card.assigned_team = payload.assigned_team
        if payload.supplies_needed:
            dispatch_card.supplies_needed = payload.supplies_needed
        if payload.notes:
            dispatch_card.notes = payload.notes

    db.add(dispatch_card)
    db.commit()
    db.refresh(sos_record)

    return sos_record


@router.get("/sos/{sos_id}/dispatch-card", response_model=DispatchCardResponse)
def get_dispatch_card(
    sos_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve formatted Rescue Dispatch Card for field teams."""
    dispatch_card = db.query(DispatchCard).filter(DispatchCard.sos_id == sos_id).first()
    if not dispatch_card:
        raise HTTPException(status_code=404, detail="Dispatch card not found for this SOS request.")
    return dispatch_card


import os
from fastapi.responses import FileResponse
from gtts import gTTS

VOICE_UPLOADS_DIR = "uploads/voice"
os.makedirs(VOICE_UPLOADS_DIR, exist_ok=True)

@router.get("/sos/{sos_id}/voice-dispatch", status_code=status.HTTP_200_OK)
def get_voice_dispatch(
    sos_id: str,
    db: Session = Depends(get_db)
):
    sos_record = db.query(SOSRequest).filter(SOSRequest.id == sos_id).first()
    if not sos_record:
        raise HTTPException(status_code=404, detail="SOS Request not found.")
        
    dispatch_card = db.query(DispatchCard).filter(DispatchCard.sos_id == sos_id).first()
    
    text_to_read = f"Emergency Alert. Location: {sos_record.extracted_location}. "
    text_to_read += f"Urgency is {sos_record.urgency_level}. "
    
    if dispatch_card and dispatch_card.notes:
        text_to_read += f"Action plan: {dispatch_card.notes}. "
    elif sos_record.action_summary:
        text_to_read += f"Action plan: {sos_record.action_summary}. "

    if sos_record.medical_details:
        text_to_read += f"Medical details: {sos_record.medical_details}."

    file_path = os.path.join(VOICE_UPLOADS_DIR, f"voice_dispatch_{sos_id}.mp3")
    
    tts = gTTS(text=text_to_read, lang='en')
    tts.save(file_path)
    
    return FileResponse(path=file_path, media_type='audio/mpeg', filename=f"voice_dispatch_{sos_id}.mp3")

from RescuAI.backend.app.models.inventory import ResourceItem, Volunteer
from pydantic import BaseModel

class ResourceItemCreate(BaseModel):
    name: str
    quantity: int

class VolunteerCreate(BaseModel):
    name: str
    phone: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

@router.post("/inventory", status_code=status.HTTP_201_CREATED)
def add_inventory(
    payload: ResourceItemCreate,
    db: Session = Depends(get_db)
):
    item = ResourceItem(name=payload.name, quantity=payload.quantity)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@router.get("/inventory", status_code=status.HTTP_200_OK)
def get_inventory(db: Session = Depends(get_db)):
    return db.query(ResourceItem).all()

@router.post("/volunteer", status_code=status.HTTP_201_CREATED)
def add_volunteer(
    payload: VolunteerCreate,
    db: Session = Depends(get_db)
):
    volunteer = Volunteer(name=payload.name, phone=payload.phone, latitude=payload.latitude, longitude=payload.longitude)
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)
    return volunteer

@router.get("/volunteer", status_code=status.HTTP_200_OK)
def get_volunteers(db: Session = Depends(get_db)):
    return db.query(Volunteer).all()


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import datetime

REPORTS_DIR = "uploads/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

@router.get("/report/pdf", status_code=status.HTTP_200_OK)
def get_pdf_report(db: Session = Depends(get_db)):
    total_requests = db.query(SOSRequest).count()
    critical_requests = db.query(SOSRequest).filter(SOSRequest.urgency_level == UrgencyLevel.CRITICAL).count()
    pending_requests = db.query(SOSRequest).filter(SOSRequest.status == SOSStatus.PENDING).count()

    filename = f"report_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    file_path = os.path.join(REPORTS_DIR, filename)

    c = canvas.Canvas(file_path, pagesize=letter)
    c.drawString(100, 750, "RescuAI - Emergency Response Report")
    c.drawString(100, 730, f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(100, 700, f"Total SOS Requests: {total_requests}")
    c.drawString(100, 680, f"Critical Requests: {critical_requests}")
    c.drawString(100, 660, f"Pending Requests: {pending_requests}")
    c.save()

    return FileResponse(path=file_path, media_type='application/pdf', filename=filename)
