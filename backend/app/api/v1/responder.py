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
