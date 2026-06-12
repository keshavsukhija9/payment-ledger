import { useState, useEffect } from 'react'
import client from '../api/client'

export function useMetrics(pollInterval = 5000) {
  const [metrics, setMetrics] = useState(null)

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const res = await client.get('/payments/metrics')
        setMetrics(res.data)
      } catch (e) {
        console.error('Failed to fetch metrics:', e.message)
      }
    }
    fetchMetrics()
    const interval = setInterval(fetchMetrics, pollInterval)
    return () => clearInterval(interval)
  }, [pollInterval])

  return { metrics }
}
