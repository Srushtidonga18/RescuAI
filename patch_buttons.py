import os
import re

path = 'frontend/src/components/ResponderDashboard.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix handleStatusChange
old_logic = '''  const handleStatusChange = async (sosId, newStatus) => {
    try {
      let team = 'Alpha Rescue Squad';
      
      if (newStatus === 'DISPATCHED') {
        const volNames = volunteers.map(v => v.name).join(', ');
        const defaultName = volunteers.length > 0 ? volunteers[0].name : 'Alpha Rescue Squad';
        const userInput = window.prompt(Assign a Volunteer/Team for this rescue.\\nAvailable: \\n\\nEnter Team Name:, defaultName);
        
        if (userInput === null) return; // Cancelled
        team = userInput || defaultName;
      }

      await api.patch(/api/v1/responder/sos//status, {
        status: newStatus,
        assigned_team: team,
      });
      fetchDashboardData();
    } catch (err) {
      console.error('Status update failed:', err);
    }
  };'''

new_logic = '''  const handleStatusChange = async (sosId, newStatus, manualTeam = null) => {
    try {
      let team = manualTeam;
      if (!team && volunteers && volunteers.length > 0) {
        team = volunteers[0].name;
      } else if (!team) {
        team = 'Alpha Rescue Squad';
      }

      await api.patch(/api/v1/responder/sos//status, {
        status: newStatus,
        assigned_team: team,
      });
      fetchDashboardData();
    } catch (err) {
      console.error('Status update failed:', err);
    }
  };'''

if old_logic in content:
    content = content.replace(old_logic, new_logic)
else:
    # Use regex if direct replace fails
    pattern = re.compile(r'  const handleStatusChange = async \(sosId, newStatus\) => \{[\s\S]*?console\.error\(\'Status update failed:\', err\);\s*\}\s*\};')
    content = pattern.sub(new_logic, content)

# Replace the buttons
old_buttons = '''{item.status === 'PENDING' && <button onClick={() => handleStatusChange(item.id, 'DISPATCHED')} className="px-2 py-1 bg-blue-600 text-white rounded text-[10px] font-bold">Dispatch</button>}'''

new_buttons = '''{item.status === 'PENDING' && (
  <div className="inline-flex items-center gap-1">
    <select id={	eam-select-} className="px-1 py-1 text-[10px] border border-slate-300 rounded bg-white" defaultValue="">
      <option value="">Auto Assign</option>
      {volunteers.map(v => <option key={v.name} value={v.name}>{v.name}</option>)}
    </select>
    <button onClick={() => {
      const selectEl = document.getElementById(	eam-select-);
      handleStatusChange(item.id, 'DISPATCHED', selectEl ? selectEl.value : null);
    }} className="px-2 py-1 bg-blue-600 text-white rounded text-[10px] font-bold">Dispatch</button>
  </div>
)}'''

content = content.replace(old_buttons, new_buttons)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
