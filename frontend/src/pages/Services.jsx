import { useNavigate } from 'react-router-dom'
import { t } from '../i18n.js'

export default function Services({ language }) {
  const navigate = useNavigate()

  return (
    <div className="bg-[#fcfcfc] min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-3xl sm:text-4xl font-extrabold text-[#0B1E40] mb-4 tracking-tight uppercase">{t(language, 'srv_title')}</h1>
        <p className="text-slate-600 mb-12 text-[15px] max-w-3xl leading-relaxed">
          {t(language, 'srv_sub')}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">

          <div className="bg-white border-t-4 border-[#0B1E40] border-x border-b border-slate-200 p-6 shadow-sm flex flex-col hover:shadow-md transition-shadow">
            <h2 className="text-[#0B1E40] font-extrabold text-[15px] mb-3 uppercase tracking-wider">{t(language, 'srv_card1_t')}</h2>
            <p className="text-slate-600 text-[13px] mb-6 flex-1 leading-relaxed">{t(language, 'srv_card1_d')}</p>
            <button onClick={() => navigate('/finder')} className="text-left text-white bg-[#1C4E80] hover:bg-[#0B1E40] text-[12px] font-bold uppercase tracking-wider py-2 px-4 rounded-sm transition-colors mt-auto">
              {t(language, 'srv_card1_b')}
            </button>
          </div>

          <div className="bg-white border-t-4 border-[#1C4E80] border-x border-b border-slate-200 p-6 shadow-sm flex flex-col hover:shadow-md transition-shadow">
            <h2 className="text-[#0B1E40] font-extrabold text-[15px] mb-3 uppercase tracking-wider">{t(language, 'srv_card2_t')}</h2>
            <p className="text-slate-600 text-[13px] mb-6 flex-1 leading-relaxed">{t(language, 'srv_card2_d')}</p>
            <button onClick={() => navigate('/assistant', { state: { prefill: t(language, 'pf_srv_cert') } })} className="text-left text-[#1C4E80] border border-[#1C4E80] hover:bg-slate-50 text-[12px] font-bold uppercase tracking-wider py-2 px-4 rounded-sm transition-colors mt-auto">
              {t(language, 'srv_card2_b')}
            </button>
          </div>

          <div className="bg-white border-t-4 border-[#1C4E80] border-x border-b border-slate-200 p-6 shadow-sm flex flex-col hover:shadow-md transition-shadow">
            <h2 className="text-[#0B1E40] font-extrabold text-[15px] mb-3 uppercase tracking-wider">{t(language, 'srv_card3_t')}</h2>
            <p className="text-slate-600 text-[13px] mb-6 flex-1 leading-relaxed">{t(language, 'srv_card3_d')}</p>
            <button onClick={() => navigate('/assistant', { state: { prefill: t(language, 'pf_srv_test') } })} className="text-left text-[#1C4E80] border border-[#1C4E80] hover:bg-slate-50 text-[12px] font-bold uppercase tracking-wider py-2 px-4 rounded-sm transition-colors mt-auto">
              {t(language, 'srv_card3_b')}
            </button>
          </div>

          <div className="bg-white border-t-4 border-[#1C4E80] border-x border-b border-slate-200 p-6 shadow-sm flex flex-col hover:shadow-md transition-shadow">
            <h2 className="text-[#0B1E40] font-extrabold text-[15px] mb-3 uppercase tracking-wider">{t(language, 'srv_card4_t')}</h2>
            <p className="text-slate-600 text-[13px] mb-6 flex-1 leading-relaxed">{t(language, 'srv_card4_d')}</p>
            <button onClick={() => navigate('/assistant', { state: { prefill: t(language, 'pf_srv_hm') } })} className="text-left text-[#1C4E80] border border-[#1C4E80] hover:bg-slate-50 text-[12px] font-bold uppercase tracking-wider py-2 px-4 rounded-sm transition-colors mt-auto">
              {t(language, 'srv_card4_b')}
            </button>
          </div>

          <div className="bg-white border-t-4 border-[#E08A2C] border-x border-b border-slate-200 p-6 shadow-sm flex flex-col hover:shadow-md transition-shadow">
            <h2 className="text-[#0B1E40] font-extrabold text-[15px] mb-3 uppercase tracking-wider">{t(language, 'srv_card5_t')}</h2>
            <p className="text-slate-600 text-[13px] mb-6 flex-1 leading-relaxed">{t(language, 'srv_card5_d')}</p>
            <button onClick={() => navigate('/consumer')} className="text-left text-[#E08A2C] border border-[#E08A2C] hover:bg-orange-50 text-[12px] font-bold uppercase tracking-wider py-2 px-4 rounded-sm transition-colors mt-auto">
              {t(language, 'srv_card5_b')}
            </button>
          </div>

          <div className="bg-white border-t-4 border-[#E08A2C] border-x border-b border-slate-200 p-6 shadow-sm flex flex-col hover:shadow-md transition-shadow">
            <h2 className="text-[#0B1E40] font-extrabold text-[15px] mb-3 uppercase tracking-wider">{t(language, 'srv_card6_t')}</h2>
            <p className="text-slate-600 text-[13px] mb-6 flex-1 leading-relaxed">{t(language, 'srv_card6_d')}</p>
            <button onClick={() => navigate('/industry')} className="text-left text-[#E08A2C] border border-[#E08A2C] hover:bg-orange-50 text-[12px] font-bold uppercase tracking-wider py-2 px-4 rounded-sm transition-colors mt-auto">
              {t(language, 'srv_card6_b')}
            </button>
          </div>

          <div className="bg-white border-t-4 border-slate-400 border-x border-b border-slate-200 p-6 shadow-sm flex flex-col hover:shadow-md transition-shadow">
            <h2 className="text-[#0B1E40] font-extrabold text-[15px] mb-3 uppercase tracking-wider">{t(language, 'srv_card7_t')}</h2>
            <p className="text-slate-600 text-[13px] mb-6 flex-1 leading-relaxed">{t(language, 'srv_card7_d')}</p>
            <button onClick={() => navigate('/assistant', { state: { prefill: t(language, 'pf_srv_sch') } })} className="text-left text-slate-600 border border-slate-300 hover:bg-slate-50 text-[12px] font-bold uppercase tracking-wider py-2 px-4 rounded-sm transition-colors mt-auto">
              {t(language, 'srv_card7_b')}
            </button>
          </div>

          <div className="bg-white border-t-4 border-slate-400 border-x border-b border-slate-200 p-6 shadow-sm flex flex-col hover:shadow-md transition-shadow">
            <h2 className="text-[#0B1E40] font-extrabold text-[15px] mb-3 uppercase tracking-wider">{t(language, 'srv_card8_t')}</h2>
            <p className="text-slate-600 text-[13px] mb-6 flex-1 leading-relaxed">{t(language, 'srv_card8_d')}</p>
            <button onClick={() => navigate('/assistant', { state: { prefill: t(language, 'pf_srv_safe') } })} className="text-left text-slate-600 border border-slate-300 hover:bg-slate-50 text-[12px] font-bold uppercase tracking-wider py-2 px-4 rounded-sm transition-colors mt-auto">
              {t(language, 'srv_card8_b')}
            </button>
          </div>

        </div>
      </div>
    </div>
  )
}
