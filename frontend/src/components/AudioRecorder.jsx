import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, RotateCcw, AlertTriangle, CheckCircle2 } from 'lucide-react';

const AudioRecorder = ({ onAudioCaptured, onReset }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioUrl, setAudioUrl] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [permissionError, setPermissionError] = useState(null);

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const startRecording = async () => {
    setPermissionError(null);
    audioChunksRef.current = [];
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const url = URL.createObjectURL(blob);
        setAudioBlob(blob);
        setAudioUrl(url);
        onAudioCaptured(blob);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingTime(0);

      timerRef.current = setInterval(() => {
        setRecordingTime((prev) => prev + 1);
      }, 1000);
    } catch (err) {
      console.error('Microphone error:', err);
      setPermissionError('Microphone access denied or unavailable. Please enable microphone permissions.');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      // Stop all tracks in the stream
      mediaRecorderRef.current.stream.getTracks().forEach((track) => track.stop());
      setIsRecording(false);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  const handleReset = () => {
    setAudioUrl(null);
    setAudioBlob(null);
    setRecordingTime(0);
    onReset();
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 text-center shadow-inner">
      {permissionError && (
        <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-xl text-xs text-red-400 flex items-center justify-center gap-2">
          <AlertTriangle className="w-4 h-4" />
          <span>{permissionError}</span>
        </div>
      )}

      {!audioUrl ? (
        <div className="flex flex-col items-center justify-center py-4">
          {isRecording ? (
            <div className="space-y-4">
              {/* Pulse Waveform Visualizer */}
              <div className="relative flex items-center justify-center">
                <div className="w-24 h-24 rounded-full bg-red-600/30 animate-ping absolute"></div>
                <div className="w-20 h-20 rounded-full bg-red-600/50 animate-pulse absolute"></div>
                <button
                  type="button"
                  onClick={stopRecording}
                  className="relative z-10 w-16 h-16 rounded-full bg-red-600 text-white flex items-center justify-center shadow-lg shadow-red-600/50 hover:bg-red-700 transition-transform transform active:scale-95"
                >
                  <Square className="w-8 h-8 fill-current" />
                </button>
              </div>

              <div className="text-center">
                <span className="inline-block bg-red-600/20 text-red-400 px-3 py-1 rounded-full text-xs font-mono font-bold border border-red-500/30 animate-pulse">
                  ● REC {formatTime(recordingTime)}
                </span>
                <p className="text-xs text-slate-400 mt-2">Speak clearly into microphone. Click stop when finished.</p>
              </div>
            </div>
          ) : (
            <div className="space-y-3">
              <button
                type="button"
                onClick={startRecording}
                className="w-20 h-20 rounded-full bg-red-600 hover:bg-red-500 text-white flex items-center justify-center shadow-xl shadow-red-600/30 hover:scale-105 transition-all mx-auto group"
              >
                <Mic className="w-9 h-9 group-hover:animate-bounce" />
              </button>
              <div>
                <p className="text-sm font-bold text-white">Record Audio Distress Message</p>
                <p className="text-xs text-slate-400">Supported formats: Multilingual Voice Notes (.webm/.mp3)</p>
              </div>
            </div>
          )}
        </div>
      ) : (
        <div className="space-y-4 py-2">
          <div className="flex items-center justify-center gap-2 text-emerald-400 font-semibold text-sm">
            <CheckCircle2 className="w-5 h-5" />
            <span>Voice SOS Recorded ({formatTime(recordingTime)})</span>
          </div>

          {/* Audio Playback Element */}
          <audio controls src={audioUrl} className="w-full max-w-md mx-auto rounded-lg" />

          <button
            type="button"
            onClick={handleReset}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-medium transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Re-record Audio</span>
          </button>
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;
