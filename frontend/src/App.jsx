import { useState } from 'react'
import { useAccounts } from './hooks/useAccounts'
import { useLedger } from './hooks/useLedger'
import { useMetrics } from './hooks/useMetrics'
import { MetricsBar } from './components/MetricsBar'
import { AccountsList } from './components/AccountsList'
import { TransferForm } from './components/TransferForm'
import { LedgerTable } from './components/LedgerTable'
import { IntegrityBanner } from './components/IntegrityBanner'
import { Toast } from './components/Toast'

export default function App() {
  const { accounts, loading: accountsLoading } = useAccounts(3000)
  const { entries, loading: ledgerLoading } = useLedger(3000)
  const { metrics } = useMetrics(5000)
  const [toast, setToast] = useState({ message: '', type: '' })

  const handleSuccess = (data, idemKey) => {
    setToast({ message: `Transfer ${data.transfer_id.slice(0,8)}… succeeded | Key: ${idemKey.slice(0,8)}…`, type: 'success' })
  }

  const handleError = (msg) => {
    setToast({ message: msg, type: 'error' })
  }

  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '24px', fontFamily: 'system-ui, sans-serif' }}>
      <h1 style={{ marginBottom: '4px' }}>Payment Ledger</h1>
      <p style={{ color: '#6c757d', marginTop: 0, marginBottom: '24px' }}>
        Idempotency · Double-Entry · Concurrent Safety
      </p>

      <IntegrityBanner metrics={metrics} />
      <MetricsBar metrics={metrics} />

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '24px' }}>
        <div>
          <TransferForm accounts={accounts} onSuccess={handleSuccess} onError={handleError} />
          <AccountsList accounts={accounts} loading={accountsLoading} />
        </div>
        <div>
          <LedgerTable entries={entries} loading={ledgerLoading} />
        </div>
      </div>

      <Toast message={toast.message} type={toast.type} onDismiss={() => setToast({ message: '', type: '' })} />
    </div>
  )
}
