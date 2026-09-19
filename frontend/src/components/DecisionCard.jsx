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

  const stdNum = message.applicable_standard || message.standard_number || message.scheme;

  // Phase 14: Intent-based priority
  const intent = message.intent || 'UNKNOWN';

  // Phase 12: Journey Structure Data
  const jProduct = message.product || message.topic || 'Unknown';
  const jStandard = (stdNum && stdNum !== 'N/A') ? stdNum : null;
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
      icon = '—';
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
          <span>{value || t(language, state === 'not_verified' ? 'j_not_verified' : 'j_unavailable')}</span>
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
            {t(language, 'journey_title')}
          </h3>
          {message.confidence && message.confidence !== 'none' && (
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 bg-slate-100 px-2.5 py-1 rounded-sm border border-slate-200">
              {t(language, 'lbl_confidence')}: {message.confidence}
            </span>
          )}
        </div>

        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <JourneyNode
              num="01"
              label={t(language, 'j_product')}
              value={jProduct}
              state="verified"
              isHighlight={false}
            />
            <JourneyNode
              num="02"
              label={t(language, 'j_standard')}
              value={jStandard}
              state={jStandard ? 'verified' : 'not_verified'}
              isHighlight={intent === 'STANDARD_DISCOVERY'}
            />
            <JourneyNode
              num="03"
              label={t(language, 'j_pathway')}
              value={jPathway}
              state={jPathway ? 'verified' : 'not_verified'}
              isHighlight={intent === 'CERTIFICATION' || intent === 'LICENSING'}
            />
            <JourneyNode
              num="04"
              label={t(language, 'j_testing')}
              value={jTesting}
              state={jTesting ? 'guidance' : 'not_verified'}
              isHighlight={intent === 'TESTING'}
            />
            <JourneyNode
              num="05"
              label={t(language, 'j_documents')}
              value={jDocs}
              state={jDocs ? 'guidance' : 'not_verified'}
              isHighlight={intent === 'DOCUMENTS'}
            />
            <JourneyNode
              num="06"
              label={t(language, 'j_next_action')}
              value={jNext}
              state={jNext ? 'guidance' : 'unavailable'}
              isHighlight={intent === 'GENERAL_BIS_GUIDANCE' || intent === 'REQUIREMENTS'}
            />
          </div>
        </div>
      </div>

      {/* WHY THIS STANDARD / EVIDENCE CHAIN */}
      {jStandard && (
        <div className="w-full bg-slate-50 border border-slate-200 rounded-sm shadow-sm overflow-hidden mb-6">
          <div className="px-6 py-4 border-b border-slate-200">
            <h4 className="text-[13px] font-bold uppercase tracking-wider text-[#0B1E40]">{t(language, 'why_standard')}</h4>
          </div>
          <div className="p-6 text-sm text-slate-700 space-y-3">
            <div className="flex flex-col sm:flex-row gap-2">
              <span className="font-bold w-40 shrink-0">{t(language, 'w_product')}</span>
              <span>{jProduct}</span>
            </div>
            <div className="flex flex-col sm:flex-row gap-2">
              <span className="font-bold w-40 shrink-0">{t(language, 'w_standard')}</span>
              <span>{jStandard}</span>
            </div>
            <div className="flex flex-col sm:flex-row gap-2">
              <span className="font-bold w-40 shrink-0">{t(language, 'w_reason')}</span>
              <span>{message.why_this_answer || t(language, 'w_default_reason')}</span>
            </div>
            {message.sources && message.sources.length > 0 && (
              <div className="flex flex-col sm:flex-row gap-2">
                <span className="font-bold w-40 shrink-0">{t(language, 'w_evidence')}</span>
                <span>{message.sources[0].source_name} ({message.sources[0].verified ? 'Verified' : 'Unverified'})</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* REALITY CHECK */}
      <div className="w-full bg-white border border-amber-200 rounded-sm shadow-sm overflow-hidden">
        <div className="bg-amber-50 px-6 py-3 border-b border-amber-200">
          <h4 className="text-[13px] font-bold uppercase tracking-wider text-amber-900 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-amber-500"></span>
            {t(language, 'rc_title')}
          </h4>
        </div>
        <div className="p-6 grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <h5 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">{t(language, 'rc_can_guide')}</h5>
            <ul className="space-y-2 text-sm text-slate-700">
              <li>{t(language, 'rc_can_1')}</li>
              <li>{t(language, 'rc_can_2')}</li>
              <li>{t(language, 'rc_can_3')}</li>
            </ul>
          </div>
          <div>
            <h5 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">{t(language, 'rc_cannot_verify')}</h5>
            <ul className="space-y-2 text-sm text-slate-700">
              <li>{t(language, 'rc_cannot_1')}</li>
              <li>{t(language, 'rc_cannot_2')}</li>
              <li>{t(language, 'rc_cannot_3')}</li>
              <li>{t(language, 'rc_cannot_4')}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
