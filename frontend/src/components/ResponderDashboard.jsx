import React, { useState, useEffect, useCallback, useContext } from 'react';
import { Search, Filter, RefreshCw, LayoutDashboard, AlertCircle, LayoutGrid, Table, CheckCircle2, ShieldAlert, Truck, Copy, Check, FileSpreadsheet } from 'lucide-react';
import api from '../api/axios';
import { AuthContext } from '../context/AuthContext';
import StatsBar from './StatsBar';
import SOSCard from './SOSCard';
import DispatchModal from './DispatchModal';

const ResponderDashboard = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Tab View: 'active' (PENDING + DISPATCHED) vs 'rescued' (RESCUED ARCHIVE)
  const [activeTab, setActiveTab] = useState('active');

  // Display Mode: 'grid' vs 'table'
  const [viewMode, setViewMode] = useState('grid');

  // Filters & Search
  const [searchLocation, setSearchLocation] = useState('');
  const [urgencyFilter, setUrgencyFilter] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [autoRefresh, setAutoRefresh] = useState(true);

  // Dispatch Modal State
  const [selectedSOS, setSelectedSOS] = useState(null);
  const [dispatchCardData, setDispatchCardData] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [copiedId, setCopiedId] = useState(null);

  const { token } = useContext(AuthContext);

  const fetchDashboardData = useCallback(async () => {
    if (!token) return;
    try {
      setError(null);
      const params = {};
      if (urgencyFilter) params.urgency = urgencyFilter;
      if (categoryFilter) params.category = categoryFilter;
      if (searchLocation) params.search_location = searchLocation;

      const response = await api.get('/api/v1/responder/dashboard', { params });
      setItems(response.data);
    } catch (err) {
      console.error('Dashboard error:', err);
      setError(err.response?.data?.detail || 'Failed to fetch responder emergency queue.');
    } finally {
      setLoading(false);
    }
  }, [token, urgencyFilter, categoryFilter, searchLocation]);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  // Auto-refresh interval (every 10 seconds)
  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      fetchDashboardData();
    }, 10000);
    return () => clearInterval(interval);
  }, [autoRefresh, fetchDashboardData]);

  // Filter items based on activeTab (active queue excludes RESCUED by default)
  const displayedItems = items.filter((item) => {
    if (activeTab === 'active') {
      return item.status === 'PENDING' || item.status === 'DISPATCHED';
    } else {
      return item.status === 'RESCUED';
    }
  });

  const handleViewDispatchCard = async (sosItem) => {
    setSelectedSOS(sosItem);
    setIsModalOpen(true);

    try {
      const response = await api.get(`/api/v1/responder/sos/${sosItem.id}/dispatch-card`);
      setDispatchCardData(response.data);
    } catch (err) {
      console.error('Fetch card error:', err);
      setDispatchCardData({
        assigned_team: 'Pending Team Assignment',
        supplies_needed: 'Disaster Relief & Medical Equipment',
        notes: sosItem.action_summary,
      });
    }
  };

  const handleStatusChange = async (sosId, newStatus) => {
    try {
      await api.patch(`/api/v1/responder/sos/${sosId}/status`, {
        status: newStatus,
        assigned_team: 'Alpha Rescue Squad',
      });
      fetchDashboardData();
    } catch (err) {
      console.error('Status update failed:', err);
    }
  };

  const handleCopyLandmark = (landmark, id) => {
    navigator.clipboard.writeText(landmark);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      {/* Top Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
        <div>
          <div className="flex items-center gap-2">
            <LayoutDashboard className="w-5 h-5 text-red-500" />
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              Emergency Command Center
            </h1>
          </div>
          <p className="text-xs text-slate-500 font-medium mt-0.5">
            Real-Time Disaster Triage & Field Rescue Dispatch Center
          </p>
        </div>

        {/* View Switchers & Controls */}
        <div className="flex items-center gap-2">
          {/* Tab Selection: Active Queue vs Rescued Archive */}
          <div className="flex rounded-lg bg-slate-200 p-1 text-xs font-bold">
            <button
              onClick={() => setActiveTab('active')}
              className={`px-3 py-1 rounded-md flex items-center gap-1.5 transition-all ${
                activeTab === 'active'
                  ? 'bg-slate-900 text-white shadow'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <ShieldAlert className="w-3.5 h-3.5 text-red-400" />
              <span>Active Queue ({items.filter(i => i.status !== 'RESCUED').length})</span>
            </button>
            <button
              onClick={() => setActiveTab('rescued')}
              className={`px-3 py-1 rounded-md flex items-center gap-1.5 transition-all ${
                activeTab === 'rescued'
                  ? 'bg-emerald-700 text-white shadow'
                  : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-300" />
              <span>Rescued Archive ({items.filter(i => i.status === 'RESCUED').length})</span>
            </button>
          </div>

          {/* Grid vs Table View Mode */}
          <div className="hidden sm:flex rounded-lg bg-slate-200 p-1 text-xs font-bold">
            <button
              onClick={() => setViewMode('grid')}
              title="Compact Cards Grid"
              className={`p-1.5 rounded-md transition-all ${
                viewMode === 'grid' ? 'bg-white text-slate-900 shadow' : 'text-slate-500'
              }`}
            >
              <LayoutGrid className="w-4 h-4" />
            </button>
            <button
              onClick={() => setViewMode('table')}
              title="Tactical Data Table"
              className={`p-1.5 rounded-md transition-all ${
                viewMode === 'table' ? 'bg-white text-slate-900 shadow' : 'text-slate-500'
              }`}
            >
              <Table className="w-4 h-4" />
            </button>
          </div>

          {/* Auto Refresh Toggle */}
          <button
            onClick={() => setAutoRefresh(!autoRefresh)}
            className={`px-2.5 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 border transition-all ${
              autoRefresh
                ? 'bg-emerald-500/10 text-emerald-700 border-emerald-500/30'
                : 'bg-slate-100 text-slate-600 border-slate-300'
            }`}
          >
            <RefreshCw className={`w-3.5 h-3.5 ${autoRefresh ? 'animate-spin' : ''}`} />
            <span className="hidden md:inline">{autoRefresh ? '10s Auto-Poll' : 'Paused'}</span>
          </button>
        </div>
      </div>

      {/* Summary Inline Metrics Banner */}
      <StatsBar allItems={items} />

      {/* Filter and Search Panel */}
      <div className="bg-white border border-slate-200 rounded-xl p-3 shadow-sm mb-5 flex flex-wrap items-center justify-between gap-3">
        {/* Search Input */}
        <div className="relative flex-1 min-w-[200px]">
          <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-slate-400" />
          <input
            type="text"
            value={searchLocation}
            onChange={(e) => setSearchLocation(e.target.value)}
            placeholder="Search location, landmark or sector..."
            className="w-full bg-slate-50 border border-slate-200 rounded-lg py-1.5 pl-8 pr-3 text-xs text-slate-900 placeholder-slate-400 focus:outline-none focus:border-red-500"
          />
        </div>

        {/* Filter Dropdowns */}
        <div className="flex flex-wrap items-center gap-2 text-xs">
          <div className="flex items-center gap-1 font-bold text-slate-500 uppercase text-[10px] mr-1">
            <Filter className="w-3 h-3" />
            <span>Filters:</span>
          </div>

          <select
            value={urgencyFilter}
            onChange={(e) => setUrgencyFilter(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-lg py-1.5 px-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:border-red-500"
          >
            <option value="">All Urgency Levels</option>
            <option value="CRITICAL">🔴 CRITICAL</option>
            <option value="MODERATE">🟡 MODERATE</option>
            <option value="LOW">🟢 LOW</option>
          </select>

          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="bg-slate-50 border border-slate-200 rounded-lg py-1.5 px-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:border-red-500"
          >
            <option value="">All Categories</option>
            <option value="MEDICAL">Medical Emergency</option>
            <option value="TRAPPED">Trapped Victims</option>
            <option value="FOOD_WATER">Food & Water</option>
            <option value="INFANT_ELDERLY">Infant/Elderly Care</option>
            <option value="GENERAL">General Request</option>
          </select>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-5 p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-600 font-medium flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Main Content Area */}
      {loading ? (
        <div className="text-center py-16">
          <div className="w-7 h-7 border-3 border-red-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
          <p className="text-xs font-semibold text-slate-500">Loading emergency queue...</p>
        </div>
      ) : displayedItems.length === 0 ? (
        <div className="bg-white border border-slate-200 rounded-2xl p-10 text-center max-w-md mx-auto my-6 shadow-sm">
          <CheckCircle2 className="w-10 h-10 text-emerald-500 mx-auto mb-2" />
          <h3 className="font-bold text-slate-800 text-sm">
            {activeTab === 'active' ? 'No Active Emergency Queue' : 'No Rescued Records'}
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            {activeTab === 'active'
              ? 'All incoming distress requests have been handled or rescued!'
              : 'Rescued cases will appear here once teams mark them completed.'}
          </p>
        </div>
      ) : viewMode === 'grid' ? (
        /* GRID VIEW (Compact Sleek Cards) */
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {displayedItems.map((item) => (
            <SOSCard
              key={item.id}
              item={item}
              onStatusUpdated={fetchDashboardData}
              onViewDispatchCard={handleViewDispatchCard}
            />
          ))}
        </div>
      ) : (
        /* TABLE VIEW (Tactical Data Table for Responders) */
        <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900 text-white text-[11px] font-bold uppercase tracking-wider">
                <tr>
                  <th className="p-3">Urgency</th>
                  <th className="p-3">Location Landmark</th>
                  <th className="p-3">Category & Victims</th>
                  <th className="p-3">AI Action Summary</th>
                  <th className="p-3">Status</th>
                  <th className="p-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200">
                {displayedItems.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50 transition-colors">
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-black uppercase ${
                        item.urgency_level === 'CRITICAL'
                          ? 'bg-red-600 text-white'
                          : item.urgency_level === 'MODERATE'
                          ? 'bg-amber-500 text-slate-950 font-bold'
                          : 'bg-emerald-600 text-white'
                      }`}>
                        {item.urgency_level}
                      </span>
                    </td>
                    <td className="p-3 font-semibold text-slate-900">
                      <div className="flex items-center gap-1.5">
                        <span>{item.extracted_location}</span>
                        <button
                          onClick={() => handleCopyLandmark(item.extracted_location, item.id)}
                          className="p-1 hover:bg-slate-200 rounded text-slate-500"
                          title="Copy Location"
                        >
                          {copiedId === item.id ? <Check className="w-3 h-3 text-emerald-600" /> : <Copy className="w-3 h-3" />}
                        </button>
                      </div>
                    </td>
                    <td className="p-3 text-slate-700">
                      <strong>{item.category}</strong> ({item.trapped_count} Victims)
                    </td>
                    <td className="p-3 text-slate-600 max-w-xs font-medium">
                      <p className="line-clamp-2">{item.action_summary}</p>
                    </td>
                    <td className="p-3">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                        item.status === 'RESCUED'
                          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : item.status === 'DISPATCHED'
                          ? 'bg-blue-50 text-blue-700 border-blue-200'
                          : 'bg-amber-50 text-amber-700 border-amber-200'
                      }`}>
                        {item.status}
                      </span>
                    </td>
                    <td className="p-3 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        <button
                          onClick={() => handleViewDispatchCard(item)}
                          className="px-2 py-1 bg-slate-800 hover:bg-slate-700 text-white rounded text-[10px] font-semibold flex items-center gap-1"
                        >
                          <FileSpreadsheet className="w-3 h-3 text-amber-400" />
                          <span>Card</span>
                        </button>
                        {item.status === 'PENDING' && (
                          <button
                            onClick={() => handleStatusChange(item.id, 'DISPATCHED')}
                            className="px-2 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-[10px] font-bold flex items-center gap-1"
                          >
                            <Truck className="w-3 h-3" />
                            <span>Dispatch</span>
                          </button>
                        )}
                        {item.status === 'DISPATCHED' && (
                          <button
                            onClick={() => handleStatusChange(item.id, 'RESCUED')}
                            className="px-2 py-1 bg-emerald-600 hover:bg-emerald-500 text-white rounded text-[10px] font-bold flex items-center gap-1"
                          >
                            <CheckCircle2 className="w-3 h-3" />
                            <span>Rescued</span>
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Field Rescue Dispatch Card Modal */}
      <DispatchModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        sosData={selectedSOS}
        dispatchData={dispatchCardData}
      />
    </div>
  );
};

export default ResponderDashboard;
