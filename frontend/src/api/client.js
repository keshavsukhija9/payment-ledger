import axios from 'axios'

const client = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

client.interceptors.response.use(
  res => res,
  err => {
    const message = err.response?.data?.error
      || err.response?.data?.detail
      || 'Something went wrong'
    return Promise.reject(new Error(message))
  }
)

export default client
