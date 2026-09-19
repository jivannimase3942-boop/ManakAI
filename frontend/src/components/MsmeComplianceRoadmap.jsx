import React from 'react';
import { t } from '../i18n.js';

export default function MsmeComplianceRoadmap({ data, language }) {
  if (!data) return null;

  const {
    product,
    applicable_standard,
    scheme,
    requirements = [],
    certification_steps = [],
    testing = [],
    required_documents = [],
    next_actions = [],
    sources = []
  } = data;

  const evidenceList = sources.filter(s => s.verified);

  return (
    <div className="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-sm mt-4 text-left w-full max-w-3xl">
      <div className="bg-navy-700 text-white px-5 py-4 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <svg className="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <div>
            <h3 className="font-bold text-base tracking-wide">MSME Compliance Roadmap</h3>
            <p className="text-xs text-navy-200 mt-0.5">{product} ({applicable_standard})</p>
          </div>
        </div>
      </div>

      <div className="p-5 space-y-6">

        {/* Step 1: Standard & Scheme */}
        <div className="flex">
          <div className="w-8 flex-shrink-0 flex justify-center">
            <div className="w-6 h-6 rounded-full bg-blue-100 text-blue-700 font-bold text-xs flex items-center justify-center">1</div>
          </div>
          <div className="ml-3 flex-1">
            <h4 className="text-sm font-bold text-slate-800">Standard & Certification Pathway</h4>
            <div className="mt-2 bg-slate-50 border border-slate-100 rounded-md p-3">
              <p className="text-sm text-slate-700"><span className="font-semibold">Standard:</span> {applicable_standard}</p>
              <p className="text-sm text-slate-700 mt-1"><span className="font-semibold">Scheme:</span> {scheme}</p>
            </div>
          </div>
        </div>

        {/* Step 2: Testing */}
        <div className="flex">
          <div className="w-8 flex-shrink-0 flex justify-center">
            <div className="w-6 h-6 rounded-full bg-purple-100 text-purple-700 font-bold text-xs flex items-center justify-center">2</div>
          </div>
          <div className="ml-3 flex-1">
            <h4 className="text-sm font-bold text-slate-800">Testing Requirements</h4>
            <ul className="mt-2 space-y-1">
              {testing.length > 0 ? testing.map((tItem, i) => (
                <li key={i} className="text-sm text-slate-600 flex items-start"><span className="text-purple-400 mr-2">•</span>{tItem}</li>
              )) : <li className="text-sm text-slate-400 italic">No specific testing guidance available in verified KB.</li>}
            </ul>
          </div>
        </div>

        {/* Step 3: Documents */}
        <div className="flex">
          <div className="w-8 flex-shrink-0 flex justify-center">
            <div className="w-6 h-6 rounded-full bg-green-100 text-green-700 font-bold text-xs flex items-center justify-center">3</div>
          </div>
          <div className="ml-3 flex-1">
            <h4 className="text-sm font-bold text-slate-800">Required Documents</h4>
            <ul className="mt-2 space-y-1">
              {required_documents.length > 0 ? required_documents.map((dItem, i) => (
                <li key={i} className="text-sm text-slate-600 flex items-start"><span className="text-green-400 mr-2">•</span>{dItem}</li>
              )) : <li className="text-sm text-slate-400 italic">Checklist unavailable in verified KB.</li>}
            </ul>
          </div>
        </div>

        {/* Step 4: Review Checklist (Requirements) */}
        <div className="flex">
          <div className="w-8 flex-shrink-0 flex justify-center">
            <div className="w-6 h-6 rounded-full bg-orange-100 text-orange-700 font-bold text-xs flex items-center justify-center">4</div>
          </div>
          <div className="ml-3 flex-1">
            <h4 className="text-sm font-bold text-slate-800">Product Review Checklist</h4>
            <ul className="mt-2 space-y-1">
              {requirements.length > 0 ? requirements.map((rItem, i) => (
                <li key={i} className="text-sm text-slate-600 flex items-start"><span className="text-orange-400 mr-2">•</span>{rItem}</li>
              )) : <li className="text-sm text-slate-400 italic">Requirements unavailable in verified KB.</li>}
            </ul>
          </div>
        </div>

        {/* Step 5: Next Action */}
        <div className="flex">
          <div className="w-8 flex-shrink-0 flex justify-center">
            <div className="w-6 h-6 rounded-full bg-red-100 text-red-700 font-bold text-xs flex items-center justify-center">5</div>
          </div>
          <div className="ml-3 flex-1">
            <h4 className="text-sm font-bold text-slate-800">Next Actions</h4>
            <ul className="mt-2 space-y-1">
              {next_actions.length > 0 ? next_actions.map((nA, i) => (
                <li key={i} className="text-sm text-slate-600 flex items-start"><span className="text-red-400 mr-2">•</span>{nA}</li>
              )) : <li className="text-sm text-slate-400 italic">Consult official BIS portal for next steps.</li>}
            </ul>
          </div>
        </div>

      </div>

      {/* Footer: Official Source */}
      <div className="bg-slate-50 px-5 py-4 border-t border-slate-200">
        <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Verified Official Sources</h4>
        {evidenceList.length > 0 ? (
          <div className="space-y-2">
            {evidenceList.map((ev, i) => (
              <a key={i} href={ev.source_url} target="_blank" rel="noopener noreferrer" className="block p-3 rounded-md border border-slate-200 bg-white hover:bg-slate-50 transition-colors">
                <div className="flex items-center">
                  <svg className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                  <span className="text-sm text-navy-700 font-medium">{ev.source_name}</span>
                </div>
                <p className="text-xs text-slate-500 mt-1 truncate">{ev.source_url}</p>
              </a>
            ))}
          </div>
        ) : (
          <div className="p-3 rounded-md border border-red-100 bg-red-50 text-red-600 text-sm italic">
            Evidence unavailable. Do not proceed without official BIS verification.
          </div>
        )}
      </div>
    </div>
  );
}
