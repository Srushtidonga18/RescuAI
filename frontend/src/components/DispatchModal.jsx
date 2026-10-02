import React from 'react';
import { X, Printer, ShieldAlert, MapPin, Users, Activity, Truck } from 'lucide-react';

const DispatchModal = ({ isOpen, onClose, sosData, dispatchData }) => {
  if (!isOpen || !sosData) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-white border border-slate-300 rounded-3xl w-full max-w-2xl overflow-hidden shadow-2xl relative text-slate-900">
        {/* Header Bar */}
        <div className="bg-slate-900 text-white px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-red-600 rounded-xl text-white">
              <ShieldAlert className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-extrabold text-base tracking-tight">FIELD RESCUE DISPATCH CARD</h3>
              <p className="text-xs text-slate-400 font-mono">ID: {sosData.id}</p>
            </div>
          </div>
          <div className="flex items-center gap-2 print:hidden">
            <button
              onClick={handlePrint}
              className="px-3.5 py-1.5 bg-red-600 hover:bg-red-500 text-white rounded-xl text-xs font-bold flex items-center gap-1.5 transition-colors shadow-sm"
            >
              <Printer className="w-4 h-4" />
              <span>Print Card</span>
            </button>
            <button
              onClick={onClose}
              className="p-1.5 text-slate-400 hover:text-white hover:bg-slate-800 rounded-xl transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Printable Card Area */}
        <div id="printable-dispatch-card" className="p-6 space-y-6">
          {/* Status & Priority Ribbon */}
          <div className="flex items-center justify-between p-4 bg-slate-100 rounded-2xl border border-slate-200">
            <div>
              <span className="text-xs font-bold text-slate-500 uppercase block">Urgency Status</span>
              <span className={`text-base font-black uppercase ${sosData.urgency_level === 'CRITICAL' ? 'text-red-600' : 'text-amber-600'}`}>
                {sosData.urgency_level} PRIORITY
              </span>
            </div>
            <div>
              <span className="text-xs font-bold text-slate-500 uppercase block">Category</span>
              <span className="text-sm font-bold text-slate-900">{sosData.category}</span>
            </div>
            <div>
              <span className="text-xs font-bold text-slate-500 uppercase block">Trapped Count</span>
              <span className="text-sm font-bold text-slate-900 flex items-center gap-1">
                <Users className="w-4 h-4 text-red-600 inline" />
                {sosData.trapped_count} Persons
              </span>
            </div>
          </div>

          {/* Location & Coordinates */}
          <div className="p-4 bg-red-50 border border-red-200 rounded-2xl">
            <div className="flex items-start gap-2.5">
              <MapPin className="w-5 h-5 text-red-600 shrink-0 mt-0.5" />
              <div>
                <strong className="text-xs font-bold text-red-900 uppercase block">Extracted Location Landmark</strong>
                <p className="text-base font-extrabold text-slate-900 mt-0.5">
                  {sosData.extracted_location}
                </p>
                {sosData.latitude && sosData.longitude && (
                  <p className="text-xs font-mono text-slate-600 mt-1">
                    GPS Coordinates: {sosData.latitude.toFixed(5)}, {sosData.longitude.toFixed(5)}
                  </p>
                )}
              </div>
            </div>
          </div>

          {/* Medical Details */}
          {sosData.medical_details && (
            <div className="p-4 bg-amber-50 border border-amber-200 rounded-2xl">
              <div className="flex items-start gap-2.5">
                <Activity className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                <div>
                  <strong className="text-xs font-bold text-amber-900 uppercase block">Medical / Special Risk Details</strong>
                  <p className="text-sm font-semibold text-slate-900 mt-0.5">
                    {sosData.medical_details}
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Dynamic AI Operational Plan */}
          <div className="p-4 bg-slate-900 text-white rounded-2xl">
            <strong className="text-xs font-bold text-red-400 uppercase block mb-1">
              AI Operational Dispatch Guide
            </strong>
            <p className="text-sm font-medium leading-relaxed text-slate-200">
              {sosData.action_summary}
            </p>
          </div>

          {/* Logistics & Equipment */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl">
              <span className="font-bold text-slate-500 uppercase block mb-1">Assigned Team</span>
              <span className="font-extrabold text-sm text-slate-900 flex items-center gap-1.5">
                <Truck className="w-4 h-4 text-red-600" />
                {dispatchData?.assigned_team || 'Pending Team Assignment'}
              </span>
            </div>

            <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl">
              <span className="font-bold text-slate-500 uppercase block mb-1">Required Equipment</span>
              <span className="font-semibold text-slate-900">
                {dispatchData?.supplies_needed || 'Disaster Relief & Medical Equipment'}
              </span>
            </div>
          </div>

          {/* Footer Warning */}
          <div className="text-center pt-2 border-t border-slate-200">
            <p className="text-[11px] text-slate-500 font-mono">
              Generated by RescuAI Real-Time Dispatcher | National Helplines: 112 / 108
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DispatchModal;
