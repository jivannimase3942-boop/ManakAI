import { useState, useRef, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import ChatMessage from '../components/ChatMessage.jsx'
import ComplaintCopilot from '../components/ComplaintCopilot.jsx'
import MsmeComplianceRoadmap from '../components/MsmeComplianceRoadmap.jsx'
import EcosystemRouter from '../components/EcosystemRouter.jsx'
import DecisionCard from '../components/DecisionCard.jsx'
import VoiceAssistant from '../components/VoiceAssistant.jsx'
import { t, EXAMPLE_QUESTIONS } from '../i18n.js'
import { api } from '../api.js'
import { useLocalData } from '../hooks/useLocalData.js'

const PRONOUNS = new Set([
  "त्याची", "त्याचा", "त्याचे", "त्याला", "ही", "हे", "तो", "ती", "याची", "याचा", "याचे", "याला",
  "उसकी", "उसका", "उसके", "उसको", "यह", "वह", "इसे", "उसे", "इसकी", "इसका", "इसके", "इसको",
  "it", "its", "this", "that"
])

function resolvePronounContext(query, context) {
  if (!context || !context.product_entity || !query) return query;

  const cleanQuery = query.replace(/[^\w\s\u0900-\u097F]/gi, '').toLowerCase();
  const words = cleanQuery.split(/\s+/);

  const hasPronoun = words.some(w => PRONOUNS.has(w));

  if (hasPronoun) {
    const product = context.product_entity;
    if (!query.toLowerCase().includes(product.toLowerCase())) {
      return `${product} ${query}`;
    }
  }
  return query;
}

export default function Assistant({ language }) {
  const location = useLocation()
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [mode, setMode] = useState('industry')
  const [result, setResult] = useState(null)
  const [notFound, setNotFound] = useState(false)
  const [ttsResponse, setTtsResponse] = useState(null)
  const [sessionContext, setSessionContext] = useState(null)
  const prefillHandled = useRef(false)
  const { addHistory } = useLocalData()

  useEffect(() => {
    setSessionContext(null)
  }, [language, mode])

  useEffect(() => {
    const prefill = location.state?.prefill
    if (prefill && !prefillHandled.current) {
      prefillHandled.current = true
      setInput(prefill)
      send(prefill)
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.state])

  async function send(text) {
    const value = (text ?? input).trim()
    if (!value || loading) return
    setError(null)
    setResult(null)
    setNotFound(false)
    addHistory(value)
    setLoading(true)
    let finalQuery = value
    if (sessionContext) {
      finalQuery = resolvePronounContext(value, sessionContext)
    }

    try {
      if (sessionContext) {
        console.log(`[CTX-TRACE] original_query="${value}"`)
        console.log(`[CTX-TRACE] session_context=${JSON.stringify(sessionContext)}`)
        console.log(`[CTX-TRACE] resolved_query="${finalQuery}"`)
        console.log(`[CTX-TRACE] selected_product="${sessionContext.product_entity}"`)
        console.log(`[CTX-TRACE] selected_standard="${sessionContext.standard_id}"`)
      }

      const historyLog = JSON.parse(localStorage.getItem('manakai_history') || '[]')
      const formattedHistory = historyLog.map(item => ({
        role: item.role || 'user',
        content: item.query || item.text || item.content || ''
      })).filter(h => h.content).slice(0, 15)

      if (sessionContext) {
        console.log(`[CTX-TRACE] history_length=${formattedHistory.length}`)
        console.log(`[CTX-TRACE] history=${JSON.stringify(formattedHistory)}`)
      }

      const res = await api.assistantQuery(finalQuery, mode, language, formattedHistory)

      if (sessionContext) {
        console.log(`[CONTEXT] intent="${res.intent}"`)
      }

      if (res.confidence === 'none' || res.match_found === false) {
        setNotFound(true)
        setSessionContext(null)
        setTtsResponse(language === 'hi' ? 'मुझे सत्यापित BIS जानकारी नहीं मिली।' : language === 'mr' ? 'मला सत्यापित BIS माहिती मिळाली नाही.' : 'I couldn\'t find a verified match for your query.')
      } else {
        setResult(res)
        setTtsResponse(res.answer)
        if (['high', 'medium'].includes(res.confidence) && res.product && res.product !== 'Unknown') {
          setSessionContext({
            product_entity: res.product,
            standard_id: res.applicable_standard
          })
        }
      }
    } catch (e) {
      setError('Could not reach ManakAI backend. Please make sure the backend server is running.')
      setSessionContext(null)
      setTtsResponse(language === 'hi' ? 'सर्वर से कनेक्ट करने में त्रुटि।' : language === 'mr' ? 'सर्व्हरशी कनेक्ट करण्यात त्रुटी.' : 'Error connecting to server.')
    } finally {
      setLoading(false)
    }
  }

  const suggested = EXAMPLE_QUESTIONS[language] || EXAMPLE_QUESTIONS['en']

  return (
    <div className="bg-slate-50 min-h-screen pb-20">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">

        <div className="flex flex-col sm:flex-row sm:justify-between sm:items-end mb-8 border-b border-slate-200 pb-4">
          <div>
            <h1 className="text-2xl font-bold text-slate-900 uppercase tracking-tight">{t(language, 'lbl_bis_guidance')}</h1>
            <p className="text-slate-600 text-[14px] mt-1">{t(language, 'lbl_bis_guidance_sub')}</p>
          </div>
          <div className="mt-4 sm:mt-0 flex bg-slate-200 p-1 rounded-md">
            <button
              onClick={() => setMode('industry')}
              className={`px-4 py-1.5 text-xs font-bold uppercase tracking-wider rounded-sm transition-colors ${mode === 'industry' ? 'bg-white shadow-sm text-navy-900' : 'text-slate-500 hover:text-navy-700'}`}
            >
              {t(language, 'lbl_industry_mode')}
            </button>
            <button
              onClick={() => setMode('consumer')}
              className={`px-4 py-1.5 text-xs font-bold uppercase tracking-wider rounded-sm transition-colors ${mode === 'consumer' ? 'bg-white shadow-sm text-navy-900' : 'text-slate-500 hover:text-navy-700'}`}
            >
              {t(language, 'lbl_consumer_mode')}
            </button>
          </div>
        </div>

        <div className="bg-white border border-slate-300 rounded-sm p-6 shadow-sm mb-8">
          <label className="block text-sm font-bold text-slate-800 mb-2 uppercase tracking-wider">{t(language, 'lbl_question')}</label>
          <div className="flex flex-col sm:flex-row gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && send()}
              placeholder={t(language, 'lbl_ask_placeholder')}
              className="flex-1 min-w-0 border border-slate-300 rounded-sm px-4 py-3 text-[15px] text-slate-900 placeholder-slate-400 focus:outline-none focus:border-navy-600 focus:ring-1 focus:ring-navy-600 h-[48px]"
            />
            <div className="flex gap-2 shrink-0">
              <VoiceAssistant
                language={language}
                isProcessingRetrieval={loading}
                ttsResponse={ttsResponse}
                onTextRecognized={(text) => {
                  setInput(text);
                  send(text);
                }}
                className="h-[48px] px-4 bg-slate-50 border border-slate-300 hover:bg-slate-100 rounded-sm text-navy-700 font-medium flex items-center justify-center transition-colors"
              />
              <button
                onClick={() => send()}
                disabled={loading}
                className="bg-navy-800 hover:bg-navy-900 disabled:opacity-50 text-white font-medium px-8 rounded-sm transition-colors whitespace-nowrap h-[48px]"
              >
                {loading ? t(language, 'lbl_processing') : t(language, 'lbl_ask')}
              </button>
            </div>
          </div>
          <div className="mt-4 flex flex-wrap gap-2">
            {suggested.map((q) => (
              <button
                key={q}
                onClick={() => { setInput(q); send(q); }}
                disabled={loading}
                className="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium rounded-full px-3 py-1.5 transition-colors disabled:opacity-50"
              >
                {q}
              </button>
            ))}
          </div>
        </div>

        {error && <p className="text-sm text-red-600 mb-6 bg-red-50 p-4 rounded-md border border-red-100">{error}</p>}

        {loading && (
          <div className="bg-white border border-slate-200 rounded-lg p-10 flex justify-center items-center">
            <div className="flex gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-navy-400 animate-pulse" />
              <span className="w-2.5 h-2.5 rounded-full bg-navy-400 animate-pulse [animation-delay:0.15s]" />
              <span className="w-2.5 h-2.5 rounded-full bg-navy-400 animate-pulse [animation-delay:0.3s]" />
            </div>
          </div>
        )}

        {notFound && !loading && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-8 text-center">
            <h3 className="text-red-800 font-bold mb-2 uppercase tracking-wider text-sm">{t(language, 'lbl_no_match')}</h3>
            <p className="text-red-700 text-[14px]">
              {t(language, 'no_verified_match')}
            </p>
          </div>
        )}

        {result && (
          <div className="flex flex-col w-full max-w-[1200px] items-start mb-8">
            <div className="flex flex-col lg:flex-row gap-6 w-full">
              {result.intent === 'COMPLAINT' ? (
                <ComplaintCopilot message={result} language={language} />
              ) : result.intent === 'MSME_COPILOT' ? (
                <MsmeComplianceRoadmap data={result} language={language} />
              ) : (
                <DecisionCard message={result} language={language} />
              )}
            </div>

            {/* PHASE 15: BIS ECOSYSTEM ROUTER */}
            <EcosystemRouter message={result} language={language} />
          </div>
        )}
      </div>
    </div>
  )
}
