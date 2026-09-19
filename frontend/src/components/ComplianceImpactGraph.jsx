import React from 'react';
import { t } from '../i18n.js';

export default function ComplianceImpactGraph({ data, language }) {
  if (!data) return null;

  const {
    standard,
    product,
    change_status,
    summary,
    impact_areas = [],
    affected_users = [],
    recommended_actions = [],
    evidence = []
  } = data;

  const statusColors = {
    VERIFIED_CHANGE: 'bg-red-50 text-red-700 border-red-200',
    NO_VERIFIED_CHANGE: 'bg-green-50 text-green-700 border-green-200',
    UNAVAILABLE: 'bg-slate-50 text-slate-700 border-slate-200',
  };

  const statusIcons = {
    VERIFIED_CHANGE: (
      <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    ),
    NO_VERIFIED_CHANGE: (
      <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
    UNAVAILABLE: (
      <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  };

  const hasImpactData = change_status === 'VERIFIED_CHANGE' && (impact_areas.length > 0 || recommended_actions.length > 0);

  return (
    <div className="bg-white border border-slate-200 rounded-lg overflow-hidden shadow-sm mt-4">
      <div className={`px-5 py-4 border-b flex items-center justify-between ${statusColors[change_status]}`}>
        <div className="flex items-center space-x-3">
          {statusIcons[change_status]}
          <div>
            <h3 className="font-bold text-sm tracking-wide">{product} ({standard})</h3>
            <p className="text-xs opacity-90 mt-0.5">{t(language, `status_${change_status}`) || change_status}</p>
          </div>
        </div>
      </div>

      <div className="p-5">
        <p className="text-sm text-slate-700 mb-6">{summary}</p>

        {hasImpactData ? (
          <div className="relative">
            {/* Graph flow line */}
            <div className="absolute left-6 top-6 bottom-6 w-0.5 bg-slate-100"></div>

            <div className="space-y-6 relative z-10">
              {/* Node 1: Impact Areas */}
              <div className="flex">
                <div className="w-12 flex-shrink-0 flex justify-center">
                  <div className="w-8 h-8 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center border border-white shadow-sm ring-4 ring-white">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" /></svg>
                  </div>
                </div>
                <div className="ml-4 flex-1">
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Impact & Affected Areas</h4>
                  <ul className="space-y-1">
                    {impact_areas.map((ia, i) => <li key={i} className="text-sm text-slate-800 flex items-start"><span className="text-slate-300 mr-2">•</span>{ia}</li>)}
                    {affected_users.map((au, i) => <li key={`au-${i}`} className="text-sm text-slate-800 flex items-start"><span className="text-slate-300 mr-2">•</span>{au}</li>)}
                  </ul>
                </div>
              </div>

              {/* Node 2: Action */}
              <div className="flex">
                <div className="w-12 flex-shrink-0 flex justify-center">
                  <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-600 flex items-center justify-center border border-white shadow-sm ring-4 ring-white">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" /></svg>
                  </div>
                </div>
                <div className="ml-4 flex-1">
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Required Actions</h4>
                  <ul className="space-y-1">
                    {recommended_actions.map((ra, i) => <li key={i} className="text-sm text-slate-800 flex items-start"><span className="text-slate-300 mr-2">•</span>{ra}</li>)}
                  </ul>
                </div>
              </div>

              {/* Node 3: Evidence */}
              <div className="flex">
                <div className="w-12 flex-shrink-0 flex justify-center">
                  <div className="w-8 h-8 rounded-full bg-slate-100 text-slate-600 flex items-center justify-center border border-white shadow-sm ring-4 ring-white">
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" /></svg>
                  </div>
                </div>
                <div className="ml-4 flex-1">
                  <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Official Evidence</h4>
                  {evidence.length > 0 ? (
                    <div className="space-y-2">
                      {evidence.map((ev, i) => (
                        <a key={i} href={ev.source_url} target="_blank" rel="noopener noreferrer" className="block p-3 rounded-md border border-slate-100 bg-slate-50 hover:bg-slate-100 hover:border-slate-200 transition-colors">
                          <div className="flex items-center">
                            {ev.verified && (
                              <svg className="w-4 h-4 text-green-500 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                              </svg>
                            )}
                            <span className="text-sm text-navy-700 font-medium">{ev.source_name}</span>
                          </div>
                          <p className="text-xs text-slate-500 mt-1 truncate">{ev.source_url}</p>
                        </a>
                      ))}
                    </div>
                  ) : (
                    <div className="p-3 rounded-md border border-red-100 bg-red-50 text-red-600 text-sm italic">
                      Evidence unavailable
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-6">
            {change_status === 'UNAVAILABLE' ? (
              <p className="text-sm text-slate-500">Check official BIS sources for the latest updates.</p>
            ) : (
              <p className="text-sm text-slate-500">The verified knowledge base indicates no active changes.</p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
