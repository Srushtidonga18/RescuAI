import React, { useState } from 'react';
import { Send, MapPin, Mic, FileText, AlertTriangle, CheckCircle2, ShieldAlert, Sparkles, Navigation, PackageCheck } from 'lucide-react';
import api from '../api/axios';
import AudioRecorder from './AudioRecorder';

const CitizenSOS = () => {
  const [activeMode, setActiveMode] = useState('text'); // 'text' or 'audio'
  const [rawText, setRawText] = useState('');
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [locationStatus, setLocationStatus] = useState('');
  const [audioBlob, setAudioBlob] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  // GPS Location Handler
  const handleDetectLocation = () => {
    if (!navigator.geolocation) {
      setLocationStatus('Geolocation is not supported by your browser.');
      return;
    }
    setLocationStatus('Detecting GPS coordinates...');
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLatitude(position.coords.latitude);
        setLongitude(position.coords.longitude);
        setLocationStatus(`GPS Detected: ${position.coords.latitude.toFixed(4)}, ${position.coords.longitude.toFixed(4)}`);
      },
      (err) => {
        console.error(err);
        setLocationStatus('Unable to retrieve location automatically. Landmark text will be parsed.');
      }
    );
  };

  // Text SOS Submit
  const handleTextSubmit = async (e) => {
    e.preventDefault();
    if (!rawText.trim()) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await api.post('/api/v1/sos/text', {
        raw_text: rawText,
        latitude: latitude,
        longitude: longitude,
      });
      setResult(response.data);
      setRawText('');
    } catch (err) {
      console.error('Submit error:', err);
      setError(err.response?.data?.detail || 'Failed to transmit distress signal. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Audio SOS Submit
  const handleAudioSubmit = async () => {
    if (!audioBlob) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      formData.append('file', audioBlob, 'sos_audio.webm');
      if (latitude) formData.append('latitude', latitude);
      if (longitude) formData.append('longitude', longitude);

      const response = await api.post('/api/v1/sos/audio', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
      setAudioBlob(null);
    } catch (err) {
      console.error('Audio submit error:', err);
      setError(err.response?.data?.detail || 'Failed to process voice SOS. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getUrgencyBadge = (level) => {
    switch (level) {
      case 'CRITICAL':
        return 'bg-red-600 text-white shadow-md shadow-red-600/30 border-red-500';
      case 'MODERATE':
        return 'bg-amber-500 text-slate-950 font-bold border-amber-400';
      default:
        return 'bg-emerald-600 text-white border-emerald-500';
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header Banner */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center gap-2 bg-red-600/10 border border-red-500/20 text-red-500 px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider mb-3">
          <ShieldAlert className="w-4 h-4" />
          <span>Emergency Citizen Portal</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-black text-slate-900 tracking-tight">
          Submit Emergency SOS Alert
        </h1>
        <p className="text-sm text-slate-600 mt-2 max-w-xl mx-auto">
          Generative AI instantly analyzes your distress call, extracts landmarks, quantifies victims, and alerts rescue teams within seconds.
        </p>
      </div>

      {/* Main Form Container */}
      <div className="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-xl shadow-slate-200/50 relative overflow-hidden">
        {/* Decorative Top Accent Bar */}
        <div className="absolute top-0 left-0 right-0 h-2 bg-gradient-to-r from-red-600 via-amber-500 to-emerald-600"></div>

        {/* Tab Switcher: Text vs Audio */}
        <div className="flex rounded-2xl bg-slate-100 p-1.5 mb-6">
          <button
            type="button"
            onClick={() => {
              setActiveMode('text');
              setResult(null);
            }}
            className={`flex-1 py-3 px-4 rounded-xl text-sm font-bold flex items-center justify-center gap-2 transition-all ${
              activeMode === 'text'
                ? 'bg-white text-slate-900 shadow-md shadow-slate-200'
                : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            <FileText className="w-4 h-4 text-red-600" />
            <span>Text Distress Message</span>
          </button>
          <button
            type="button"
            onClick={() => {
              setActiveMode('audio');
              setResult(null);
            }}
            className={`flex-1 py-3 px-4 rounded-xl text-sm font-bold flex items-center justify-center gap-2 transition-all ${
              activeMode === 'audio'
                ? 'bg-white text-slate-900 shadow-md shadow-slate-200'
                : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            <Mic className="w-4 h-4 text-red-600" />
            <span>Voice Recording SOS</span>
          </button>
        </div>

        {/* GPS Location Bar */}
        <div className="mb-6 p-4 bg-slate-50 border border-slate-200 rounded-2xl flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2.5 text-xs text-slate-700 font-medium">
            <MapPin className="w-4 h-4 text-red-600 shrink-0" />
            <span>{locationStatus || 'Optional: Attach current GPS coordinates for pinpoint dispatch.'}</span>
          </div>
          <button
            type="button"
            onClick={handleDetectLocation}
            className="px-3 py-1.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-semibold flex items-center gap-1.5 transition-colors shadow-sm"
          >
            <Navigation className="w-3.5 h-3.5 text-amber-400" />
            <span>Detect GPS</span>
          </button>
        </div>

        {/* Error Notification */}
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-2xl text-xs text-red-600 font-medium flex items-center gap-3">
            <AlertTriangle className="w-5 h-5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* MODE 1: TEXT SOS FORM */}
        {activeMode === 'text' && (
          <form onSubmit={handleTextSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
                Describe Your Emergency (Any Language / Dialect)
              </label>
              <textarea
                required
                rows={5}
                value={rawText}
                onChange={(e) => setRawText(e.target.value)}
                placeholder="Example: We are safe on 2nd floor at Sunshine Apartments, Civil Lines. Need baby milk powder, food for 2 kids and drinking water."
                className="w-full bg-slate-50 border border-slate-300 rounded-2xl p-4 text-sm text-slate-900 placeholder-slate-400 focus:outline-none focus:border-red-500 focus:ring-2 focus:ring-red-500/20 transition-all"
              />
            </div>

            <button
              type="submit"
              disabled={loading || !rawText.trim()}
              className="w-full py-4 bg-red-600 hover:bg-red-500 disabled:opacity-50 text-white font-extrabold rounded-2xl shadow-xl shadow-red-600/30 transition-all flex items-center justify-center gap-2 text-base"
            >
              {loading ? (
                <div className="flex items-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Transmitting & AI Triaging...</span>
                </div>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span>DISPATCH EMERGENCY ALERT NOW</span>
                </>
              )}
            </button>
          </form>
        )}

        {/* MODE 2: VOICE AUDIO SOS FORM */}
        {activeMode === 'audio' && (
          <div className="space-y-6">
            <AudioRecorder
              onAudioCaptured={(blob) => setAudioBlob(blob)}
              onReset={() => setAudioBlob(null)}
            />

            <button
              type="button"
              onClick={handleAudioSubmit}
              disabled={loading || !audioBlob}
              className="w-full py-4 bg-red-600 hover:bg-red-500 disabled:opacity-50 text-white font-extrabold rounded-2xl shadow-xl shadow-red-600/30 transition-all flex items-center justify-center gap-2 text-base"
            >
              {loading ? (
                <div className="flex items-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Processing Voice Note with Gemini AI...</span>
                </div>
              ) : (
                <>
                  <Mic className="w-5 h-5" />
                  <span>TRANSMIT VOICE DISTRESS SIGNAL</span>
                </>
              )}
            </button>
          </div>
        )}

        {/* SUCCESS RESULT CARD (DYNAMIC TRIAGE PREVIEW) */}
        {result && (
          <div className="mt-8 p-6 bg-slate-900 text-white rounded-3xl border border-slate-800 shadow-2xl animate-fade-in relative overflow-hidden">
            <div className="flex items-center justify-between gap-4 mb-4 pb-4 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <div className="p-2.5 bg-emerald-500/20 text-emerald-400 rounded-xl border border-emerald-500/30">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="font-bold text-lg text-white">SOS Dispatch Card Created</h3>
                  <p className="text-xs text-slate-400 font-mono">ID: {result.id}</p>
                </div>
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-black uppercase tracking-wider border ${getUrgencyBadge(result.urgency_level)}`}>
                {result.urgency_level} URGENCY
              </span>
            </div>

            {/* Extracted Details Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
              <div className="bg-slate-800/80 p-3.5 rounded-xl border border-slate-700/60">
                <span className="text-slate-400 block text-[10px] uppercase font-bold mb-1">Landmark / Location</span>
                <span className="font-semibold text-white text-sm">{result.extracted_location || 'Unknown Landmark'}</span>
              </div>

              <div className="bg-slate-800/80 p-3.5 rounded-xl border border-slate-700/60">
                <span className="text-slate-400 block text-[10px] uppercase font-bold mb-1">Category & Headcount</span>
                <span className="font-semibold text-white text-sm">{result.category} ({result.trapped_count} Persons)</span>
              </div>
            </div>

            {/* Medical / Special Needs if extracted */}
            {result.medical_details && (
              <div className="mt-3 p-3.5 bg-amber-500/10 border border-amber-500/20 rounded-xl text-xs text-amber-300">
                <span className="text-[10px] font-bold uppercase block text-amber-400 mb-0.5">Special Need / Medical Note</span>
                <p className="font-medium text-amber-200">{result.medical_details}</p>
              </div>
            )}

            {/* Dynamic AI Operational Action Plan */}
            <div className="mt-4 bg-red-600/10 border border-red-500/30 p-4 rounded-2xl">
              <div className="flex items-center gap-1.5 text-red-400 font-bold text-xs uppercase mb-1">
                <Sparkles className="w-4 h-4" />
                <span>Tailored Operational Action Guide</span>
              </div>
              <p className="text-sm text-slate-200 font-medium leading-relaxed">
                {result.action_summary || 'Dispatch team assigned to location.'}
              </p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CitizenSOS;
