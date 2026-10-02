import os

path = 'frontend/src/components/SOSCard.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add volunteers prop
content = content.replace('const SOSCard = ({ item, onStatusUpdated, onViewDispatchCard }) => {', 'const SOSCard = ({ item, volunteers = [], onStatusUpdated, onViewDispatchCard }) => {')

# 2. Add handleDelete logic
delete_logic = """  const handleStatusChange = async (newStatus, manualTeam = null) => {
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
      });
      if (onStatusUpdated) onStatusUpdated();
    } catch (err) {
      console.error('Status update failed:', err);
    } finally {
      setUpdating(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to permanently delete this resolved case?")) {
      try {
        await api.delete(`/api/v1/responder/sos/${item.id}`);
        if (onStatusUpdated) onStatusUpdated();
      } catch (err) {
        console.error("Delete failed", err);
      }
    }
  };"""

content = content.replace('''  const handleStatusChange = async (newStatus) => {
    setUpdating(true);
    try {
      await api.patch(`/api/v1/responder/sos/${item.id}/status`, {
        status: newStatus,
        assigned_team: 'Alpha Rescue Squad',
      });
      if (onStatusUpdated) onStatusUpdated();
    } catch (err) {
      console.error('Status update failed:', err);
    } finally {
      setUpdating(false);
    }
  };''', delete_logic)

# 3. Add Dropdown to Dispatch button
old_dispatch = """          {item.status === 'PENDING' && (
            <button
              disabled={updating}
              onClick={() => handleStatusChange('DISPATCHED')}
              className="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-[11px] font-bold transition-colors shadow-sm flex items-center gap-1"
            >
              <Truck className="w-3 h-3" />
              <span>Dispatch</span>
            </button>
          )}"""

new_dispatch = """          {item.status === 'PENDING' && (
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
content = content.replace(old_dispatch, new_dispatch)

# 4. Add Delete button to Rescued
old_rescued = """          {item.status === 'RESCUED' && (
            <button
              disabled={true}
              className="px-2.5 py-1 bg-slate-800 text-emerald-500 rounded text-[11px] font-bold flex items-center gap-1 border border-emerald-500/30"
            >
              <CheckCircle2 className="w-3 h-3" />
              <span>Resolved</span>
            </button>
          )}"""

new_rescued = """          {item.status === 'RESCUED' && (
            <button
              onClick={handleDelete}
              className="px-2.5 py-1 bg-red-900/30 hover:bg-red-900/50 text-red-400 rounded text-[11px] font-bold flex items-center gap-1 border border-red-500/30 transition-colors"
            >
              <span>Delete</span>
            </button>
          )}"""
content = content.replace(old_rescued, new_rescued)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
