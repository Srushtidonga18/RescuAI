import React from 'react';
import { AlertTriangle, Clock, CheckCircle2, ShieldAlert } from 'lucide-react';

const StatsBar = ({ items = [], allItems = [] }) => {
  const source = allItems.length > 0 ? allItems : items;
  const totalCount = source.length;
  const criticalCount = source.filter((item) => item.urgency_level === 'CRITICAL').length;
  const pendingCount = source.filter((item) => item.status === 'PENDING').length;
  const dispatchedCount = source.filter((item) => item.status === 'DISPATCHED').length;
  const rescuedCount = source.filter((item) => item.status === 'RESCUED').length;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-3 shadow-md mb-5 flex flex-wrap items-center justify-between gap-3 text-white">
      {/* Total Active */}
      <div className="flex items-center gap-2.5 px-3 py-1.5 bg-slate-800/80 rounded-lg border border-slate-700/60">
        <ShieldAlert className="w-4 h-4 text-slate-400" />
        <span className="text-xs text-slate-400 font-medium">Total Alerts:</span>
        <span className="text-sm font-black text-white">{totalCount}</span>
      </div>

      {/* Critical */}
      <div className="flex items-center gap-2.5 px-3 py-1.5 bg-red-950/40 rounded-lg border border-red-800/60">
        <AlertTriangle className="w-4 h-4 text-red-500 animate-pulse" />
        <span className="text-xs text-red-300 font-medium">Critical:</span>
        <span className="text-sm font-black text-red-400">{criticalCount}</span>
      </div>

      {/* Pending */}
      <div className="flex items-center gap-2.5 px-3 py-1.5 bg-amber-950/30 rounded-lg border border-amber-800/50">
        <Clock className="w-4 h-4 text-amber-400" />
        <span className="text-xs text-amber-300 font-medium">Pending:</span>
        <span className="text-sm font-black text-amber-400">{pendingCount}</span>
      </div>

      {/* Dispatched */}
      <div className="flex items-center gap-2.5 px-3 py-1.5 bg-blue-950/30 rounded-lg border border-blue-800/50">
        <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping"></span>
        <span className="text-xs text-blue-300 font-medium">Dispatched:</span>
        <span className="text-sm font-black text-blue-400">{dispatchedCount}</span>
      </div>

      {/* Rescued (Compact Badge) */}
      <div className="flex items-center gap-2.5 px-3 py-1.5 bg-emerald-950/30 rounded-lg border border-emerald-800/50">
        <CheckCircle2 className="w-4 h-4 text-emerald-400" />
        <span className="text-xs text-emerald-300 font-medium">Rescued Archive:</span>
        <span className="text-sm font-black text-emerald-400">{rescuedCount}</span>
      </div>
    </div>
  );
};

export default StatsBar;
