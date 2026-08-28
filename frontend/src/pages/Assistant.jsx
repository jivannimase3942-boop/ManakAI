import { useState, useRef, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import ChatMessage from '../components/ChatMessage.jsx'
import { t, EXAMPLE_QUESTIONS } from '../i18n.js'
import { api } from '../api.js'

export default function Assistant({ language }) {
  const location = useLocation()
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [mode, setMode] = useState('industry')
  const scrollRef = useRef(null)
  const prefillHandled = useRef(false)

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, loading])

  useEffect(() => {
    const prefill = location.state?.prefill
    if (prefill && !prefillHandled.current) {
      prefillHandled.current = true
      send(prefill)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function send(text) {
    const value = (text ?? input).trim()
    if (!value || loading) return
    setInput('')
    setError(null)
    const userMsg = { role: 'user', content: value }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)
    try {
      const res = await api.assistantQuery(value, mode, language)
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          ...res
        },
      ])
    } catch (e) {
      setError('Could not reach ManakAI backend. Please make sure the backend server is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col" style={{ minHeight: 'calc(100vh - 64px)' }}>
      <div className="mb-5 flex flex-col sm:flex-row sm:justify-between sm:items-end">
        <div>
          <h1 className="text-2xl font-bold text-navy-900">{t(language, 'chat_title')}</h1>
          <p className="text-navy-600 text-sm mt-1">{t(language, 'chat_sub')}</p>
        </div>
        <div className="mt-4 sm:mt-0 flex bg-gray-100 p-1 rounded-lg">
          <button
            onClick={() => setMode('industry')}
            className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-colors ${mode === 'industry' ? 'bg-white shadow text-navy-900' : 'text-gray-500 hover:text-navy-700'}`}
          >
            INDUSTRY / MSME
          </button>
          <button
            onClick={() => setMode('consumer')}
            className={`px-4 py-1.5 text-sm font-semibold rounded-md transition-colors ${mode === 'consumer' ? 'bg-white shadow text-navy-900' : 'text-gray-500 hover:text-navy-700'}`}
          >
            CONSUMER
          </button>
        </div>
      </div>

      <div
        ref={scrollRef}
        className="flex-1 overflow-y-auto scrollbar-thin bg-slate-50 border border-navy-100 rounded-2xl p-4 sm:p-6 space-y-4 min-h-[420px] max-h-[60vh]"
      >
        {messages.length === 0 && (
          <div className="h-full flex flex-col items-center justify-center text-center py-10">
            <p className="text-navy-500 text-sm max-w-sm">{t(language, 'chat_empty')}</p>
          </div>
        )}
        {messages.map((m, i) => (
          <ChatMessage key={i} message={m} language={language} />
        ))}
        {loading && (
          <div className="flex justify-start mb-6 w-full">
            <div className="w-full bg-white border border-navy-100 rounded-xl px-6 py-8 shadow-card flex items-center justify-center">
              <div className="flex gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-navy-400 animate-pulse" />
                <span className="w-2.5 h-2.5 rounded-full bg-navy-400 animate-pulse [animation-delay:0.15s]" />
                <span className="w-2.5 h-2.5 rounded-full bg-navy-400 animate-pulse [animation-delay:0.3s]" />
              </div>
            </div>
          </div>
        )}
      </div>

      {error && <p className="text-sm text-red-600 mt-3">{error}</p>}

      <div className="mt-4 flex flex-wrap gap-2">
        {EXAMPLE_QUESTIONS[language].map((q) => (
          <button
            key={q}
            onClick={() => send(q)}
            disabled={loading}
            className="text-xs sm:text-[13px] bg-white border border-navy-200 hover:bg-navy-50 text-navy-700 rounded-full px-3.5 py-1.5 transition-colors disabled:opacity-50"
          >
            {q}
          </button>
        ))}
      </div>

      <div className="mt-4 flex items-stretch gap-2 bg-white border border-navy-200 rounded-xl p-1.5 shadow-card focus-within:ring-2 focus-within:ring-navy-500">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && send()}
          placeholder={t(language, 'chat_placeholder')}
          className="flex-1 px-3.5 py-2.5 text-[15px] text-navy-900 placeholder-navy-400 focus:outline-none bg-transparent"
        />
        <button
          onClick={() => send()}
          disabled={loading}
          className="bg-navy-700 hover:bg-navy-800 disabled:opacity-50 text-white font-semibold text-sm px-5 py-2.5 rounded-lg transition-colors whitespace-nowrap"
        >
          {t(language, 'chat_send')}
        </button>
      </div>
    </div>
  )
}
