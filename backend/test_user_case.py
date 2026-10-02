from RescuAI.backend.app.services.gemini_service import gemini_service

user_text = "We are safe on the 2nd floor at Sunshine Apartments, Civil Lines, but clean water supply is completely blocked and we have run out of baby milk powder and food for 2 children since yesterday. Please send dry food packets and drinking water."

print("\n" + "="*70)
print("TESTING USER'S EXACT DISRESS MESSAGE:")
print(f"\"{user_text}\"")
print("="*70)

res = gemini_service.process_text(user_text)

print(f"\n[1] Extracted Location:  {res.extracted_location}")
print(f"[2] Urgency Level:       {res.urgency_level}")
print(f"[3] Category:            {res.category}")
print(f"[4] Trapped Count:       {res.trapped_count}")
print(f"[5] Medical Details:     {res.medical_details}")
print(f"[6] DYNAMIC Action Plan: {res.action_summary}")
print("="*70)
