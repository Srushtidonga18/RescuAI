import os
import re

path = 'frontend/src/components/ResponderDashboard.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

new_logic = '''  const handleStatusChange = async (sosId, newStatus) => {
    try {
      let team = 'Alpha Rescue Squad';
      
      if (newStatus === 'DISPATCHED') {
        const volNames = volunteers.map(v => v.name).join(', ');
        const defaultName = volunteers.length > 0 ? volunteers[0].name : 'Alpha Rescue Squad';
        const userInput = window.prompt(Assign a Volunteer/Team for this rescue.\\nAvailable:  + volNames + \\n\\nEnter Team Name:, defaultName);
        
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

# Regex to match the entire handleStatusChange function
pattern = re.compile(r'  const handleStatusChange = async \(sosId, newStatus\) => \{[\s\S]*?fetchDashboardData\(\);\s*\} catch \(err\) \{\s*console\.error\(\'Status update failed:\', err\);\s*\}\s*\};')
content = pattern.sub(new_logic, content)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
