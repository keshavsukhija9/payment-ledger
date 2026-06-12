export function MetricsBar({ metrics }) {
  if (!metrics) return <div style={{padding:'16px'}}>Loading metrics...</div>
  const cards = [
    { label: 'Total Transfers', value: metrics.total_transfers },
    { label: 'Total Volume', value: '₹' + Number(metrics.total_volume).toLocaleString('en-IN') },
    { label: 'Deduped Requests', value: metrics.deduped_requests },
    { label: 'Ledger Status', value: metrics.ledger_balanced ? '✓ Balanced' : '✗ Imbalanced' },
  ]
  return (
    <div style={{ display:'flex', gap:'16px', marginBottom:'20px', flexWrap:'wrap' }}>
      {cards.map(c => (
        <div key={c.label} style={{
          flex:'1', minWidth:'160px', padding:'16px', background:'#f8f9fa',
          borderRadius:'8px', border:'1px solid #dee2e6'
        }}>
          <div style={{ fontSize:'12px', color:'#6c757d', marginBottom:'4px' }}>{c.label}</div>
          <div style={{ fontSize:'20px', fontWeight:700 }}>{c.value}</div>
        </div>
      ))}
    </div>
  )
}
