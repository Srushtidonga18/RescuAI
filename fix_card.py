import os
import re

path = 'frontend/src/components/SOSCard.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add volunteers prop
content = content.replace('const SOSCard = ({ item, onStatusUpdated, onViewDispatchCard }) => {', 'const SOSCard = ({ item, volunteers = [], onStatusUpdated, onViewDispatchCard }) => {')

# 2. Update handleStatusChange
old_handler = """  const handleStatusChange = async (newStatus) => {
    setUpdating(true);
    try {
      await api.patch(`/api/v1/responder/sos/${item.id}/status`, {
        status: newStatus,
        assigned_team: 'Alpha Rescue Squad',
      });"""

new_handler = """  const handleStatusChange = async (newStatus, manualTeam = null) => {
    setUpdating(true);
    try {
      let team = manualTeam;
      if (!team && volunteers && volunteers.length > 0) {
        team = volunteers[0].name;
      } else if (!team) {
        team = 'Alpha Rescue Squad';
      }
      await api.patch(`/api/v1/responder/sos/${item.id}/status`, {
        status: newStatus,
        assigned_team: team,
      });"""

content = content.replace(old_handler, new_handler)

# 3. Update the Dispatch Button to include the dropdown
old_button_block = """          {item.status === 'PENDING' && (
            <button
              disabled={updating}
              onClick={() => handleStatusChange('DISPATCHED')}
              className="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-[11px] font-bold transition-colors shadow-sm flex items-center gap-1"
            >
              <Truck className="w-3 h-3" />
              <span>Dispatch</span>
            </button>
          )}"""

new_button_block = """          {item.status === 'PENDING' && (
            <div className="flex items-center gap-1">
              <select id={`card-select-${item.id}`} className="px-1 py-1 text-[10px] border border-slate-700 rounded bg-slate-800 text-white" defaultValue="">
                <option value="">Auto Assign</option>
                {volunteers.map(v => <option key={v.name} value={v.name}>{v.name}</option>)}
              </select>
              <button
                disabled={updating}
                onClick={() => {
                  const selectEl = document.getElementById(`card-select-${item.id}`);
                  handleStatusChange('DISPATCHED', selectEl ? selectEl.value : null);
                }}
                className="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-[11px] font-bold transition-colors shadow-sm flex items-center gap-1"
              >
                <Truck className="w-3 h-3" />
                <span>Dispatch</span>
              </button>
            </div>
          )}"""

content = content.replace(old_button_block, new_button_block)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
