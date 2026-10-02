import React, { useState } from 'react';
import { MapPin, Users, Activity, FileSpreadsheet, ChevronDown, ChevronUp, CheckCircle2, Truck, Copy, Check, Volume2 } from 'lucide-react';
import api from '../api/axios';

const SOSCard = ({ item, onStatusUpdated, onViewDispatchCard }) => {
  const [expanded, setExpanded] = useState(false);
  const [updating, setUpdating] = useState(false);
  const [copied, setCopied] = useState(false);

  const getBorderColor = (urgency) => {
    switch (urgency) {
      case 'CRITICAL':
        return 'border-l-red-600 border-l-4';
      case 'MODERATE':
        return 'border-l-amber-500 border-l-4';
      default:
        return 'border-l-emerald-600 border-l-4';
    }
  };

  const getUrgencyBadge = (urgency) => {
    switch (urgency) {
      case 'CRITICAL':
        return 'bg-red-600 text-white shadow-sm';
      case 'MODERATE':
        return 'bg-amber-500 text-slate-950 font-bold';
      default:
        return 'bg-emerald-600 text-white';
    }
  };

  const getStatusBadge = (status) => {
    switch (status) {
      case 'RESCUED':
        return 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30';
      case 'DISPATCHED':
        return 'bg-blue-500/15 text-blue-400 border-blue-500/30';
      default:
        return 'bg-amber-500/15 text-amber-400 border-amber-500/30';
    }
  };

  const handleStatusChange = async (newStatus) => {
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
  };

  const handleCopyLocation = () => {
    if (item.extracted_location) {
      navigator.clipboard.writeText(item.extracted_location);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const formattedDate = item.created_at
    ? new Date(item.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : 'Just now';

  return (
    <div className={`bg-slate-900 border border-slate-800 rounded-xl p-3.5 text-white shadow-md transition-all hover:border-slate-700 ${getBorderColor(item.urgency_level)}`}>
      {/* Top Header Row */}
      <div className="flex items-center justify-between gap-2 mb-2">
        <div className="flex items-center gap-1.5">
          <span className={`px-2 py-0.5 rounded text-[11px] font-black uppercase tracking-wider ${getUrgencyBadge(item.urgency_level)}`}>
            {item.urgency_level}
          </span>
          <span className="text-[11px] text-slate-400 font-mono">
            {item.input_type} • {formattedDate}
          </span>
        </div>

        <div className="flex items-center gap-1">
          <span className={`px-2 py-0.5 rounded text-[11px] font-bold border ${getStatusBadge(item.status)}`}>
            {item.status}
          </span>
        </div>
      </div>

      {/* Location Landmark Bar */}
      <div className="flex items-start justify-between gap-2 mb-2">
        <h4 className="text-sm font-bold text-white flex items-center gap-1.5 leading-snug">
          <MapPin className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
          <span className="line-clamp-1">{item.extracted_location}</span>
        </h4>
        <button
          onClick={handleCopyLocation}
          title="Copy Landmark to Clipboard"
          className="p-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-[10px] flex items-center gap-1 shrink-0 transition-colors"
        >
          {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
          <span>{copied ? 'Copied' : 'Copy'}</span>
        </button>
      </div>

      {/* Meta Badges */}
      <div className="flex items-center gap-3 text-[11px] text-slate-300 mb-2 bg-slate-800/60 p-1.5 rounded-lg border border-slate-800">
        <span className="flex items-center gap-1 font-semibold">
          <Users className="w-3.5 h-3.5 text-amber-400" />
          {item.trapped_count} Victim(s)
        </span>
        <span className="text-slate-500">|</span>
        <span className="font-semibold text-slate-300">Category: {item.category}</span>
      </div>

      {/* Medical Risk Note if present */}
      {item.medical_details && (
        <div className="mb-2 p-2 bg-amber-500/10 border border-amber-500/20 rounded-lg text-[11px] text-amber-300 flex items-center gap-1.5">
          <Activity className="w-3.5 h-3.5 shrink-0 text-amber-400" />
          <span className="line-clamp-1 font-medium">{item.medical_details}</span>
        </div>
      )}

      {/* AI Operational Action Plan */}
      <div className="p-2.5 bg-slate-800/90 rounded-lg border border-slate-700/60 mb-3 text-xs">
        <span className="text-[10px] font-bold text-red-400 uppercase block mb-0.5">Dynamic AI Action Plan</span>
        <p className="text-slate-200 font-medium leading-normal text-[11px]">
          {item.action_summary}
        </p>
      </div>

      {/* Audio Player if Audio SOS */}
      {item.input_type === 'AUDIO' && item.audio_file_path && (
        <div className="mb-3 p-2 bg-slate-950 rounded-lg border border-slate-800 flex items-center gap-2 text-xs">
          <Volume2 className="w-4 h-4 text-amber-400 shrink-0" />
          <span className="text-[11px] text-slate-400 font-mono">Audio SOS Recording</span>
        </div>
      )}

      {/* Expandable Transcript */}
      {expanded && (
        <div className="mb-3 p-2.5 bg-slate-950 rounded-lg border border-slate-800 text-[11px] text-slate-300 space-y-1 animate-fade-in">
          <strong className="text-slate-400 block text-[10px] uppercase font-bold">Raw SOS Message:</strong>
          <p className="text-slate-200 italic font-mono">"{item.transcribed_text || item.raw_text}"</p>
        </div>
      )}

      {/* Card Action Buttons */}
      <div className="flex items-center justify-between gap-1.5 pt-2 border-t border-slate-800">
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-[11px] text-slate-400 hover:text-white flex items-center gap-0.5 font-medium transition-colors"
        >
          {expanded ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
          <span>{expanded ? 'Less' : 'Transcript'}</span>
        </button>

        <div className="flex items-center gap-1.5">
          <button
            onClick={() => onViewDispatchCard(item)}
            className="px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-white rounded text-[11px] font-semibold flex items-center gap-1 transition-colors border border-slate-700"
          >
            <FileSpreadsheet className="w-3 h-3 text-amber-400" />
            <span>Card</span>
          </button>

          {item.status === 'PENDING' && (
            <button
              disabled={updating}
              onClick={() => handleStatusChange('DISPATCHED')}
              className="px-2.5 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-[11px] font-bold transition-colors shadow-sm flex items-center gap-1"
            >
              <Truck className="w-3 h-3" />
              <span>Dispatch</span>
            </button>
          )}

          {item.status === 'DISPATCHED' && (
            <button
              disabled={updating}
              onClick={() => handleStatusChange('RESCUED')}
              className="px-2.5 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[11px] font-bold transition-colors shadow-sm flex items-center gap-1"
            >
              <CheckCircle2 className="w-3 h-3" />
              <span>Rescued</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default SOSCard;
