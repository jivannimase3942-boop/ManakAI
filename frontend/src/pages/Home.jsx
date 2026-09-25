import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { t } from '../i18n.js'
import VoiceAssistant from '../components/VoiceAssistant.jsx'

const audienceCards = [
  { key: 'industry', icon: '▦', route: '/industry', color: 'border-[#1C4E80] bg-[#F4F8FC]' },
  { key: 'msme', icon: '◈', route: '/msme', color: 'border-[#4E7A63] bg-[#F4FAF5]' },
  { key: 'consumer', icon: '✓', route: '/consumer', color: 'border-[#E08A2C] bg-[#FFF9F1]' },
]

const popularActions = [
  { key: 'standard', route: '/finder' },
  { key: 'certification', route: '/services?feature=certification' },
  { key: 'testing', route: '/services?feature=testing' },
  { key: 'hallmarking', route: '/services?feature=hallmarking' },
  { key: 'compliance', route: '/consumer' },
  { key: 'alerts', route: '/consumer' },
]

function Icon({ children, className = '' }) {
  return <span aria-hidden="true" className={`inline-flex items-center justify-center ${className}`}>{children}</span>
}

export default function Home({ language }) {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')

  const handleSearch = (event) => {
    event.preventDefault()
    if (search.trim()) navigate('/assistant', { state: { prefill: search.trim() } })
  }

  const cards = audienceCards.map((card) => ({
    ...card,
    title: t(language, `home_${card.key}_title`),
    description: t(language, `home_${card.key}_desc`),
    features: t(language, `home_${card.key}_features`).split('|'),
    action: t(language, `home_${card.key}_action`),
  }))

  return (
    <div className="min-h-screen bg-[#F7F9FC] text-slate-800">
      <section className="border-b border-slate-200 bg-[#EEF3F8]">
        <div className="mx-auto max-w-[1360px] px-5 py-14 sm:px-8 lg:px-12 lg:py-16">
          <div className="grid items-center gap-10 lg:grid-cols-[1.1fr_0.9fr]">
            <div className="max-w-3xl">
              <p className="mb-4 text-xs font-bold uppercase tracking-[0.2em] text-[#1C4E80]">ManakAI / BIS guidance platform</p>
              <h1 className="max-w-3xl text-4xl font-extrabold leading-tight tracking-tight text-[#0B1E40] sm:text-5xl">{t(language, 'hero_title_new')}</h1>
              <p className="mt-5 max-w-2xl text-base leading-7 text-slate-600">{t(language, 'hero_sub_new')}</p>
              <div className="mt-7 flex flex-wrap gap-3">
                <button onClick={() => navigate('/finder')} className="min-h-11 bg-[#0B1E40] px-5 py-3 text-sm font-bold text-white shadow-sm hover:bg-[#152F5A]">{t(language, 'nav_finder')}</button>
                <button onClick={() => navigate('/scan')} className="min-h-11 border border-[#E08A2C] bg-white px-5 py-3 text-sm font-bold text-[#A85D10] hover:bg-orange-50">{t(language, 'home_scan_title')}</button>
              </div>
            </div>
            <div className="relative min-h-[230px] overflow-hidden border border-[#C8D5E3] bg-white p-7 shadow-sm">
              <div className="absolute right-0 top-0 h-28 w-28 border-l border-b border-[#D7E2ED] bg-[#F8FBFD]" />
              <div className="relative flex h-full flex-col justify-between">
                <div><p className="text-xs font-bold uppercase tracking-[0.16em] text-[#E08A2C]">Evidence-led</p><h2 className="mt-3 max-w-xs text-2xl font-bold text-[#0B1E40]">Find a clear path through standards and services.</h2></div>
                <div className="mt-8 flex items-center gap-3 text-sm font-semibold text-[#1C4E80]"><span className="h-2 w-2 bg-[#E08A2C]" /> Verified sources, explicit next actions</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <main className="mx-auto max-w-[1360px] px-5 py-12 sm:px-8 lg:px-12">
        <section>
          <div className="flex flex-col justify-between gap-3 sm:flex-row sm:items-end"><div><p className="text-xs font-bold uppercase tracking-[0.18em] text-[#1C4E80]">Choose your path</p><h2 className="mt-2 text-2xl font-extrabold text-[#0B1E40]">How can ManakAI help?</h2></div><p className="max-w-md text-sm leading-6 text-slate-500">Start with the route that matches your role. Each path keeps its own guidance and next actions.</p></div>
          <div className="mt-6 grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
            {cards.map((card) => <article key={card.key} className={`flex min-h-[290px] flex-col border p-6 shadow-sm transition-shadow hover:shadow-md ${card.color}`}>
              <Icon className="h-11 w-11 border border-current text-xl font-bold text-[#1C4E80]">{card.icon}</Icon>
              <h3 className="mt-5 text-xl font-extrabold text-[#0B1E40]">{card.title}</h3>
              <p className="mt-2 text-sm leading-6 text-slate-600">{card.description}</p>
              <ul className="mt-4 space-y-2 text-sm text-slate-700">{card.features.map((feature) => <li key={feature} className="flex gap-2"><span className="font-bold text-[#1C4E80]">✓</span>{feature}</li>)}</ul>
              <button onClick={() => navigate(card.route)} className="mt-auto pt-6 text-left text-sm font-bold text-[#1C4E80] hover:underline">{card.action} <span aria-hidden="true">→</span></button>
            </article>)}
          </div>
        </section>

        <section className="mt-12 border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <div className="grid gap-6 lg:grid-cols-[0.8fr_1.2fr] lg:items-center"><div><p className="text-xs font-bold uppercase tracking-[0.18em] text-[#E08A2C]">Search</p><h2 className="mt-2 text-2xl font-extrabold text-[#0B1E40]">{t(language, 'home_search_title')}</h2><p className="mt-3 text-sm leading-6 text-slate-500">{t(language, 'home_search_examples')}</p></div><form onSubmit={handleSearch} className="flex flex-col gap-3 sm:flex-row"><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder={t(language, 'search_placeholder_new')} className="min-h-12 min-w-0 flex-1 border border-slate-300 px-4 text-sm text-slate-900 outline-none focus:border-[#1C4E80] focus:ring-2 focus:ring-[#DCE8F3]" /><VoiceAssistant language={language} onTextRecognized={(text) => { setSearch(text); navigate('/assistant', { state: { prefill: text } }) }} onTranscriptChange={setSearch} className="min-h-12 border border-slate-300 bg-slate-50 px-5 text-sm font-bold text-[#1C4E80]" /><button type="submit" className="min-h-12 bg-[#0B1E40] px-7 text-sm font-bold text-white hover:bg-[#152F5A]">{t(language, 'lbl_search')}</button></form></div>
        </section>

        <section className="mt-8 border border-[#B9CBDD] bg-[#EAF2F8] p-6 shadow-sm sm:p-8"><div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between"><div><p className="text-xs font-bold uppercase tracking-[0.2em] text-[#1C4E80]">{t(language, 'home_scan_title')}</p><h2 className="mt-2 text-2xl font-extrabold text-[#0B1E40]">{t(language, 'home_scan_desc')}</h2><p className="mt-2 max-w-2xl text-sm leading-6 text-slate-600">Identification and verified BIS information are shown separately. Uncertain images stay uncertain.</p></div><div className="flex shrink-0 flex-col gap-3 sm:flex-row"><button onClick={() => navigate('/scan')} className="inline-flex min-h-12 items-center justify-center gap-2 bg-[#0B1E40] px-6 text-sm font-bold text-white hover:bg-[#152F5A]"><Icon className="text-lg">⌾</Icon>{t(language, 'home_scan_camera')}</button><button onClick={() => navigate('/scan')} className="inline-flex min-h-12 items-center justify-center gap-2 border border-[#1C4E80] bg-white px-6 text-sm font-bold text-[#1C4E80] hover:bg-[#F7FBFF]"><Icon className="text-lg">□</Icon>{t(language, 'home_scan_upload')}</button></div></div></section>

        <section className="mt-10"><div className="flex items-center justify-between"><h2 className="text-xl font-extrabold text-[#0B1E40]">{t(language, 'home_popular_title')}</h2><button onClick={() => navigate('/services')} className="text-sm font-bold text-[#1C4E80] hover:underline">{t(language, 'nav_services')} →</button></div><div className="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3">{popularActions.map((action) => <button key={action.key} onClick={() => navigate(action.route)} className="flex min-h-14 items-center justify-between border border-slate-200 bg-white px-4 text-left text-sm font-bold text-slate-700 shadow-sm hover:border-[#1C4E80] hover:text-[#1C4E80]"><span>{t(language, `home_popular_${action.key}`)}</span><span aria-hidden="true" className="text-[#E08A2C]">→</span></button>)}</div></section>
      </main>
    </div>
  )
}
