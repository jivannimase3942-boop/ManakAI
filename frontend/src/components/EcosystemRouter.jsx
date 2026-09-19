import React from 'react';
import { t } from '../i18n.js';

export default function EcosystemRouter({ message, language = 'en' }) {
  const intent = message.intent || 'UNKNOWN';

  // Deterministic routing based on intent
  let highlightedService = null;
  let serviceLink = null;

  if (intent === 'COMPLAINT') {
    highlightedService = 'eco_consumer';
  } else if (intent === 'CONSUMER_VERIFICATION') {
    highlightedService = 'eco_consumer';
  } else if (intent === 'HALLMARKING') {
    highlightedService = 'eco_huid';
  } else if (intent === 'TESTING') {
    highlightedService = 'eco_lims';
  } else if (intent === 'CERTIFICATION' || intent === 'LICENSING') {
    highlightedService = 'eco_cert';
  } else if (intent === 'SCHEME' && message.scheme === 'CRS') {
    highlightedService = 'eco_crs';
  } else if (intent === 'STANDARD_DISCOVERY') {
    highlightedService = 'eco_kys';
  }

  // Find official verified URL from sources
  if (message.sources && message.sources.length > 0) {
    const verifiedSource = message.sources.find(s => s.verified && s.source_url && (s.source_url.includes('bis.gov.in') || s.source_url.includes('crsbis.in')));
    if (verifiedSource) {
      serviceLink = verifiedSource.source_url;
    }
  }

  return (
    <div className="w-full bg-slate-900 border border-slate-700 rounded-sm shadow-lg overflow-hidden my-8">
      <div className="bg-slate-800 px-6 py-4 border-b border-slate-700 flex justify-between items-center">
        <h4 className="text-[13px] font-bold uppercase tracking-wider text-slate-100 flex items-center gap-2">
          <svg className="w-4 h-4 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {t(language, 'eco_title')}
        </h4>
      </div>
      <div className="p-6">
        <p className="text-slate-300 text-sm font-medium mb-6 leading-relaxed">
          {t(language, 'eco_desc')}
        </p>

        {/* Tree visualization */}
        <div className="flex flex-col md:flex-row items-center gap-4 text-sm font-bold text-slate-200">
          <div className="bg-slate-800 border border-slate-600 px-6 py-3 rounded-md shadow-inner text-center min-w-[150px]">
            {t(language, 'eco_manakai')}
          </div>

          <div className="hidden md:block w-8 border-b-2 border-slate-600 border-dashed"></div>
          <div className="block md:hidden h-8 border-l-2 border-slate-600 border-dashed"></div>

          <div className="flex flex-col gap-2 w-full md:w-auto">
            {['eco_kys', 'eco_cert', 'eco_crs', 'eco_lims', 'eco_consumer', 'eco_huid'].map((svcKey) => (
              <div
                key={svcKey}
                className={`px-4 py-2 rounded-sm border transition-all ${
                  highlightedService === svcKey
                    ? 'bg-cyan-900 border-cyan-400 text-cyan-50 shadow-[0_0_15px_rgba(34,211,238,0.3)]'
                    : 'bg-slate-800 border-slate-700 text-slate-400'
                }`}
              >
                {t(language, svcKey)}
              </div>
            ))}
          </div>

          {highlightedService && (
            <>
              <div className="hidden md:block w-8 border-b-2 border-cyan-500 border-dashed"></div>
              <div className="block md:hidden h-8 border-l-2 border-cyan-500 border-dashed"></div>

              <div className="flex flex-col items-center gap-3">
                <div className="bg-cyan-950 border-2 border-cyan-400 px-6 py-4 rounded-md shadow-lg text-center min-w-[150px]">
                  <span className="text-cyan-300 text-xs uppercase tracking-wider block mb-1">Target</span>
                  <span className="text-cyan-50">{t(language, 'eco_official')}</span>
                </div>
                {serviceLink ? (
                  <a
                    href={serviceLink}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs bg-cyan-600 hover:bg-cyan-500 text-white font-bold py-2 px-4 rounded-sm transition-colors uppercase tracking-wider"
                  >
                    Open Official Portal
                  </a>
                ) : (
                  <span className="text-xs text-slate-400 italic">
                    {t(language, 'w_not_verified')}
                  </span>
                )}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
