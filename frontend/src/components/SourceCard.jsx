import { t } from '../i18n.js'

export default function SourceCard({ sources, language }) {
  if (!sources || sources.length === 0) return null
  return (
    <div className="mt-3 border border-navy-100 bg-navy-50/60 rounded-lg p-3.5">
      <p className="text-[11px] font-semibold uppercase tracking-wide text-navy-500 mb-2">
        {t(language, 'source_label')}
      </p>
      <div className="space-y-2.5">
        {sources.map((s, idx) => (
          <div key={idx} className="flex items-start gap-2.5">
            <svg className="mt-0.5 shrink-0" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#2c5490" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 19.5A2.5 2.5 0 0 0 6.5 22H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15Z" />
            </svg>
            <div className="min-w-0">
              <p className="text-sm font-medium text-navy-800">
                {s.title} <span className="font-mono text-xs text-navy-500">({s.standard_number})</span>
              </p>
              <p className="text-xs text-navy-500">
                {s.source_name}
                {s.source_url && (
                  <>
                    {' · '}
                    <a href={s.source_url} target="_blank" rel="noreferrer" className="text-navy-600 underline underline-offset-2 hover:text-navy-800">
                      {s.source_url.replace(/^https?:\/\//, '')}
                    </a>
                  </>
                )}
              </p>
            </div>
            {s.verified && (
              <span className="ml-auto shrink-0 text-[10px] font-semibold bg-white text-navy-600 border border-navy-200 rounded-full px-2 py-0.5 whitespace-nowrap">
                {t(language, 'verified_label')}
              </span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
