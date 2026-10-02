import sys
from fastapi.testclient import TestClient
from RescuAI.backend.app.main import app

client = TestClient(app)

print("=" * 60)
print("  RESCUAI BACKEND API END-TO-END AUTOMATED TEST SUITE")
print("=" * 60)

# 1. Health Check Test
print("\n[1/6] Testing Health Endpoint GET /health...")
res = client.get("/health")
assert res.status_code == 200, f"Health check failed: {res.text}"
print("  -> PASSED! Response:", res.json())

# 2. Text SOS Submission Test
print("\n[2/6] Testing Public Citizen Text SOS Ingestion (POST /api/v1/sos/text)...")
sos_payload = {
    "raw_text": "Urgent! Flood water rising fast in Sector 14, House #204. 4 people trapped on roof. Elderly man needs insulin urgently!",
    "latitude": 28.6139,
    "longitude": 77.2090
}
res = client.post("/api/v1/sos/text", json=sos_payload)
assert res.status_code == 201, f"SOS text creation failed: {res.text}"
sos_data = res.json()
print("  -> PASSED! Created SOS Record ID:", sos_data["id"])
print("     Urgency Level:", sos_data["urgency_level"])
print("     Category:", sos_data["category"])
print("     Location:", sos_data["extracted_location"])
print("     Action Plan:", sos_data["action_summary"])

sos_id = sos_data["id"]

# 3. Authentication Login Test
print("\n[3/6] Testing Responder JWT Authentication (POST /api/v1/auth/login)...")
login_data = {
    "username": "responder@rescuai.org",
    "password": "admin123"
}
res = client.post("/api/v1/auth/login", data=login_data)
assert res.status_code == 200, f"Login failed: {res.text}"
token_data = res.json()
access_token = token_data["access_token"]
print("  -> PASSED! Generated JWT Token:", access_token[:30] + "...")

headers = {"Authorization": f"Bearer {access_token}"}

# 4. Responder Dashboard Fetch Test
print("\n[4/6] Testing Responder Command Dashboard (GET /api/v1/responder/dashboard)...")
res = client.get("/api/v1/responder/dashboard", headers=headers)
assert res.status_code == 200, f"Dashboard fetch failed: {res.text}"
dashboard_items = res.json()
print(f"  -> PASSED! Retrieved {len(dashboard_items)} prioritized SOS request(s) on dashboard.")

# 5. Update Status Test
print(f"\n[5/6] Testing Status Update for SOS ID {sos_id} (PATCH /api/v1/responder/sos/{{id}}/status)...")
update_payload = {
    "status": "DISPATCHED",
    "assigned_team": "Alpha Rescue Squad",
    "supplies_needed": "Inflatable Boat, Medical Insulin Kit, Oxygen Cylinder",
    "notes": "Deploying 4 personnel via boat immediately."
}
res = client.patch(f"/api/v1/responder/sos/{sos_id}/status", json=update_payload, headers=headers)
assert res.status_code == 200, f"Status update failed: {res.text}"
print("  -> PASSED! Updated SOS Status to:", res.json()["status"])

# 6. Retrieve Dispatch Card Test
print(f"\n[6/6] Testing Field Dispatch Card Retrieval (GET /api/v1/responder/sos/{{id}}/dispatch-card)...")
res = client.get(f"/api/v1/responder/sos/{sos_id}/dispatch-card", headers=headers)
assert res.status_code == 200, f"Dispatch card fetch failed: {res.text}"
card_data = res.json()
print("  -> PASSED! Dispatch Card Details:")
print("     Assigned Team:", card_data["assigned_team"])
print("     Supplies Needed:", card_data["supplies_needed"])
print("     Notes:", card_data["notes"])

print("\n" + "=" * 60)
print("  ALL 6 BACKEND API TESTS PASSED SUCCESSFULLY! 100% WORKING!")
print("=" * 60)
