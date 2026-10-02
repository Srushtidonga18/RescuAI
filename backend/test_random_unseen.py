from RescuAI.backend.app.services.gemini_service import gemini_service

unseen_text_1 = "Emergency in Sector 9 Patna! Pregnant woman 8 months having severe abdominal pain and water level rising fast, ambulance road blocked."
unseen_text_2 = "Kolkata Salt Lake Sector 5, 2 stroke patients trapped in ground floor house, power cut since 2 days, need ICU transport."

print("\n" + "="*75)
print("TESTING COMPLETELY UNSEEN RANDOM DISTRESS CALL 1:")
print(f"\"{unseen_text_1}\"")
print("="*75)
res1 = gemini_service.process_text(unseen_text_1)
print(f"Location:  {res1.extracted_location}")
print(f"Urgency:   {res1.urgency_level}")
print(f"Category:  {res1.category}")
print(f"Action:    {res1.action_summary}")

print("\n" + "="*75)
print("TESTING COMPLETELY UNSEEN RANDOM DISTRESS CALL 2:")
print(f"\"{unseen_text_2}\"")
print("="*75)
res2 = gemini_service.process_text(unseen_text_2)
print(f"Location:  {res2.extracted_location}")
print(f"Urgency:   {res2.urgency_level}")
print(f"Category:  {res2.category}")
print(f"Action:    {res2.action_summary}")
print("="*75)
