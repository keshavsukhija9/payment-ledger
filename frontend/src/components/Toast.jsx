import { useEffect } from 'react'

export function Toast({ message, type, onDismiss }) {
  useEffect(() => {
    if (!message) return
    const t = setTimeout(onDismiss, 3000)
    return () => clearTimeout(t)
  }, [message])

  if (!message) return null
  return (
    <div style={{
      position:'fixed', bottom:'24px', right:'24px',
      padding:'12px 20px', borderRadius:'8px', fontWeight:600,
      background: type === 'error' ? '#f8d7da' : '#d4edda',
      color: type === 'error' ? '#721c24' : '#155724',
      boxShadow:'0 2px 8px rgba(0,0,0,0.15)', zIndex:1000
    }}>
      {message}
    </div>
  )
}
