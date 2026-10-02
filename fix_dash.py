import os

path = 'frontend/src/components/ResponderDashboard.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('item={item}', 'item={item}\n                  volunteers={volunteers}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
