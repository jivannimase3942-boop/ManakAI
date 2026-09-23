import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { t } from '../i18n.js'
import VoiceAssistant from '../components/VoiceAssistant.jsx'

export default function Home({ language }) {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')

  const handleSearch = (e) => {
    if (e) e.preventDefault()
    if (search.trim()) {
      navigate('/assistant', { state: { prefill: search } })
    }
  }

  const handleVoiceRecognized = (text) => {
    setSearch(text);
    navigate('/assistant', { state: { prefill: text } });
  };

  const officialSources = [
    { name: "BIS Product Certification", url: "https://www.bis.gov.in/certification/product-certification-scheme/" },
    { name: "BIS CRS Portal", url: "https://crsbis.in/BIS/products.do" },
    { name: "BIS Hallmarking", url: "https://www.bis.gov.in/hallmarking/" },
    { name: "BIS Consumer Corner", url: "https://www.bis.gov.in/consumer-corner/" }
  ];

  return (
    <div className="bg-[#fcfcfc] min-h-screen font-sans text-slate-800">

      {/* 1. HERO SECTION */}
      <section className="bg-tech-pattern border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-3xl sm:text-4xl font-extrabold text-[#0B1E40] tracking-tight leading-tight mb-4">
              {t(language, 'hero_title_new')}
            </h1>
            <p className="text-base text-slate-600 mb-8 max-w-2xl mx-auto leading-relaxed">
              {t(language, 'hero_sub_new')}
            </p>
            <form onSubmit={handleSearch} className="flex flex-col sm:flex-row gap-2 max-w-3xl mx-auto justify-center mb-4">
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder={t(language, 'search_placeholder_new')}
                className="flex-1 min-w-0 border border-slate-300 rounded-sm px-4 py-3 text-[15px] text-slate-900 placeholder-slate-400 focus:outline-none focus:border-[#1C4E80] focus:ring-1 focus:ring-[#1C4E80] h-[48px] shadow-sm"
              />
              <div className="flex flex-col sm:flex-row gap-2 shrink-0 w-full sm:w-auto">
                <VoiceAssistant
                  language={language}
                  onTextRecognized={handleVoiceRecognized}
                  onTranscriptChange={setSearch}
                  className="h-[48px] w-full sm:w-auto px-4 bg-slate-50 border border-slate-300 hover:bg-slate-100 rounded-sm text-[#1C4E80] font-medium flex items-center justify-center transition-colors shadow-sm"
                />
                <button type="submit" className="w-full sm:w-auto bg-[#0B1E40] hover:bg-[#152F5A] text-white font-semibold px-8 rounded-sm transition-colors h-[48px] shadow-sm">
                  {t(language, 'lbl_search')}
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>

      {/* 1.5. SCANNER CTA SECTION */}
      <section className="bg-white border-b border-slate-200 py-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-[14px] font-bold text-[#0B1E40] mb-2 uppercase tracking-wider">{language === 'hi' ? 'उत्पाद स्कैन करें' : language === 'mr' ? 'उत्पादन स्कॅन करा' : 'SCAN A PRODUCT'}</h2>
          <p className="text-[14px] text-slate-600 mb-6 max-w-2xl mx-auto">
            {language === 'hi' ? 'प्रासंगिक BIS मानक और अनुपालन मार्ग पहचानने के लिए उत्पाद लेबल स्कैन करें।' : language === 'mr' ? 'संबंधित BIS मानक आणि अनुपालन मार्ग ओळखण्यासाठी उत्पादन लेबल स्कॅन करा.' : 'Scan a product label to identify the relevant BIS standard and compliance pathway.'}
          </p>
          <button 
            onClick={() => navigate('/scan')}
            className="inline-flex items-center gap-2 bg-[#E08A2C] hover:bg-[#c97a24] text-white font-bold py-3 px-8 rounded-sm transition-colors shadow-sm"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            {language === 'hi' ? 'उत्पाद स्कैन करें' : language === 'mr' ? 'उत्पादन स्कॅन करा' : 'Scan Product'}
          </button>
        </div>
      </section>

      {/* 2. VALUE STRIP */}
      <section className="bg-slate-50 border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 divide-y md:divide-y-0 md:divide-x divide-slate-200">
            <div className="px-4 py-2 text-center md:text-left">
              <h3 className="text-[12px] font-bold text-[#1C4E80] uppercase tracking-wider mb-1">{t(language, 'val_standards')}</h3>
              <p className="text-[13px] text-slate-600 font-medium">{t(language, 'val_standards_desc')}</p>
            </div>
            <div className="px-4 py-2 text-center md:text-left">
              <h3 className="text-[12px] font-bold text-[#1C4E80] uppercase tracking-wider mb-1">{t(language, 'val_services')}</h3>
              <p className="text-[13px] text-slate-600 font-medium">{t(language, 'val_services_desc')}</p>
            </div>
            <div className="px-4 py-2 text-center md:text-left">
              <h3 className="text-[12px] font-bold text-[#E08A2C] uppercase tracking-wider mb-1">{t(language, 'val_evidence')}</h3>
              <p className="text-[13px] text-slate-600 font-medium">{t(language, 'val_evidence_desc')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* 3. GUIDANCE GRID */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 className="text-[14px] font-bold text-[#0B1E40] mb-8 uppercase tracking-wider">{t(language, 'guidance_title')}</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[
            {
              title: t(language, 'srv_card1_t'),
              desc: t(language, 'srv_card1_d'),
              route: '/finder'
            },
            {
              title: t(language, 'srv_card2_t'),
              desc: t(language, 'srv_card2_d'),
              route: '/assistant', state: { prefill: 'I need BIS certification' }
            },
            {
              title: t(language, 'srv_card3_t'),
              desc: t(language, 'srv_card3_d'),
              route: '/assistant', state: { prefill: 'I need testing guidance' }
            },
            {
              title: t(language, 'srv_card4_t'),
              desc: t(language, 'srv_card4_d'),
              route: '/assistant', state: { prefill: 'Tell me about hallmarking of gold and silver' }
            },
            {
              title: t(language, 'srv_card5_t'),
              desc: t(language, 'srv_card5_d'),
              route: '/consumer'
            },
            {
              title: t(language, 'srv_card6_t'),
              desc: t(language, 'srv_card6_d'),
              route: '/industry'
            }
          ].map((item, idx) => (
            <div
              key={idx}
              onClick={() => navigate(item.route, { state: item.state })}
              className="bg-white border border-slate-200 rounded-sm p-5 hover:border-[#1C4E80] transition-colors cursor-pointer shadow-sm group"
            >
              <h3 className="text-[15px] font-bold text-[#0B1E40] mb-2 flex justify-between items-center">
                {item.title}
                <span className="text-slate-300 group-hover:text-[#1C4E80] transition-colors">→</span>
              </h3>
              <p className="text-[13px] text-slate-600 leading-relaxed">
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      {/* 4. CORE JOURNEY & 5. WHY MANAKAI */}
      <section className="bg-white border-y border-slate-200 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16">

            {/* Core Journey */}
            <div>
              <h2 className="text-[14px] font-bold text-[#0B1E40] mb-8 uppercase tracking-wider">{t(language, 'journey_title_new')}</h2>
              <div className="space-y-3 relative before:absolute before:inset-0 before:ml-[11px] before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-slate-200 before:to-transparent">
                {[
                  { n: '01', l: t(language, 'journey_q') },
                  { n: '02', l: t(language, 'journey_i') },
                  { n: '03', l: t(language, 'journey_s') },
                  { n: '04', l: t(language, 'journey_e') },
                  { n: '05', l: t(language, 'journey_n') },
                  { n: '06', l: t(language, 'journey_o') }
                ].map((step, i) => (
                  <div key={i} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                    <div className="flex items-center justify-center w-6 h-6 rounded-full border border-slate-300 bg-white text-[10px] font-bold text-slate-500 shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-sm">
                      {step.n}
                    </div>
                    <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] px-4 py-2 rounded-sm border border-slate-200 bg-slate-50 text-[13px] font-bold text-[#1C4E80] shadow-sm">
                      {step.l}
                    </div>
                  </div>
                ))}
              </div>
              <p className="mt-8 text-[13px] text-slate-500 italic text-center md:text-left">
                {t(language, 'journey_desc')}
              </p>
            </div>

            {/* Why ManakAI */}
            <div>
              <h2 className="text-[14px] font-bold text-[#0B1E40] mb-8 uppercase tracking-wider">{t(language, 'why_title')}</h2>

              <div className="mb-6">
                <h3 className="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-3">{t(language, 'why_trad_title')}</h3>
                <div className="bg-slate-50 border border-slate-200 rounded-sm p-4 text-[13px] text-slate-600 font-medium">
                  <div className="flex flex-col gap-2">
                    <span className="opacity-70">→ {t(language, 'why_trad_1')}</span>
                    <span className="opacity-70">→ {t(language, 'why_trad_2')}</span>
                    <span className="opacity-70">→ {t(language, 'why_trad_3')}</span>
                    <span className="opacity-70">→ {t(language, 'why_trad_4')}</span>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-[11px] font-bold text-[#E08A2C] uppercase tracking-wider mb-3">{t(language, 'why_man_title')}</h3>
                <div className="bg-[#f8fcfd] border border-[#1C4E80]/20 rounded-sm p-4 text-[13px] text-[#0B1E40] font-bold shadow-sm">
                  <div className="flex flex-col gap-3">
                    <span className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#1C4E80]"></span>{t(language, 'why_man_1')}</span>
                    <span className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#1C4E80]"></span>{t(language, 'why_man_2')}</span>
                    <span className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#1C4E80]"></span>{t(language, 'why_man_3')}</span>
                    <span className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#1C4E80]"></span>{t(language, 'why_man_4')}</span>
                    <span className="flex items-center gap-2"><span className="w-1.5 h-1.5 rounded-full bg-[#E08A2C]"></span>{t(language, 'why_man_5')}</span>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </section>

      {/* 6. EVIDENCE / TRUST */}
      <section className="bg-slate-900 text-slate-300 py-16 border-b border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-[14px] font-bold text-slate-100 mb-10 uppercase tracking-wider text-center">{t(language, 'ev_title')}</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center md:text-left">
            <div>
              <div className="w-10 h-10 rounded-sm bg-slate-800 border border-slate-700 flex items-center justify-center mb-4 mx-auto md:mx-0">
                <span className="text-cyan-400 font-bold">✓</span>
              </div>
              <h3 className="text-[13px] font-bold text-slate-100 uppercase tracking-wider mb-2">{t(language, 'ev_1_t')}</h3>
              <p className="text-[13px] leading-relaxed">{t(language, 'ev_1_d')}</p>
            </div>
            <div>
              <div className="w-10 h-10 rounded-sm bg-slate-800 border border-slate-700 flex items-center justify-center mb-4 mx-auto md:mx-0">
                <span className="text-amber-400 font-bold">!</span>
              </div>
              <h3 className="text-[13px] font-bold text-slate-100 uppercase tracking-wider mb-2">{t(language, 'ev_2_t')}</h3>
              <p className="text-[13px] leading-relaxed">{t(language, 'ev_2_d')}</p>
            </div>
            <div>
              <div className="w-10 h-10 rounded-sm bg-slate-800 border border-slate-700 flex items-center justify-center mb-4 mx-auto md:mx-0">
                <span className="text-emerald-400 font-bold">→</span>
              </div>
              <h3 className="text-[13px] font-bold text-slate-100 uppercase tracking-wider mb-2">{t(language, 'ev_3_t')}</h3>
              <p className="text-[13px] leading-relaxed">{t(language, 'ev_3_d')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* 7. OFFICIAL SOURCES */}
      <section className="bg-slate-50 py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-[14px] font-bold text-[#0B1E40] mb-8 uppercase tracking-wider text-center">{t(language, 'os_title')}</h2>
          <div className="flex flex-wrap justify-center gap-4 max-w-4xl mx-auto">
            {officialSources.map((src, idx) => (
              <a
                key={idx}
                href={src.url}
                target="_blank"
                rel="noreferrer"
                className="bg-white border border-slate-200 rounded-sm px-6 py-4 hover:border-[#1C4E80] transition-colors shadow-sm flex items-center gap-4 group"
              >
                <div className="flex-col">
                  <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">{t(language, 'os_bis')} {t(language, 'os_official')}</span>
                  <span className="text-[14px] font-bold text-[#0B1E40]">{src.name}</span>
                </div>
                <span className="text-[11px] font-bold text-[#1C4E80] opacity-0 group-hover:opacity-100 transition-opacity ml-2">
                  {t(language, 'os_open')}
                </span>
              </a>
            ))}
          </div>
        </div>
      </section>

    </div>
  )
}
