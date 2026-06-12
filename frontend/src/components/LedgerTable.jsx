export function LedgerTable({ entries, loading }) {
  if (loading) return <div>Loading ledger...</div>
  return (
    <div>
      <h3>Ledger Entries</h3>
      <table style={{ width:'100%', borderCollapse:'collapse', fontSize:'13px' }}>
        <thead>
          <tr style={{ background:'#f8f9fa' }}>
            {['Type','Amount','Account','Transfer ID','Time'].map(h => (
              <th key={h} style={{ padding:'8px 12px', textAlign:'left', borderBottom:'2px solid #dee2e6' }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {entries.map(e => (
            <tr key={e.id} style={{ borderBottom:'1px solid #f0f0f0' }}>
              <td style={{ padding:'8px 12px' }}>
                <span style={{
                  padding:'2px 8px', borderRadius:'4px', fontSize:'11px', fontWeight:700,
                  background: e.entry_type === 'DEBIT' ? '#f8d7da' : '#d4edda',
                  color: e.entry_type === 'DEBIT' ? '#721c24' : '#155724'
                }}>{e.entry_type}</span>
              </td>
              <td style={{ padding:'8px 12px', fontWeight:600 }}>₹{Number(e.amount).toLocaleString('en-IN')}</td>
              <td style={{ padding:'8px 12px', color:'#6c757d' }}>{e.account_id.slice(0,8)}...</td>
              <td style={{ padding:'8px 12px', color:'#6c757d' }}>{e.transfer_id.slice(0,8)}...</td>
              <td style={{ padding:'8px 12px', color:'#6c757d' }}>{new Date(e.created_at).toLocaleTimeString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
