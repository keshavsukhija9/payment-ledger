import { useState, useEffect } from 'react'
import client from '../api/client'

export function useAccounts(pollInterval = 3000) {
  const [accounts, setAccounts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        const res = await client.get('/accounts/')
        setAccounts(res.data)
      } catch (e) {
        console.error('Failed to fetch accounts:', e.message)
      } finally {
        setLoading(false)
      }
    }
    fetchAccounts()
    const interval = setInterval(fetchAccounts, pollInterval)
    return () => clearInterval(interval)
  }, [pollInterval])

  return { accounts, loading }
}
