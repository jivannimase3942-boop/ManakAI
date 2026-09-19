import React, { useState } from 'react';

import { useTranslation } from '../i18n';



export default function WhyThisAnswer({ message, language = 'en' }) {

  const [isOpen, setIsOpen] = useState(false);

  const { t } = useTranslation();



  return (

    <div className="border border-slate-200 rounded-sm mb-8 bg-white shadow-sm mt-4">

      <button

        onClick={() => setIsOpen(!isOpen)}

        className="w-full flex items-center justify-between px-5 py-3 text-left focus:outline-none bg-slate-50 hover:bg-slate-100 transition-colors"

      >

        <span className="text-[13px] font-bold uppercase tracking-wider text-[#0B1E40] flex items-center gap-2">

          <svg className="w-4 h-4 text-[#1C4E80]" fill="none" viewBox="0 0 24 24" stroke="currentColor">

            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />

          </svg>

          {t(language, 'why_this_standard')}

        </span>

        <span className="text-[#1C4E80] font-bold text-lg leading-none">{isOpen ? '−' : '+'}</span>

      </button>



      {isOpen && (

        <div className="px-5 pb-5 border-t border-slate-200 pt-4 space-y-4">

          <div className="space-y-3">

            <div>

              <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider">{t(language, 'product_identified')}</p>

              <p className="text-[14px] text-slate-800 font-medium">{message.product || t(language, 'not_verified')}</p>

            </div>

            <div>

              <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider">{t(language, 'applicable_standard')}</p>

              <p className="text-[14px] text-slate-800 font-medium">{message.applicable_standard || t(language, 'not_verified')}</p>

            </div>

            <div>

              <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider">{t(language, 'reason')}</p>

              <p className="text-[14px] text-slate-800 font-medium">{message.why_applicable || (message.compliance_journey && message.compliance_journey.summary) || t(language, 'not_verified')}</p>

            </div>

            <div>

              <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider">{t(language, 'evidence')}</p>

              <p className="text-[14px] text-slate-800 font-medium">BIS CRS Products List / Official BIS Portal</p>

            </div>

            <div>

              <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider">{t(language, 'source_status')}</p>

              <p className="text-[14px] text-green-700 font-bold flex items-center gap-1">

                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">

                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />

                </svg>

                Verified

              </p>

            </div>



            {message.official_sources && message.official_sources.length > 0 && (

              <div className="pt-2">

                <a

                  href={message.official_sources[0].url}

                  target="_blank"

                  rel="noopener noreferrer"

                  className="inline-flex items-center gap-2 bg-[#1C4E80] text-white px-4 py-2 rounded-sm text-xs font-bold uppercase tracking-wider hover:bg-[#0B1E40] transition-colors"

                >

                  {t(language, 'open_official_source')}

                  <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">

                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />

                  </svg>

                </a>

              </div>

            )}

          </div>

        </div>

      )}

    </div>

  );

}
