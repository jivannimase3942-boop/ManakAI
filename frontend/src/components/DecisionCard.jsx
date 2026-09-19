import React from 'react';

import { t } from '../i18n.js';

import { useLocalData } from '../hooks/useLocalData.js';



export default function DecisionCard({ message, language = 'en' }) {

  const { isSaved, saveStandard, removeStandard } = useLocalData();



  const hasStandard = message.applicable_standard && message.applicable_standard !== 'N/A';

  const saved = hasStandard ? isSaved(message.applicable_standard) : false;



  const handleSaveToggle = () => {

    if (!hasStandard) return;

    if (saved) {

      removeStandard(message.applicable_standard);

    } else {

      saveStandard({

        title: message.product || message.topic || message.product_category,

        standard_number: message.applicable_standard,

        scheme: message.scheme

      });

    }

  };



  const intent = message.intent;



  const jProduct = message.product || message.topic || null;

  const jStandard = message.applicable_standard || null;

  const jPathway = message.scheme || (message.certification_steps?.length > 0 ? message.certification_steps.join(' → ') : null);

  const jTesting = message.testing?.length > 0 ? message.testing[0] : null;

  const jDocs = message.required_documents?.length > 0 ? message.required_documents.join(', ') : null;

  const jNext = message.next_actions?.length > 0 ? message.next_actions[0] : null;



  const JourneyNode = ({ num, label, value, state, isHighlight }) => {

    let icon = '';

    let textColor = '';

    let bgColor = '';

    if (state === 'verified') {

      icon = '✓';

      textColor = 'text-green-700';

      bgColor = 'bg-green-50 border-green-200';

    } else if (state === 'guidance') {

      icon = '→';

      textColor = 'text-blue-700';

      bgColor = 'bg-blue-50 border-blue-200';

    } else {

      icon = '?';

      textColor = 'text-gray-500';

      bgColor = 'bg-gray-50 border-gray-200';

    }



    return (

      <div className={`p-4 rounded-sm border ${bgColor} ${isHighlight ? 'ring-2 ring-navy-600 shadow-md' : 'shadow-sm'} transition-all`}>

        <div className="flex items-center gap-2 mb-2">

          <span className="text-xs font-bold text-gray-400">{num}</span>

          <h4 className="text-[11px] font-bold uppercase tracking-wider text-gray-700">{label}</h4>

        </div>

        <div className={`flex items-start gap-2 font-semibold text-[14px] ${textColor}`}>

          <span className="mt-0.5">{icon}</span>

          <span>{value || t(language, 'not_verified')}</span>

        </div>

      </div>

    );

  };



  return (

    <div className="flex flex-col animate-fade-in mb-8 w-full font-sans">



      {/* Primary Answer Section */}

      {message.answer && (

        <div className="bg-white border border-slate-200 rounded-sm shadow-sm overflow-hidden mb-6">

          <div className="bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center">

             <h3 className="font-bold text-[15px] uppercase tracking-wider text-[#0B1E40]">

               {language === 'hi' ? 'उत्तर' : language === 'mr' ? 'उत्तर' : 'Answer'}

             </h3>

          </div>

          <div className="p-6 text-slate-800">

             <p className="text-[16px] text-slate-900 font-medium leading-relaxed whitespace-pre-wrap">

               {message.answer}

             </p>

          </div>

        </div>

      )}



      {/* BIS JOURNEY COMPOSER */}

      <div className="w-full bg-white border border-slate-200 rounded-sm shadow-sm overflow-hidden mb-6">

        <div className="bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center">

          <h3 className="font-bold text-[15px] uppercase tracking-wider text-[#0B1E40]">

            {t(language, 'bis_pathway')}

          </h3>

          {message.confidence && message.confidence !== 'none' && (

            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 bg-slate-100 px-2.5 py-1 rounded-sm border border-slate-200">

              {t(language, 'lbl_confidence') || 'Confidence'}: {message.confidence}

            </span>

          )}

        </div>



        <div className="p-6">

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

            <JourneyNode

              num="01"

              label={t(language, 'product')}

              value={jProduct}

              state="verified"

              isHighlight={false}

            />

            <JourneyNode

              num="02"

              label={t(language, 'standard')}

              value={jStandard}

              state={jStandard ? 'verified' : 'not_verified'}

              isHighlight={intent === 'STANDARD_DISCOVERY'}

            />

            <JourneyNode

              num="03"

              label={t(language, 'bis_pathway')}

              value={jPathway}

              state={jPathway ? 'verified' : 'not_verified'}

              isHighlight={intent === 'CERTIFICATION' || intent === 'LICENSING'}

            />

            <JourneyNode

              num="04"

              label={t(language, 'testing')}

              value={jTesting}

              state={jTesting ? 'guidance' : 'not_verified'}

              isHighlight={intent === 'TESTING'}

            />

            <JourneyNode

              num="05"

              label={t(language, 'documents')}

              value={jDocs}

              state={jDocs ? 'guidance' : 'not_verified'}

              isHighlight={intent === 'DOCUMENTS'}

            />

            <JourneyNode

              num="06"

              label={t(language, 'next_action')}

              value={jNext}

              state={jNext ? 'guidance' : 'unavailable'}

              isHighlight={intent === 'GENERAL_BIS_GUIDANCE' || intent === 'REQUIREMENTS'}

            />

          </div>

        </div>

      </div>



      {/* COMPLIANCE STATUS GAP (No Score) */}

      <div className="w-full bg-white border border-slate-200 rounded-sm shadow-sm overflow-hidden mb-6">

        <div className="px-6 py-4 border-b border-slate-200">

          <h4 className="text-[13px] font-bold uppercase tracking-wider text-[#0B1E40]">{t(language, 'compliance_status')}</h4>

        </div>

        <div className="p-6 text-sm text-slate-700 space-y-2">

          <div className="flex items-center gap-2">

             {jProduct ? <span className="text-green-600 font-bold">✓</span> : <span className="text-red-600 font-bold">⚠</span>}

             <span>{t(language, 'product_identified')}</span>

          </div>

          <div className="flex items-center gap-2">

             {jStandard ? <span className="text-green-600 font-bold">✓</span> : <span className="text-red-600 font-bold">⚠</span>}

             <span>{t(language, 'applicable_standard')}</span>

          </div>

          <div className="flex items-center gap-2">

             {jPathway ? <span className="text-green-600 font-bold">✓</span> : <span className="text-amber-600 font-bold">⚠</span>}

             <span>{t(language, 'bis_pathway')}</span>

          </div>

          <div className="flex items-center gap-2">

             {jTesting ? <span className="text-green-600 font-bold">✓</span> : <span className="text-amber-600 font-bold">⚠</span>}

             <span>{t(language, 'testing')}</span>

          </div>

          <div className="flex items-center gap-2">

             {jDocs ? <span className="text-green-600 font-bold">✓</span> : <span className="text-amber-600 font-bold">⚠</span>}

             <span>{t(language, 'documents')} {t(language, 'requires_confirmation') ? `- ${t(language, 'requires_confirmation')}` : ''}</span>

          </div>

        </div>

      </div>



      {/* WHY THIS STANDARD / EVIDENCE CHAIN */}

      {jStandard && (

        <div className="w-full bg-slate-50 border border-slate-200 rounded-sm shadow-sm overflow-hidden mb-6">

          <div className="px-6 py-4 border-b border-slate-200">

            <h4 className="text-[13px] font-bold uppercase tracking-wider text-[#0B1E40]">{t(language, 'why_this_standard')}</h4>

          </div>

          <div className="p-6 text-sm text-slate-700 space-y-3">

            <div className="flex flex-col sm:flex-row gap-2">

              <span className="font-bold w-40 shrink-0">{t(language, 'product_identified')}:</span>

              <span>{jProduct}</span>

            </div>

            <div className="flex flex-col sm:flex-row gap-2">

              <span className="font-bold w-40 shrink-0">{t(language, 'applicable_standard')}:</span>

              <span>{jStandard}</span>

            </div>

            <div className="flex flex-col sm:flex-row gap-2">

              <span className="font-bold w-40 shrink-0">{t(language, 'reason')}:</span>

              <span>{message.why_applicable || message.why_this_answer || t(language, 'not_verified')}</span>

            </div>

            <div className="flex flex-col sm:flex-row gap-2">

              <span className="font-bold w-40 shrink-0">{t(language, 'evidence')}:</span>

              <span>{message.sources && message.sources.length > 0 ? message.sources[0].source_name : 'BIS CRS Products List / Official BIS Portal'}</span>

            </div>

            <div className="flex flex-col sm:flex-row gap-2 items-center">

              <span className="font-bold w-40 shrink-0">{t(language, 'source_status')}:</span>

              <span className="text-green-700 font-bold">Verified</span>

            </div>

            {message.sources && message.sources.length > 0 && message.sources[0].source_url && (

              <div className="pt-2">

                <a

                  href={message.sources[0].source_url}

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



      {/* TRUST & EVIDENCE */}

      <div className="w-full bg-white border border-slate-300 rounded-sm shadow-sm overflow-hidden">

        <div className="bg-slate-100 px-6 py-3 border-b border-slate-300">

          <h4 className="text-[13px] font-bold uppercase tracking-wider text-slate-800 flex items-center gap-2">

            <span className="w-2 h-2 rounded-full bg-slate-500"></span>

            {t(language, 'trust_and_evidence')}

          </h4>

        </div>

        <div className="p-6">

          <p className="text-[14px] text-slate-600 italic mb-6">

            "Evidence-backed guidance based on verified BIS information. Official decisions and live verification remain with BIS."

          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">

            <div>

              <h5 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3">VERIFIED GUIDANCE</h5>

              <ul className="space-y-2 text-sm text-slate-700">

                <li className="flex items-start gap-2"><span className="text-green-600 font-bold">✓</span> Applicable standard</li>

                <li className="flex items-start gap-2"><span className="text-green-600 font-bold">✓</span> BIS / certification pathway</li>

                <li className="flex items-start gap-2"><span className="text-green-600 font-bold">✓</span> Supporting evidence</li>

              </ul>

            </div>

            <div>

              <h5 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3">OFFICIAL VERIFICATION</h5>

              <ul className="space-y-2 text-sm text-slate-700">

                <li className="flex items-start gap-2"><span className="text-blue-600 font-bold">→</span> Live licence status</li>

                <li className="flex items-start gap-2"><span className="text-blue-600 font-bold">→</span> Product authenticity</li>

                <li className="flex items-start gap-2"><span className="text-blue-600 font-bold">→</span> Live HUID status</li>

                <li className="flex items-start gap-2"><span className="text-blue-600 font-bold">→</span> Specific laboratory capability unless independently verified</li>

              </ul>

            </div>

          </div>

        </div>

      </div>



    </div>

  );

}
