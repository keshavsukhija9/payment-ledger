export function AccountsList({ accounts, loading }) {
  if (loading) return <div>Loading accounts...</div>
  return (
    <div style={{ marginBottom:'24px' }}>
      <h3>Accounts</h3>
      <div style={{ display:'flex', gap:'12px', flexWrap:'wrap' }}>
        {accounts.map(a => (
          <div key={a.id} style={{
            padding:'12px 16px', background:'#fff', border:'1px solid #dee2e6',
            borderRadius:'8px', minWidth:'180px'
          }}>
            <div style={{ fontWeight:600 }}>{a.owner_name}</div>
            <div style={{ fontSize:'20px', color:'#198754', fontWeight:700 }}>
              ₹{Number(a.balance).toLocaleString('en-IN')}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
