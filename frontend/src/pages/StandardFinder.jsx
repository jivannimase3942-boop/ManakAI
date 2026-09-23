import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { t } from '../i18n.js'
import { api } from '../api.js'
import { useLocalData } from '../hooks/useLocalData.js'

export default function StandardFinder({ language }) {
  const location = useLocation()
  const { saveStandard, removeStandard, isSaved } = useLocalData()
  const [description, setDescription] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [notFound, setNotFound] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const prefill = location.state?.prefill
    if (prefill) {
      setDescription(prefill)
      handleSearch(prefill)
    }
  }, [location.state])

  async function handleSearch(q) {
    const val = q || description
    if (!val.trim() || loading) return
    setLoading(true)
    setNotFound(false)
    setError(null)
    setResult(null)
    try {
      const res = await api.standardSearch(val, language)
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
    <div className="bg-[#f8f9fa] min-h-screen pb-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h1 className="text-3xl font-extrabold text-[#0B1E40] tracking-tight mb-2">{t(language, 'nav_finder')}</h1>
        <p className="text-slate-600 text-lg mb-10 leading-relaxed max-w-2xl">{t(language, 'lbl_sf_desc')}</p>

      <div className="flex flex-col sm:flex-row gap-3 bg-white border border-slate-300 rounded-lg p-2 shadow-sm focus-within:border-[#0B1E40] focus-within:ring-1 focus-within:ring-[#0B1E40] mb-12">
        <input
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
          placeholder={t(language, 'finder_placeholder')}
          className="flex-1 px-4 py-3 text-[15px] text-slate-900 placeholder-slate-400 focus:outline-none bg-transparent"
        />
        <button
          onClick={() => handleSearch()}
          disabled={loading}
          className="bg-[#0B1E40] hover:bg-navy-900 disabled:opacity-50 text-white font-semibold px-8 py-3 rounded-md transition-colors whitespace-nowrap"
        >
          {loading ? 'Searching...' : 'Find Standard'}
        </button>
      </div>

      {error && <p className="text-sm text-red-600 mt-4">{error}</p>}

      {!result && !notFound && !loading && (
        <div className="text-center text-slate-500 text-sm border border-dashed border-slate-300 bg-slate-50 rounded-xl py-14 px-6">
          {t(language, 'lbl_sf_empty')}
        </div>
      )}

      {notFound && !loading && (
        <div className="text-center bg-red-50 border border-red-200 rounded-lg py-12 px-6 shadow-sm">
          <h3 className="text-red-800 font-bold mb-2 uppercase tracking-wider text-sm">{t(language, 'lbl_no_match')}</h3>
          <p className="text-red-700 text-sm max-w-lg mx-auto leading-relaxed">
            {t(language, 'lbl_sf_not_found')}
          </p>
        </div>
      )}

      {result && !loading && (
        <div className="bg-white border border-slate-200 hover:border-[#1C4E80] transition-colors rounded-lg p-8 shadow-sm">
          <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">{t(language, 'lbl_app_standard')}</h3>
          <p className="text-3xl font-extrabold text-[#0B1E40] mb-2">{result.applicable_standard || t(language, 'lbl_app_standard')}</p>
          <p className="text-md font-medium text-[#1C4E80] mb-8">{result.product}</p>

          {result.sources && result.sources.length > 0 && (
            <div className="border-t border-slate-200 pt-6 mt-6">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">{t(language, 'lbl_evidence')}</h4>
              <a href={result.sources[0].source_url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center text-sm font-semibold text-[#1C4E80] hover:underline underline-offset-2">
                {t(language, 'lbl_view_official')} <span className="ml-1 text-lg leading-none">→</span>
              </a>
            </div>
          )}
        </div>
      )}
      </div>
    </div>
  )
}
