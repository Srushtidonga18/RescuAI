import os

path = 'backend/app/services/gemini_service.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

prefix = '''import os
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
load_dotenv(env_path)
'''

with open(path, 'w', encoding='utf-8') as f:
    f.write(prefix + content)
