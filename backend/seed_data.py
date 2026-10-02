import sys
import os

# Add root directory to python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from RescuAI.backend.app.core.database import SessionLocal, engine, Base
from RescuAI.backend.app.models.sos import SOSRequest, InputType, UrgencyLevel, SOSCategory, SOSStatus
from RescuAI.backend.app.models.inventory import ResourceItem, Volunteer
import uuid
from datetime import datetime, timezone, timedelta

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # 1. Clear existing test data
    db.query(SOSRequest).delete()
    db.query(ResourceItem).delete()
    db.query(Volunteer).delete()
    db.commit()

    # 2. Add Inventory
    resources = [
        ResourceItem(name="Inflatable Life Boats", quantity=15),
        ResourceItem(name="First Aid Kits", quantity=150),
        ResourceItem(name="Food Packets (MRE)", quantity=500),
        ResourceItem(name="Drinking Water (Liters)", quantity=2000),
        ResourceItem(name="Blankets", quantity=300),
    ]
    db.add_all(resources)

    # 3. Add Volunteers
    volunteers = [
        Volunteer(name="Rahul Sharma", phone="+91 9876543210", latitude=19.0760, longitude=72.8777),
        Volunteer(name="Priya Patel", phone="+91 8765432109", latitude=19.0800, longitude=72.8800),
        Volunteer(name="Dr. Amit Kumar", phone="+91 7654321098", latitude=19.0700, longitude=72.8700),
        Volunteer(name="Sunita Singh", phone="+91 6543210987", latitude=19.0900, longitude=72.8900),
    ]
    db.add_all(volunteers)

    # 4. Add SOS Requests (Simulating a flood in Mumbai)
    sos_requests = [
        SOSRequest(
            raw_text="Paani ghar ke andar aa gaya hai, hum 3 log chhat par fase hain. Jaldi madad bhejo!",
            extracted_location="Dharavi, Mumbai",
            latitude=19.0380,
            longitude=72.8538,
            urgency_level=UrgencyLevel.CRITICAL,
            category=SOSCategory.TRAPPED,
            trapped_count=3,
            status=SOSStatus.PENDING,
            action_summary="Dispatch inflatable boat. Priority rescue for 3 trapped individuals.",
            created_at=datetime.now(timezone.utc) - timedelta(minutes=5)
        ),
        SOSRequest(
            raw_text="Need medical help immediately. An old man is having trouble breathing due to cold water.",
            extracted_location="Kurla West, Mumbai",
            latitude=19.0728,
            longitude=72.8826,
            urgency_level=UrgencyLevel.CRITICAL,
            category=SOSCategory.MEDICAL,
            trapped_count=1,
            status=SOSStatus.PENDING,
            action_summary="Dispatch ambulance with oxygen support. Medical emergency.",
            created_at=datetime.now(timezone.utc) - timedelta(minutes=15)
        ),
        SOSRequest(
            raw_text="Bhookh aur pyas se bura haal hai, yaha 15 log camp me hain.",
            extracted_location="Bandra East",
            latitude=19.0596,
            longitude=72.8295,
            urgency_level=UrgencyLevel.MODERATE,
            category=SOSCategory.FOOD_WATER,
            trapped_count=15,
            status=SOSStatus.DISPATCHED,
            action_summary="Deliver 15 food packets and 30 liters water.",
            created_at=datetime.now(timezone.utc) - timedelta(hours=1)
        ),
        SOSRequest(
            raw_text="Tree fell on the main road, completely blocking the path.",
            extracted_location="Andheri East",
            latitude=19.1136,
            longitude=72.8697,
            urgency_level=UrgencyLevel.LOW,
            category=SOSCategory.GENERAL,
            trapped_count=0,
            status=SOSStatus.RESCUED,
            action_summary="Road block logged. Forwarding to municipal corporation.",
            created_at=datetime.now(timezone.utc) - timedelta(hours=3)
        ),
    ]
    db.add_all(sos_requests)
    
    db.commit()
    db.close()
    print("Successfully seeded all test data!")

if __name__ == "__main__":
    seed_data()
