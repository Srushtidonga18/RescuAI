import React, { useState } from 'react';
import { MessageCircle, X, Send, HeartPulse } from 'lucide-react';
import api from '../api/axios';

const FirstAidChatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [chatHistory, setChatHistory] = useState([
    { sender: 'bot', text: 'Hello! I am your AI First Aid Assistant. Describe the medical emergency or symptoms, and I will provide immediate guidance.' }
  ]);
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    const userMessage = { sender: 'user', text: query };
    setChatHistory((prev) => [...prev, userMessage]);
    setQuery('');
    setLoading(true);

    try {
      const response = await api.post('/api/v1/sos/first-aid', { query: userMessage.text });
      const botMessage = { sender: 'bot', text: response.data.response || response.data.instructions || 'Sorry, I could not process that.' };
      setChatHistory((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Chatbot error:', error);
      const errorMessage = { sender: 'bot', text: 'Failed to connect to First Aid Service. Please try again or seek professional help immediately.' };
      setChatHistory((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 p-4 bg-red-600 hover:bg-red-500 text-white rounded-full shadow-2xl transition-all z-50 flex items-center justify-center"
          title="AI First Aid Assistant"
        >
          <HeartPulse className="w-6 h-6 animate-pulse" />
        </button>
      )}

      {isOpen && (
        <div className="fixed bottom-6 right-6 w-80 sm:w-96 bg-white border border-slate-200 rounded-2xl shadow-2xl z-50 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-red-600 p-4 text-white flex items-center justify-between">
            <div className="flex items-center gap-2">
              <HeartPulse className="w-5 h-5" />
              <h3 className="font-bold text-sm">AI First Aid Assistant</h3>
            </div>
            <button onClick={() => setIsOpen(false)} className="text-white hover:text-red-200">
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Chat Body */}
          <div className="h-80 p-4 overflow-y-auto bg-slate-50 flex flex-col gap-3">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`max-w-[85%] p-3 rounded-xl text-sm ${msg.sender === 'user' ? 'bg-red-600 text-white self-end rounded-br-sm' : 'bg-white border border-slate-200 text-slate-800 self-start rounded-bl-sm shadow-sm'}`}>
                {msg.text}
              </div>
            ))}
            {loading && (
              <div className="max-w-[85%] p-3 bg-white border border-slate-200 rounded-xl rounded-bl-sm self-start text-sm text-slate-500 shadow-sm flex items-center gap-2">
                <div className="w-3 h-3 border-2 border-red-600 border-t-transparent rounded-full animate-spin"></div>
                Thinking...
              </div>
            )}
          </div>

          {/* Input Area */}
          <form onSubmit={handleSend} className="p-3 bg-white border-t border-slate-200 flex items-center gap-2">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask for first aid advice..."
              className="flex-1 bg-slate-50 border border-slate-200 rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-red-500"
            />
            <button
              type="submit"
              disabled={loading || !query.trim()}
              className="p-2 bg-red-600 hover:bg-red-500 text-white rounded-lg disabled:opacity-50"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      )}
    </>
  );
};

export default FirstAidChatbot;
