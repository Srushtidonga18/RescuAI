import os

path = 'backend/app/api/v1/sos.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old_fallback = '''                return {"response": response.text}
            except Exception as e:
                pass
                
    return {"response": "Wash with clean water and seek medical help if available."}'''

new_fallback = '''                return {"response": response.text}
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
        
    return {"response": ans}'''

content = content.replace(old_fallback, new_fallback)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
