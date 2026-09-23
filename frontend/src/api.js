export const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function post(path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }))
    throw new Error(err.detail || 'Request failed')
  }
  return res.json()
}

async function get(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error('Request failed')
  return res.json()
}

export const api = {
  assistantQuery: (query, mode, language, history = []) => post('/api/assistant/query', { query, mode, language, history }),
  standardSearch: (description, language) => post('/api/standard-search', { description, language }),
  services: () => get('/api/services'),
  sources: () => get('/api/sources'),
  health: () => get('/api/health'),
  analyzeProduct: async (formData) => {
    const res = await fetch(`${BASE}/api/analyze-product`, {
      method: 'POST',
      body: formData
    })
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Request failed' }))
      throw new Error(err.detail || err.error || 'Analysis failed')
    }
    return res.json()
  }
}
