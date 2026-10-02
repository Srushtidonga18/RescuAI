import uuid
import math
from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from RescuAI.backend.app.models.sos import SOSRequest, SOSStatus


def calculate_distance_meters(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Haversine formula to compute distance in meters between two lat/long points."""
    R = 6371000  # Radius of earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def find_or_create_cluster(
    db: Session,
    location: Optional[str],
    category: str,
    lat: Optional[float],
    lon: Optional[float],
    time_window_minutes: int = 30
) -> str:
    """
    Checks if a matching pending SOS request exists within the last N minutes by landmark or GPS proximity (~500m).
    Returns the cluster_id to assign to the new request.
    """
    cutoff_time = datetime.now(timezone.utc) - timedelta(minutes=time_window_minutes)

    # Query recent pending SOS requests of the same category
    recent_requests = db.query(SOSRequest).filter(
        SOSRequest.created_at >= cutoff_time,
        SOSRequest.status == SOSStatus.PENDING,
        SOSRequest.is_spam_or_fake == False
    ).all()

    for req in recent_requests:
        # Check 1: Text landmark match (case insensitive substring match)
        if location and req.extracted_location and location.lower() != "unknown":
            if location.lower() in req.extracted_location.lower() or req.extracted_location.lower() in location.lower():
                cluster = req.cluster_id or str(uuid.uuid4())
                if not req.cluster_id:
                    req.cluster_id = cluster
                    db.add(req)
                return cluster

        # Check 2: GPS coordinate proximity within 500 meters
        if lat and lon and req.latitude and req.longitude:
            dist = calculate_distance_meters(lat, lon, req.latitude, req.longitude)
            if dist <= 500.0:  # 500 meters threshold
                cluster = req.cluster_id or str(uuid.uuid4())
                if not req.cluster_id:
                    req.cluster_id = cluster
                    db.add(req)
                return cluster

    # If no match found, create a fresh cluster_id for this unique request
    return str(uuid.uuid4())
