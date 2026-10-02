import React, { useState, useEffect, useCallback, useContext } from 'react';
import { Search, Filter, RefreshCw, LayoutDashboard, AlertCircle, LayoutGrid, Table, CheckCircle2, ShieldAlert, Truck, Copy, Check, FileSpreadsheet, Map, Package, Users, Download } from 'lucide-react';
import api from '../api/axios';
import { AuthContext } from '../context/AuthContext';
import StatsBar from './StatsBar';
import SOSCard from './SOSCard';
import DispatchModal from './DispatchModal';

const ResponderDashboard = () => {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Tab View for queue
  const [activeTab, setActiveTab] = useState('active');
  const [viewMode, setViewMode] = useState('grid');
  
  const [dashboardTab, setDashboardTab] = useState('queue'); // 'queue', 'map', 'inventory', 'volunteers'
  const [mapData, setMapData] = useState([]);
  const [inventory, setInventory] = useState([]);
  const [volunteers, setVolunteers] = useState([]);

  // Filters & Search
  const [searchLocation, setSearchLocation] = useState('');
  const [newInvName, setNewInvName] = useState('');
  const [newInvQty, setNewInvQty] = useState('');
  const [newVolName, setNewVolName] = useState('');
  const [newVolPhone, setNewVolPhone] = useState('');

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

  const fetchMapData = async () => {
    try {
      const res = await api.get('/api/v1/sos/map-data');
      setMapData(res.data);
    } catch (err) { console.error(err); }
  };
  const fetchInventory = async () => {
    try {
      const res = await api.get('/api/v1/responder/inventory');
      setInventory(res.data);
    } catch (err) { console.error(err); }
  };
  const fetchVolunteers = async () => {
    try {
      const res = await api.get('/api/v1/responder/volunteer');
      setVolunteers(res.data);
    } catch (err) { console.error(err); }
  };

  useEffect(() => {
    fetchDashboardData();
    fetchInventory();
    fetchVolunteers();
  }, [fetchDashboardData]);

  useEffect(() => {
    if (!autoRefresh) return;
    const interval = setInterval(() => {
      fetchDashboardData();
    }, 10000);
    return () => clearInterval(interval);
  }, [autoRefresh, fetchDashboardData]);

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

  const handleStatusChange = async (sosId, newStatus, manualTeam = null) => {
    try {
      let team = manualTeam;
      if (!team && volunteers && volunteers.length > 0) {
        team = volunteers[0].name;
      } else if (!team) {
        team = 'Alpha Rescue Squad';
      }

      await api.patch(`/api/v1/responder/sos/${sosId}/status`, {
        status: newStatus,
        assigned_team: team,
      });
      fetchDashboardData();
    } catch (err) {
      console.error('Status update failed:', err);
    }
  };

  
  const handleAddInventory = async (e) => {
    e.preventDefault();
    if (!newInvName || !newInvQty) return;
    try {
      await api.post('/api/v1/responder/inventory', { name: newInvName, quantity: parseInt(newInvQty) });
      setNewInvName(''); setNewInvQty('');
      fetchInventory();
    } catch(err) { console.error(err); }
  };

  const handleAddVolunteer = async (e) => {
    e.preventDefault();
    if (!newVolName || !newVolPhone) return;
    try {
      await api.post('/api/v1/responder/volunteer', { name: newVolName, phone: newVolPhone });
      setNewVolName(''); setNewVolPhone('');
      fetchVolunteers();
    } catch(err) { console.error(err); }
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

        <div className="flex items-center gap-2">
          <a
            href="http://localhost:8000/api/v1/responder/report/pdf"
            target="_blank"
            rel="noopener noreferrer"
            className="px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white rounded-lg text-xs font-bold flex items-center gap-1.5 shadow"
          >
            <Download className="w-4 h-4" />
            <span>Download PDF Report</span>
          </a>
        </div>
      </div>

      <StatsBar allItems={items} />

      {/* Main Dashboard Tabs */}
      <div className="flex space-x-2 border-b border-slate-200 mb-4">
        <button
          onClick={() => setDashboardTab('queue')}
          className={`pb-2 px-1 text-sm font-bold flex items-center gap-2 border-b-2 transition-colors ${dashboardTab === 'queue' ? 'border-red-600 text-red-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          <ShieldAlert className="w-4 h-4" /> Queue
        </button>
        <button
          onClick={() => setDashboardTab('inventory')}
          className={`pb-2 px-1 text-sm font-bold flex items-center gap-2 border-b-2 transition-colors ${dashboardTab === 'inventory' ? 'border-red-600 text-red-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          <Package className="w-4 h-4" /> Inventory
        </button>
        <button
          onClick={() => setDashboardTab('volunteers')}
          className={`pb-2 px-1 text-sm font-bold flex items-center gap-2 border-b-2 transition-colors ${dashboardTab === 'volunteers' ? 'border-red-600 text-red-600' : 'border-transparent text-slate-500 hover:text-slate-700'}`}
        >
          <Users className="w-4 h-4" /> Volunteers
        </button>
      </div>

      {dashboardTab === 'queue' && (
        <>
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

            {/* Controls */}
            <div className="flex flex-wrap items-center gap-2 text-xs">
              {/* Tab Selection: Active Queue vs Rescued Archive */}
              <div className="flex rounded-lg bg-slate-200 p-1 text-xs font-bold mr-2">
                <button
                  onClick={() => setActiveTab('active')}
                  className={`px-3 py-1 rounded-md flex items-center gap-1.5 transition-all ${
                    activeTab === 'active' ? 'bg-slate-900 text-white shadow' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <span>Active</span>
                </button>
                <button
                  onClick={() => setActiveTab('rescued')}
                  className={`px-3 py-1 rounded-md flex items-center gap-1.5 transition-all ${
                    activeTab === 'rescued' ? 'bg-emerald-700 text-white shadow' : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  <span>Rescued</span>
                </button>
              </div>

              <select
                value={urgencyFilter}
                onChange={(e) => setUrgencyFilter(e.target.value)}
                className="bg-slate-50 border border-slate-200 rounded-lg py-1.5 px-2.5 text-xs font-semibold text-slate-800 focus:outline-none focus:border-red-500"
              >
                <option value="">All Urgency</option>
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
                <option value="MEDICAL">Medical</option>
                <option value="TRAPPED">Trapped</option>
                <option value="FOOD_WATER">Food</option>
              </select>

              <button
                onClick={() => setViewMode(viewMode === 'grid' ? 'table' : 'grid')}
                className="px-2.5 py-1.5 rounded-lg text-xs font-bold border transition-all bg-slate-100 text-slate-600 border-slate-300 ml-2"
              >
                {viewMode === 'grid' ? <Table className="w-4 h-4" /> : <LayoutGrid className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {error && (
            <div className="mb-5 p-3 bg-red-50 border border-red-200 rounded-xl text-xs text-red-600 font-medium flex items-center gap-2">
              <AlertCircle className="w-4 h-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {loading ? (
            <div className="text-center py-16">
              <div className="w-7 h-7 border-3 border-red-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
              <p className="text-xs font-semibold text-slate-500">Loading emergency queue...</p>
            </div>
          ) : displayedItems.length === 0 ? (
            <div className="bg-white border border-slate-200 rounded-2xl p-10 text-center max-w-md mx-auto my-6 shadow-sm">
              <CheckCircle2 className="w-10 h-10 text-emerald-500 mx-auto mb-2" />
              <h3 className="font-bold text-slate-800 text-sm">No Records Found</h3>
            </div>
          ) : viewMode === 'grid' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {displayedItems.map((item) => (
                <SOSCard
                  key={item.id}
                  item={item}
                  volunteers={volunteers}
                  onStatusUpdated={fetchDashboardData}
                  onViewDispatchCard={handleViewDispatchCard}
                />
              ))}
            </div>
          ) : (
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
                            item.urgency_level === 'CRITICAL' ? 'bg-red-600 text-white' : item.urgency_level === 'MODERATE' ? 'bg-amber-500 text-slate-950 font-bold' : 'bg-emerald-600 text-white'
                          }`}>{item.urgency_level}</span>
                        </td>
                        <td className="p-3 font-semibold text-slate-900">{item.extracted_location}</td>
                        <td className="p-3 text-slate-700"><strong>{item.category}</strong> ({item.trapped_count})</td>
                        <td className="p-3 text-slate-600 max-w-xs font-medium"><p className="line-clamp-2">{item.action_summary}</p></td>
                        <td className="p-3">
                          <span className={`px-2 py-0.5 rounded text-[10px] font-bold border ${
                            item.status === 'RESCUED' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : item.status === 'DISPATCHED' ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-amber-50 text-amber-700 border-amber-200'
                          }`}>{item.status}</span>
                        </td>
                        <td className="p-3 text-right">
                          <button onClick={() => handleViewDispatchCard(item)} className="px-2 py-1 bg-slate-800 text-white rounded text-[10px] font-semibold mr-1">Card</button>
                          {item.status === 'PENDING' && (
  <div className="inline-flex items-center gap-1">
    <select id={`team-select-${item.id}`} className="px-1 py-1 text-[10px] border border-slate-300 rounded bg-white" defaultValue="">
      <option value="">Auto Assign</option>
      {volunteers.map(v => <option key={v.name} value={v.name}>{v.name}</option>)}
    </select>
    <button onClick={() => {
      const selectEl = document.getElementById(`team-select-${item.id}`);
      handleStatusChange(item.id, 'DISPATCHED', selectEl ? selectEl.value : null);
    }} className="px-2 py-1 bg-blue-600 text-white rounded text-[10px] font-bold">Dispatch</button>
  </div>
)}
                          {item.status === 'DISPATCHED' && <button onClick={() => handleStatusChange(item.id, 'RESCUED')} className="px-2 py-1 bg-emerald-600 text-white rounded text-[10px] font-bold">Rescued</button>}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}

      {dashboardTab === 'inventory' && (
        <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm p-4">
          <h3 className="font-bold mb-4 text-slate-800">Available Resources</h3>
          <form onSubmit={handleAddInventory} className="mb-6 flex gap-2">
            <input type="text" placeholder="Item Name" value={newInvName} onChange={e=>setNewInvName(e.target.value)} className="border rounded p-2 text-sm flex-1" required />
            <input type="number" placeholder="Qty" value={newInvQty} onChange={e=>setNewInvQty(e.target.value)} className="border rounded p-2 text-sm w-24" required />
            <button type="submit" className="bg-red-600 text-white px-4 py-2 rounded text-sm font-bold">Add</button>
          </form>
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b bg-slate-50"><th className="p-2">Item Name</th><th className="p-2">Quantity</th></tr>
            </thead>
            <tbody>
              {inventory.length > 0 ? inventory.map(inv => (
                <tr key={inv.id} className="border-b"><td className="p-2">{inv.name}</td><td className="p-2">{inv.quantity}</td></tr>
              )) : <tr><td colSpan="2" className="p-2 text-center text-slate-500">No inventory found</td></tr>}
            </tbody>
          </table>
        </div>
      )}

      {dashboardTab === 'volunteers' && (
        <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm p-4">
          <h3 className="font-bold mb-4 text-slate-800">Active Volunteers</h3>
          <form onSubmit={handleAddVolunteer} className="mb-6 flex gap-2">
            <input type="text" placeholder="Volunteer Name" value={newVolName} onChange={e=>setNewVolName(e.target.value)} className="border rounded p-2 text-sm flex-1" required />
            <input type="text" placeholder="Phone" value={newVolPhone} onChange={e=>setNewVolPhone(e.target.value)} className="border rounded p-2 text-sm flex-1" required />
            <button type="submit" className="bg-red-600 text-white px-4 py-2 rounded text-sm font-bold">Register</button>
          </form>
          <table className="w-full text-left text-sm border-collapse">
            <thead>
              <tr className="border-b bg-slate-50"><th className="p-2">Name</th><th className="p-2">Specialty</th><th className="p-2">Location</th></tr>
            </thead>
            <tbody>
              {volunteers.length > 0 ? volunteers.map(vol => (
                <tr key={vol.id} className="border-b"><td className="p-2">{vol.name}</td><td className="p-2">{vol.phone}</td><td className="p-2">{vol.location}</td></tr>
              )) : <tr><td colSpan="3" className="p-2 text-center text-slate-500">No volunteers found</td></tr>}
            </tbody>
          </table>
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

