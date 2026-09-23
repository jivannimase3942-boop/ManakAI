import { useEffect, useState } from 'react'
import { t } from '../i18n.js'
import { api } from '../api.js'

export default function About({ language }) {
  const [sources, setSources] = useState([])

  useEffect(() => {
    api.sources().then(setSources).catch(() => {})
  }, [])

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-3xl font-extrabold text-slate-900 mb-2">{t(language, 'abt_title')}</h1>
      <p className="text-slate-600 text-[15px] mb-8">{t(language, 'abt_subtitle')}</p>

      <div className="space-y-10 text-[15px] text-slate-700 leading-relaxed">

        <section>
          <h2 className="text-lg font-bold text-slate-900 mb-3 border-b border-slate-200 pb-2 uppercase tracking-wider text-[13px]">{t(language, 'abt_h1')}</h2>
          <p>
            {t(language, 'abt_p1')}
          </p>
        </section>

        <section>
          <h2 className="text-lg font-bold text-slate-900 mb-4 border-b border-slate-200 pb-2 uppercase tracking-wider text-[13px]">{t(language, 'abt_h2')}</h2>
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-6 font-mono text-sm text-center">
            <div className="font-bold text-slate-800">{t(language, 'lbl_question')}</div>
            <div className="text-slate-400 my-2">↓</div>
            <div className="font-bold text-slate-800">{t(language, 'nav_learning') === 'Learning Centre' ? 'Intent' : (language === 'hi' ? 'इरादा' : 'उद्देश्य')}</div>
            <div className="text-slate-400 my-2">↓</div>
            <div className="font-bold text-slate-800">{t(language, 'nav_learning') === 'Learning Centre' ? 'Verified Knowledge' : (language === 'hi' ? 'सत्यापित ज्ञान' : 'सत्यापित ज्ञान')}</div>
            <div className="text-slate-400 my-2">↓</div>
            <div className="font-bold text-slate-800">{t(language, 'nav_learning') === 'Learning Centre' ? 'Standard / Scheme' : (language === 'hi' ? 'मानक / योजना' : 'मानक / योजना')}</div>
            <div className="text-slate-400 my-2">↓</div>
            <div className="font-bold text-slate-800">{t(language, 'nav_learning') === 'Learning Centre' ? 'Guidance' : (language === 'hi' ? 'मार्गदर्शन' : 'मार्गदर्शन')}</div>
            <div className="text-slate-400 my-2">↓</div>
            <div className="font-bold text-slate-800">{t(language, 'lbl_evidence')}</div>
            <div className="text-slate-400 my-2">↓</div>
            <div className="font-bold text-slate-800">{t(language, 'nav_learning') === 'Learning Centre' ? 'Next Action' : (language === 'hi' ? 'अगली कार्रवाई' : 'पुढील कृती')}</div>
          </div>
        </section>

        <section>
          <h2 className="text-lg font-bold text-slate-900 mb-3 border-b border-slate-200 pb-2 uppercase tracking-wider text-[13px]">{t(language, 'abt_h3')}</h2>
          <p className="mb-3">
            {t(language, 'abt_p3')}
          </p>
          <ul className="list-disc pl-6 space-y-2 mt-4">
            <li>{t(language, 'abt_li3_1')}</li>
            <li>{t(language, 'abt_li3_2')}</li>
            <li>{t(language, 'abt_li3_3')}</li>
          </ul>
        </section>

        <section>
          <h2 className="text-lg font-bold text-slate-900 mb-3 border-b border-slate-200 pb-2 uppercase tracking-wider text-[13px]">{t(language, 'abt_h1')} NOT Do</h2>
          <ul className="list-disc pl-6 space-y-2">
            <li>{t(language, 'abt_li4_1')}</li>
            <li>{t(language, 'abt_li4_2')}</li>
            <li>{t(language, 'abt_li4_3')}</li>
            <li>{t(language, 'abt_li4_4')}</li>
          </ul>
        </section>

        <section className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-slate-900 mb-2 uppercase tracking-wider text-[13px]">{t(language, 'abt_h5')}</h2>
          <p className="mb-4 text-[14px] text-slate-600">
            {t(language, 'abt_p5')}
          </p>
          <a href="https://www.bis.gov.in/" target="_blank" rel="noreferrer" className="inline-block bg-navy-600 hover:bg-navy-700 text-white font-medium text-[13px] px-5 py-2.5 rounded-md transition-colors">
            {t(language, 'abt_btn5')}
          </a>
        </section>
      </div>
    </div>
  )
}
