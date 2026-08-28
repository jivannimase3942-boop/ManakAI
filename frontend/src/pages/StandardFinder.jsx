import { useState } from 'react'
import ChatMessage from '../components/ChatMessage.jsx'
import { t } from '../i18n.js'
import { api } from '../api.js'

export default function StandardFinder({ language }) {
  const [description, setDescription] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [notFound, setNotFound] = useState(false)
  const [error, setError] = useState(null)

  async function handleSearch() {
    if (!description.trim() || loading) return
    setLoading(true)
    setNotFound(false)
    setError(null)
    setResult(null)
    try {
      const res = await api.standardSearch(description, language)
      if (res.confidence === 'none') {
        setNotFound(true)
      } else {
        setResult(res)
      }
    } catch (e) {
      setNotFound(true)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-2xl font-bold text-navy-900">{t(language, 'finder_title')}</h1>
      <p className="text-navy-600 text-sm mt-1.5">{t(language, 'finder_sub')}</p>

      <div className="mt-6 flex flex-col sm:flex-row gap-2 bg-white border border-navy-200 rounded-xl p-1.5 shadow-card focus-within:ring-2 focus-within:ring-navy-500 mb-10">
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          placeholder={t(language, 'finder_placeholder')}
          className="flex-1 px-3.5 py-2.5 text-[15px] text-navy-900 placeholder-navy-400 focus:outline-none bg-transparent"
        />
        <button
          onClick={handleSearch}
          disabled={loading}
          className="bg-navy-700 hover:bg-navy-800 disabled:opacity-50 text-white font-semibold text-sm px-5 py-2.5 rounded-lg transition-colors whitespace-nowrap"
        >
          {loading ? '…' : t(language, 'finder_button')}
        </button>
      </div>

      {error && <p className="text-sm text-red-600 mt-4">{error}</p>}

      {!result && !notFound && !loading && (
        <div className="mt-10 text-center text-navy-500 text-sm border border-dashed border-navy-200 rounded-2xl py-14 px-6">
          {t(language, 'finder_empty')}
        </div>
      )}

      {notFound && !loading && (
        <div className="mt-10 text-center text-navy-600 text-sm bg-navy-50 border border-navy-100 rounded-2xl py-10 px-6">
          {t(language, 'finder_not_found')}
        </div>
      )}

      {result && !loading && (
        <div className="mt-8">
           <ChatMessage message={{ role: 'assistant', ...result }} language={language} />
        </div>
      )}
    </div>
  )
}
