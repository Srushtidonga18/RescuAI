import os

path = 'frontend/src/components/ResponderDashboard.jsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

states_hook = '''
  const [newInvName, setNewInvName] = useState('');
  const [newInvQty, setNewInvQty] = useState('');
  const [newVolName, setNewVolName] = useState('');
  const [newVolPhone, setNewVolPhone] = useState('');
'''
content = content.replace('const [searchLocation, setSearchLocation] = useState(\'\');', 'const [searchLocation, setSearchLocation] = useState(\'\');' + states_hook)

functions = '''
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
'''
content = content.replace('const handleCopyLandmark', functions + '\n  const handleCopyLandmark')

inv_ui = '''<div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm p-4">
          <h3 className="font-bold mb-4 text-slate-800">Available Resources</h3>
          <form onSubmit={handleAddInventory} className="mb-6 flex gap-2">
            <input type="text" placeholder="Item Name" value={newInvName} onChange={e=>setNewInvName(e.target.value)} className="border rounded p-2 text-sm flex-1" required />
            <input type="number" placeholder="Qty" value={newInvQty} onChange={e=>setNewInvQty(e.target.value)} className="border rounded p-2 text-sm w-24" required />
            <button type="submit" className="bg-red-600 text-white px-4 py-2 rounded text-sm font-bold">Add</button>
          </form>
          <table className="w-full text-left text-sm border-collapse">'''
content = content.replace('<div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm p-4">\n          <h3 className="font-bold mb-4 text-slate-800">Available Resources</h3>\n          <table className="w-full text-left text-sm border-collapse">', inv_ui)

vol_ui = '''<div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm p-4">
          <h3 className="font-bold mb-4 text-slate-800">Active Volunteers</h3>
          <form onSubmit={handleAddVolunteer} className="mb-6 flex gap-2">
            <input type="text" placeholder="Volunteer Name" value={newVolName} onChange={e=>setNewVolName(e.target.value)} className="border rounded p-2 text-sm flex-1" required />
            <input type="text" placeholder="Phone" value={newVolPhone} onChange={e=>setNewVolPhone(e.target.value)} className="border rounded p-2 text-sm flex-1" required />
            <button type="submit" className="bg-red-600 text-white px-4 py-2 rounded text-sm font-bold">Register</button>
          </form>
          <table className="w-full text-left text-sm border-collapse">'''
content = content.replace('<div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm p-4">\n          <h3 className="font-bold mb-4 text-slate-800">Active Volunteers</h3>\n          <table className="w-full text-left text-sm border-collapse">', vol_ui)

content = content.replace('vol.specialty', 'vol.phone')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
