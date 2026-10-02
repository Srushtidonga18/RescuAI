import os
import re

path = 'frontend/src/components/SOSCard.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Make it completely light-themed and professional
content = content.replace('bg-slate-900 border border-slate-800 rounded-xl p-3.5 text-white shadow-md transition-all hover:border-slate-700', 'bg-white border border-slate-200 rounded-xl p-4 text-slate-800 shadow-sm hover:shadow-md transition-all')

# Fix text colors inside
content = content.replace('text-slate-400', 'text-slate-500')
content = content.replace('text-slate-300', 'text-slate-600')
content = content.replace('bg-slate-800', 'bg-slate-100')
content = content.replace('hover:bg-slate-700', 'hover:bg-slate-200')
content = content.replace('text-white', 'text-slate-900')
content = content.replace('bg-slate-950/50 border-slate-800', 'bg-slate-50 border-slate-200')
content = content.replace('border-slate-700', 'border-slate-300')
content = content.replace('bg-blue-600 text-slate-900', 'bg-blue-600 text-white') # Revert buttons to white text
content = content.replace('bg-emerald-600 text-slate-900', 'bg-emerald-600 text-white')
content = content.replace('bg-slate-100 hover:bg-slate-200 text-slate-900', 'bg-white hover:bg-slate-100 text-slate-700 border border-slate-300') # Card button

# Badges
content = content.replace("bg-blue-500/15 text-blue-400 border-blue-500/30", "bg-blue-50 text-blue-700 border-blue-200")
content = content.replace("bg-emerald-500/15 text-emerald-400 border-emerald-500/30", "bg-emerald-50 text-emerald-700 border-emerald-200")
content = content.replace("bg-amber-500/15 text-amber-400 border-amber-500/30", "bg-amber-50 text-amber-700 border-amber-200")

# Delete button function
delete_logic = """
  const handleDelete = async () => {
    if (window.confirm("Are you sure you want to permanently delete this resolved case?")) {
      try {
        await api.delete(`/api/v1/responder/sos/${item.id}`);
        if (onStatusUpdated) onStatusUpdated();
      } catch (err) {
        console.error("Delete failed", err);
      }
    }
  };
"""
content = content.replace('const handleCopyLocation = () => {', delete_logic + '\n  const handleCopyLocation = () => {')

# Add Delete button in the UI next to Rescued state
delete_btn = """          {item.status === 'RESCUED' && (
            <button
              onClick={handleDelete}
              className="px-2.5 py-1 bg-red-100 hover:bg-red-200 text-red-700 rounded text-[11px] font-bold transition-colors flex items-center gap-1"
            >
              <span>Delete</span>
            </button>
          )}"""

content = content.replace("{item.status === 'RESCUED' && (", delete_btn + "\n\n          {/* Original Rescued logic hidden if needed, or kept */}          {item.status === 'RESCUED' && false && (")

# Re-fix some button text colors that might have gotten messed up
content = content.replace('text-slate-900', 'text-slate-800')
content = content.replace('bg-blue-600 hover:bg-blue-500 text-slate-800', 'bg-blue-600 hover:bg-blue-500 text-white')
content = content.replace('bg-emerald-600 hover:bg-emerald-500 text-slate-800', 'bg-emerald-600 hover:bg-emerald-500 text-white')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
