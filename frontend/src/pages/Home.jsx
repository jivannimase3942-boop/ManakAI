import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ServiceCard from '../components/ServiceCard.jsx'
import { t, EXAMPLE_QUESTIONS } from '../i18n.js'
import { api } from '../api.js'

const STEP_KEYS = ['step1', 'step2', 'step3', 'step4', 'step5', 'step6']

export default function Home({ language }) {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const [services, setServices] = useState([])

  useEffect(() => {
    api.services().then(setServices).catch(() => {})
  }, [])

  function goAsk(q) {
    const val = q ?? query
    if (!val.trim()) return
    navigate('/assistant', { state: { prefill: val } })
  }

  return (
    <div>
      {/* Prototype banner */}
      <div className="bg-navy-900 text-navy-50 text-xs sm:text-[13px] text-center px-4 py-2">
        {t(language, 'prototype_banner')}
      </div>

      {/* Hero */}
      <section className="bg-white border-b border-navy-100">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-14 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-navy-50 border border-navy-100 text-navy-600 text-xs font-medium mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-saffron-500" />
            SIH 2026 · SIH26107
          </div>
          <h1 className="text-3xl sm:text-5xl font-extrabold text-navy-900 tracking-tight leading-tight max-w-3xl mx-auto">
            {t(language, 'hero_title')}
          </h1>
          <p className="mt-5 text-navy-600 text-base sm:text-lg max-w-2xl mx-auto leading-relaxed">
            {t(language, 'hero_sub')}
          </p>

          <div className="mt-9 max-w-2xl mx-auto">
            <div className="flex flex-col sm:flex-row items-stretch gap-2 bg-white border border-navy-200 rounded-xl p-1.5 shadow-card focus-within:ring-2 focus-within:ring-navy-500">
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && goAsk()}
                placeholder={t(language, 'search_placeholder')}
                className="flex-1 px-3.5 py-2.5 text-[15px] text-navy-900 placeholder-navy-400 focus:outline-none bg-transparent"
              />
              <button
                onClick={() => goAsk()}
                className="bg-navy-700 hover:bg-navy-800 text-white font-semibold text-sm px-5 py-2.5 rounded-lg transition-colors whitespace-nowrap"
              >
                {t(language, 'hero_cta')}
              </button>
            </div>
            <div className="mt-4 flex flex-wrap justify-center gap-2">
              {EXAMPLE_QUESTIONS[language].slice(0, 3).map((q) => (
                <button
                  key={q}
                  onClick={() => goAsk(q)}
                  className="text-xs sm:text-[13px] bg-navy-50 hover:bg-navy-100 text-navy-700 rounded-full px-3.5 py-1.5 transition-colors"
                >
                  {q}
                </button>
              ))}
            </div>
            <button
              onClick={() => navigate('/finder')}
              className="mt-5 text-sm font-medium text-navy-600 hover:text-navy-800 underline underline-offset-4"
            >
              {t(language, 'hero_cta_secondary')} →
            </button>
          </div>
        </div>
      </section>

      {/* Services */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center max-w-xl mx-auto mb-10">
          <h2 className="text-2xl sm:text-3xl font-bold text-navy-900">{t(language, 'services_heading')}</h2>
          <p className="mt-2.5 text-navy-600 text-[15px]">{t(language, 'services_sub')}</p>
        </div>
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {services.map((s) => (
            <ServiceCard
              key={s.id}
              name={s.name}
              description={s.description}
              icon={s.icon}
              onClick={() => navigate('/services', { state: { focus: s.id } })}
            />
          ))}
        </div>
      </section>

      {/* How it works */}
      <section className="bg-navy-900 text-white">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center max-w-xl mx-auto mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold">{t(language, 'how_heading')}</h2>
            <p className="mt-2.5 text-navy-300 text-[15px]">{t(language, 'how_sub')}</p>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-6 gap-4">
            {STEP_KEYS.map((key, i) => (
              <div key={key} className="relative">
                <div className="bg-navy-800/70 border border-navy-700 rounded-xl p-4 h-full">
                  <span className="font-mono text-[11px] text-saffron-500 font-semibold">0{i + 1}</span>
                  <h3 className="mt-2 font-semibold text-sm text-white leading-snug">{t(language, `${key}_t`)}</h3>
                  <p className="mt-1.5 text-xs text-navy-300 leading-relaxed">{t(language, `${key}_d`)}</p>
                </div>
                {i < STEP_KEYS.length - 1 && (
                  <div className="hidden lg:block absolute top-1/2 -right-2.5 -translate-y-1/2 text-navy-600 text-lg">›</div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  )
}
