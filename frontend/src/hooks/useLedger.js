import { useState, useEffect } from 'react'
import client from '../api/client'

export function useLedger(pollInterval = 3000) {
  const [entries, setEntries] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchEntries = async () => {
      try {
        const res = await client.get('/ledger/entries')
        setEntries(res.data)
      } catch (e) {
        console.error('Failed to fetch ledger:', e.message)
      } finally {
        setLoading(false)
      }
    }
    fetchEntries()
    const interval = setInterval(fetchEntries, pollInterval)
    return () => clearInterval(interval)
  }, [pollInterval])

  return { entries, loading }
}
