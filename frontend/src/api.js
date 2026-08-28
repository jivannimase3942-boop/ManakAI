const BASE = ''

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
  assistantQuery: (query, mode, language) => post('/api/assistant/query', { query, mode, language }),
  standardSearch: (description, language) => post('/api/standard-search', { description, language }),
  services: () => get('/api/services'),
  sources: () => get('/api/sources'),
  health: () => get('/api/health'),
}
