from RescuAI.backend.app.services.gemini_service import gemini_service

user_hinglish_text = "Kripya madad karein! Village Rampur, Near Old Panchayat Ghar. Nadi ka pani gaon me ghus gaya hai. 65 saal ke buzurg ko tez bukhar aur dehydration hai, doctor ya ambulance nahi aa pa rahi. Khane ka raashan aur ORS/dawai bhej do."

print("\n" + "="*75)
print("TESTING USER'S SCREENSHOT HINGLISH MESSAGE:")
print(f"\"{user_hinglish_text}\"")
print("="*75)

res = gemini_service.process_text(user_hinglish_text)

print(f"\n[1] Extracted Location:  {res.extracted_location}")
print(f"[2] Urgency Level:       {res.urgency_level}")
print(f"[3] Category:            {res.category}")
print(f"[4] Trapped Count:       {res.trapped_count}")
print(f"[5] Medical Details:     {res.medical_details}")
print(f"[6] DYNAMIC Action Plan: {res.action_summary}")
print("="*75)
