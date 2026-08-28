import { useEffect, useState } from 'react'
import { t } from '../i18n.js'
import { api } from '../api.js'

export default function About({ language }) {
  const [sources, setSources] = useState([])

  useEffect(() => {
    api.sources().then(setSources).catch(() => {})
  }, [])

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-2xl font-bold text-navy-900">{t(language, 'about_title')}</h1>
      <p className="text-navy-600 text-sm mt-1.5">{t(language, 'about_sub')}</p>

      <div className="mt-6 space-y-4 text-[15px] text-navy-700 leading-relaxed">
        <p>{t(language, 'about_p1')}</p>
        <p>{t(language, 'about_p2')}</p>
        <p>{t(language, 'about_p3')}</p>
      </div>

      <div className="mt-8 bg-navy-900 text-white rounded-2xl p-5">
        <h2 className="font-semibold text-sm mb-1.5">{t(language, 'disclaimer_heading')}</h2>
        <p className="text-navy-200 text-sm leading-relaxed">{t(language, 'disclaimer_text')}</p>
      </div>

      <h2 className="mt-10 text-lg font-bold text-navy-900">{t(language, 'about_sources_heading')}</h2>
      <div className="mt-4 divide-y divide-navy-100 border border-navy-100 rounded-xl overflow-hidden bg-white">
        {sources.map((s, i) => (
          <div key={i} className="p-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
            <div>
              <p className="text-sm font-medium text-navy-800">{s.title}</p>
              <p className="text-xs text-navy-500 font-mono">{s.standard_number}</p>
            </div>
            <a
              href={s.source_url}
              target="_blank"
              rel="noreferrer"
              className="text-xs text-navy-600 underline underline-offset-2 hover:text-navy-800"
            >
              {s.source_name}
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}
