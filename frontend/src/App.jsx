import React, { useState, useContext } from 'react';
import { AuthProvider, AuthContext } from './context/AuthContext';
import Navbar from './components/Navbar';
import CitizenSOS from './components/CitizenSOS';
import ResponderDashboard from './components/ResponderDashboard';
import LoginModal from './components/LoginModal';
import FirstAidChatbot from './components/FirstAidChatbot';

const AppContent = () => {
  const [currentTab, setCurrentTab] = useState('citizen'); // 'citizen' or 'responder'
  const [isLoginModalOpen, setIsLoginModalOpen] = useState(false);
  const { isAuthenticated } = useContext(AuthContext);

  const handleOpenLogin = () => {
    setIsLoginModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      {/* Top Navbar */}
      <Navbar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        onOpenLogin={handleOpenLogin}
      />

      {/* Main View Area */}
      <main className="flex-1">
        {currentTab === 'citizen' && <CitizenSOS />}

        {currentTab === 'responder' && (
          isAuthenticated ? (
            <ResponderDashboard />
          ) : (
            <div className="max-w-md mx-auto my-16 p-8 bg-white rounded-3xl border border-slate-200 shadow-xl text-center">
              <h2 className="text-xl font-bold text-slate-900 mb-2">Responder Access Required</h2>
              <p className="text-xs text-slate-500 mb-6">
                Please log in with emergency responder credentials to view the live command center dashboard.
              </p>
              <button
                onClick={handleOpenLogin}
                className="w-full py-3 bg-red-600 hover:bg-red-500 text-white font-bold rounded-xl shadow-lg shadow-red-600/30 transition-all text-sm"
              >
                Log In to Command Center
              </button>
            </div>
          )
        )}
      </main>

      {/* Login Modal */}
      <LoginModal
        isOpen={isLoginModalOpen}
        onClose={() => setIsLoginModalOpen(false)}
        onSuccess={() => setCurrentTab('responder')}
      />

      {/* Floating First Aid Chatbot */}
      <FirstAidChatbot />

      {/* Footer */}
      <footer className="bg-slate-900 text-slate-400 py-6 text-center text-xs border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4">
          <p className="font-semibold text-slate-300">RescuAI — Emergency SOS Aggregator & AI Triage System</p>
          <p className="text-[11px] text-slate-500 mt-1">Built with FastAPI, Google Gemini 1.5/3.8 Flash, React & Tailwind CSS | National Helplines: 112 / 108</p>
        </div>
      </footer>
    </div>
  );
};

const App = () => {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
};

export default App;
