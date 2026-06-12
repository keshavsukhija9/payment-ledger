import { useState } from 'react'
import client from '../api/client'

export function TransferForm({ accounts, onSuccess, onError }) {
  const [form, setForm] = useState({ sender_id:'', receiver_id:'', amount:'', idem_key:'' })
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    if (!form.sender_id || !form.receiver_id || !form.amount) { onError('All fields required'); return }
    if (form.sender_id === form.receiver_id) { onError('Sender and receiver must differ'); return }
    const idemKey = form.idem_key || crypto.randomUUID()
    setLoading(true)
    try {
      const res = await client.post('/payments/', {
        sender_id: form.sender_id,
        receiver_id: form.receiver_id,
        amount: parseFloat(form.amount)
      }, { headers: { 'Idempotency-Key': idemKey } })
      onSuccess(res.data, idemKey)
      setForm(f => ({ ...f, amount:'', idem_key:'' }))
    } catch (e) {
      onError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const inp = { padding:'8px 12px', borderRadius:'6px', border:'1px solid #ced4da', width:'100%', boxSizing:'border-box' }
  return (
    <div style={{ padding:'20px', background:'#fff', border:'1px solid #dee2e6', borderRadius:'8px', marginBottom:'24px' }}>
      <h3 style={{ marginTop:0 }}>New Transfer</h3>
      <div style={{ display:'grid', gap:'12px' }}>
        <div>
          <label style={{ display:'block', marginBottom:'4px', fontSize:'13px', fontWeight:600 }}>From</label>
          <select style={inp} value={form.sender_id} onChange={e => setForm(f => ({...f, sender_id:e.target.value}))}>
            <option value="">Select account</option>
            {accounts.map(a => <option key={a.id} value={a.id}>{a.owner_name} — ₹{Number(a.balance).toLocaleString('en-IN')}</option>)}
          </select>
        </div>
        <div>
          <label style={{ display:'block', marginBottom:'4px', fontSize:'13px', fontWeight:600 }}>To</label>
          <select style={inp} value={form.receiver_id} onChange={e => setForm(f => ({...f, receiver_id:e.target.value}))}>
            <option value="">Select account</option>
            {accounts.map(a => <option key={a.id} value={a.id}>{a.owner_name}</option>)}
          </select>
        </div>
        <div>
          <label style={{ display:'block', marginBottom:'4px', fontSize:'13px', fontWeight:600 }}>Amount (₹)</label>
          <input style={inp} type="number" min="1" placeholder="500" value={form.amount} onChange={e => setForm(f => ({...f, amount:e.target.value}))} />
        </div>
        <div>
          <label style={{ display:'block', marginBottom:'4px', fontSize:'13px', fontWeight:600 }}>Idempotency Key <span style={{fontWeight:400, color:'#6c757d'}}>(blank = auto)</span></label>
          <input style={inp} type="text" placeholder="leave blank for auto UUID" value={form.idem_key} onChange={e => setForm(f => ({...f, idem_key:e.target.value}))} />
        </div>
        <button onClick={handleSubmit} disabled={loading} style={{
          padding:'10px', background:'#0d6efd', color:'#fff', border:'none',
          borderRadius:'6px', fontWeight:600, cursor:'pointer', fontSize:'14px'
        }}>
          {loading ? 'Processing…' : 'Send Transfer'}
        </button>
      </div>
    </div>
  )
}
