export function IntegrityBanner({ metrics }) {
  if (!metrics) return null
  const balanced = metrics.ledger_balanced
  return (
    <div style={{
      padding: '12px 20px',
      background: balanced ? '#d4edda' : '#f8d7da',
      color: balanced ? '#155724' : '#721c24',
      borderRadius: '6px',
      fontWeight: 600,
      marginBottom: '20px'
    }}>
      {balanced ? '✓ Ledger Balanced — debit sum equals credit sum' : '✗ LEDGER IMBALANCED — investigate immediately'}
      {' | '}Debit: ₹{Number(metrics.debit_sum).toLocaleString('en-IN')}
      {' | '}Credit: ₹{Number(metrics.credit_sum).toLocaleString('en-IN')}
    </div>
  )
}
