from RescuAI.backend.app.services.gemini_service import gemini_service

spam_text = "Fresh fish and seafood available at discounted prices today! Delivery available near Sector 62. Call now for bulk orders. Also looking to buy a second-hand mobile phone under 5000 rupees."

print("\n" + "="*75)
print("TESTING USER SCREENSHOT SPAM TEST CASE:")
print(f"\"{spam_text}\"")
print("="*75)
res = gemini_service.process_text(spam_text)
print(f"Is Spam:   {res.is_spam_or_fake}")
print(f"Urgency:   {res.urgency_level}")
print(f"Category:  {res.category}")
print(f"Location:  {res.extracted_location}")
print(f"Action:    {res.action_summary}")
print("="*75)
