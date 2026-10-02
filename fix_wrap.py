import os

path = 'frontend/src/components/SOSCard.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make the outer container wrap
old_outer = '      <div className="flex items-center justify-between gap-1.5 pt-2 border-t border-slate-800">'
new_outer = '      <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-800">'
content = content.replace(old_outer, new_outer)

# Make the inner container wrap
old_inner = '        <div className="flex items-center gap-1.5">'
new_inner = '        <div className="flex flex-wrap items-center justify-end gap-1.5 mt-1 sm:mt-0">'
content = content.replace(old_inner, new_inner)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
