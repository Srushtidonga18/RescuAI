import os
import re

path = 'frontend/src/components/ResponderDashboard.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'\{item\.status === \'PENDING\' && \([\s\S]*?</div>\s*\)\}', re.MULTILINE)
new_buttons = """{item.status === 'PENDING' && (
  <div className="inline-flex items-center gap-1">
    <select id={`team-select-${item.id}`} className="px-1 py-1 text-[10px] border border-slate-300 rounded bg-white" defaultValue="">
      <option value="">Auto Assign</option>
      {volunteers.map(v => <option key={v.name} value={v.name}>{v.name}</option>)}
    </select>
    <button onClick={() => {
      const selectEl = document.getElementById(`team-select-${item.id}`);
      handleStatusChange(item.id, 'DISPATCHED', selectEl ? selectEl.value : null);
    }} className="px-2 py-1 bg-blue-600 text-white rounded text-[10px] font-bold">Dispatch</button>
  </div>
)}"""

content = pattern.sub(new_buttons, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
