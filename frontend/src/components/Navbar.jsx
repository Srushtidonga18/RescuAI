import React, { useContext } from 'react';
import { ShieldAlert, PhoneCall, Lock, LogOut, LayoutDashboard, Send } from 'lucide-react';
import { AuthContext } from '../context/AuthContext';

const Navbar = ({ currentTab, setCurrentTab, onOpenLogin }) => {
  const { isAuthenticated, logout, user } = useContext(AuthContext);

  return (
    <header className="bg-slate-900 text-white sticky top-0 z-40 border-b border-slate-800 shadow-lg">
      {/* Emergency Helpline Banner */}
      <div className="bg-red-600 px-4 py-1 text-xs md:text-sm font-semibold flex items-center justify-between text-white">
        <div className="flex items-center gap-2">
          <PhoneCall className="w-4 h-4 animate-bounce" />
          <span>NATIONAL DISASTER HELPLINE: <strong>112</strong> | EMERGENCY AI TRIAGE LIVE</span>
        </div>
        <div className="hidden sm:flex items-center gap-4 text-xs opacity-90">
          <span>24x7 Real-Time Automated Response</span>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-mx px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between mx-auto">
        {/* Brand Logo */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => setCurrentTab('citizen')}>
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-red-600 text-white shadow-md shadow-red-600/30">
            <ShieldAlert className="w-6 h-6" />
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-400 rounded-full animate-ping"></span>
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="text-xl font-black tracking-tight text-white">Rescu<span className="text-red-500">AI</span></span>
              <span className="text-[10px] font-bold bg-slate-800 text-red-400 px-1.5 py-0.5 rounded border border-slate-700">PRO</span>
            </div>
            <p className="text-[11px] text-slate-400 font-medium">Disaster Triage & SOS Aggregator</p>
          </div>
        </div>

        {/* Tab Switcher & User Actions */}
        <div className="flex items-center gap-2 sm:gap-3">
          <button
            onClick={() => setCurrentTab('citizen')}
            className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
              currentTab === 'citizen'
                ? 'bg-red-600 text-white shadow-md shadow-red-600/20'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white'
            }`}
          >
            <Send className="w-4 h-4" />
            <span className="hidden sm:inline">Submit SOS</span>
          </button>

          <button
            onClick={() => {
              if (isAuthenticated) {
                setCurrentTab('responder');
              } else {
                onOpenLogin();
              }
            }}
            className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all ${
              currentTab === 'responder'
                ? 'bg-red-600 text-white shadow-md shadow-red-600/20'
                : 'text-slate-300 hover:bg-slate-800 hover:text-white border border-slate-700'
            }`}
          >
            <LayoutDashboard className="w-4 h-4 text-amber-400" />
            <span className="hidden sm:inline">Command Dashboard</span>
          </button>

          {isAuthenticated ? (
            <div className="flex items-center gap-2 border-l border-slate-800 pl-3 ml-1">
              <span className="hidden lg:inline text-xs text-slate-400 font-mono">
                {user?.email || 'Responder'}
              </span>
              <button
                onClick={logout}
                title="Logout"
                className="p-2 rounded-lg text-slate-400 hover:text-red-400 hover:bg-slate-800 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={onOpenLogin}
              className="flex items-center gap-1.5 px-3 py-2 text-xs font-semibold text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-lg border border-slate-700 transition-colors ml-1"
            >
              <Lock className="w-3.5 h-3.5 text-amber-400" />
              <span>Login</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Navbar;
