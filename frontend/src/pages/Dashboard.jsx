import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLocalData } from '../hooks/useLocalData.js';
import { t } from '../i18n.js';
import { api } from '../api.js';
import ComplianceImpactGraph from '../components/ComplianceImpactGraph.jsx';

export default function Dashboard({ language }) {
  const navigate = useNavigate();
  const { history, savedStandards, removeStandard, clearHistory, quizScore } = useLocalData();
  const [checkingImpact, setCheckingImpact] = useState({});
  const [impactData, setImpactData] = useState({});

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 min-h-[calc(100vh-64px)]">
      <div className="mb-8 border-b border-slate-200 pb-5 flex flex-col md:flex-row md:items-end justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">{t(language, 'dash_title')}</h1>
          <p className="text-slate-500 mt-2">{t(language, 'dash_desc')}</p>
        </div>
        <div className="mt-4 md:mt-0 text-[12px] bg-blue-50 text-blue-800 font-medium px-3 py-1.5 rounded-sm border border-blue-100 flex items-center">
          <svg className="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {t(language, 'dash_guest')}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

        {/* Left Column: Quick Links & Progress */}
        <div className="lg:col-span-1 space-y-8">

          {/* Quick Links */}
          <div className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden">
            <h2 className="text-lg font-bold text-slate-800 px-5 py-4 border-b border-slate-100 bg-slate-50">{t(language, 'lbl_quick_links')}</h2>
            <div className="divide-y divide-slate-100">
              <button onClick={() => navigate('/assistant')} className="w-full text-left px-5 py-3 hover:bg-slate-50 flex items-center justify-between text-slate-700 transition-colors">
                <span className="font-medium">{t(language, 'nav_assistant')}</span>
                <span className="text-slate-400">→</span>
              </button>
              <button onClick={() => navigate('/industry')} className="w-full text-left px-5 py-3 hover:bg-slate-50 flex items-center justify-between text-slate-700 transition-colors">
                <span className="font-medium">{t(language, 'srv_card6_t')}</span>
                <span className="text-slate-400">→</span>
              </button>
              <button onClick={() => navigate('/finder')} className="w-full text-left px-5 py-3 hover:bg-slate-50 flex items-center justify-between text-slate-700 transition-colors">
                <span className="font-medium">{t(language, 'nav_finder')}</span>
                <span className="text-slate-400">→</span>
              </button>
              <button onClick={() => navigate('/learning')} className="w-full text-left px-5 py-3 hover:bg-slate-50 flex items-center justify-between text-slate-700 transition-colors">
                <span className="font-medium">{t(language, 'nav_learning')}</span>
                <span className="text-slate-400">→</span>
              </button>
            </div>
          </div>

          {/* Learning Progress */}
          <div className="bg-white border border-slate-200 rounded-lg shadow-sm p-5">
            <h2 className="text-lg font-bold text-slate-800 mb-3">{t(language, 'lbl_learning_progress')}</h2>
            {quizScore !== null ? (
              <div className="text-center bg-green-50 border border-green-100 rounded-lg py-6">
                <div className="text-3xl font-bold text-green-700 mb-1">{quizScore} / 5</div>
                <div className="text-green-800 text-sm font-medium">{t(language, 'lbl_last_quiz_score')}</div>
                <button onClick={() => navigate('/learning')} className="mt-4 text-xs bg-white border border-green-200 text-green-700 px-3 py-1.5 rounded hover:bg-green-100 transition-colors">
                  {t(language, 'lbl_retake_quiz')}
                </button>
              </div>
            ) : (
              <div className="text-center bg-slate-50 border border-slate-100 rounded-lg py-6 px-4">
                <p className="text-slate-500 text-sm mb-3">{t(language, 'lbl_no_quiz_taken')}</p>
                <button onClick={() => navigate('/learning')} className="text-sm bg-navy-600 hover:bg-navy-700 text-white px-4 py-2 rounded-md font-medium transition-colors">
                  {t(language, 'lbl_take_quiz')}
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Standards & History */}
        <div className="lg:col-span-2 space-y-8">

          {/* Saved Standards */}
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-slate-800">{t(language, 'lbl_saved_standards')}</h2>
              <span className="bg-slate-100 text-slate-600 text-xs font-bold px-2 py-0.5 rounded-full">{savedStandards.length}</span>
            </div>

            {savedStandards.length === 0 ? (
              <div className="bg-white border border-slate-200 p-10 text-center rounded-lg shadow-sm flex flex-col items-center justify-center">
                <svg className="w-10 h-10 text-slate-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
                </svg>
                <h3 className="text-slate-700 font-medium mb-1">{t(language, 'lbl_no_saved_standards')}</h3>
                <p className="text-sm text-slate-500 max-w-sm">{t(language, 'lbl_bookmark_hint')}</p>
                <button onClick={() => navigate('/finder')} className="mt-4 text-sm text-navy-600 font-medium hover:underline">{t(language, 'lbl_go_to_finder')}</button>
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {savedStandards.map(s => (
                  <div
                    key={s.standard_number}
                    className="bg-white border border-slate-200 p-5 rounded-lg shadow-sm flex flex-col items-start relative group hover:border-navy-400 hover:shadow-md transition-all cursor-pointer"
                    onClick={() => navigate('/finder', { state: { prefill: s.title || s.standard_number } })}
                  >
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        removeStandard(s.standard_number);
                      }}
                      className="absolute top-4 right-4 text-slate-300 hover:text-red-500 transition-colors"
                      title="Remove Bookmark"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                      </svg>
                    </button>
                    <span className="text-[11px] font-bold uppercase tracking-wider text-navy-700 bg-navy-50 px-2 py-0.5 rounded-sm mb-2 border border-navy-100">
                      {s.standard_number}
                    </span>
                    <h3 className="font-bold text-slate-800 text-sm pr-8 mb-1 line-clamp-2">{s.title}</h3>
                    <p className="text-xs text-slate-500 mb-3">{s.scheme || t(language, 'lbl_applicable_scheme')}</p>

                    <button
                      onClick={async (e) => {
                        e.stopPropagation();
                        setCheckingImpact(prev => ({...prev, [s.standard_number]: true}));
                        try {
                          const res = await api.post('/api/compliance/impact', {
                            standard: s.standard_number,
                            product: s.title
                          });
                          setImpactData(prev => ({...prev, [s.standard_number]: res.data}));
                        } catch (err) {
                          console.error(err);
                        } finally {
                          setCheckingImpact(prev => ({...prev, [s.standard_number]: false}));
                        }
                      }}
                      disabled={checkingImpact[s.standard_number]}
                      className="mt-auto w-full text-center text-xs font-bold uppercase tracking-wider bg-slate-50 hover:bg-slate-100 text-navy-600 border border-slate-200 py-2 rounded-sm transition-colors"
                    >
                      {checkingImpact[s.standard_number] ? 'Checking...' : 'Check for BIS Changes'}
                    </button>

                    {impactData[s.standard_number] && (
                      <div className="w-full mt-3" onClick={e => e.stopPropagation()}>
                        <ComplianceImpactGraph data={impactData[s.standard_number]} language={language} />
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* History */}
          <div>
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-xl font-bold text-slate-800">{t(language, 'lbl_recent_queries')}</h2>
              {history.length > 0 && (
                <button
                  onClick={clearHistory}
                  className="text-xs text-slate-500 hover:text-red-600 underline transition-colors"
                >
                  {t(language, 'lbl_clear_history')}
                </button>
              )}
            </div>

            {history.length === 0 ? (
              <div className="bg-white border border-slate-200 p-10 text-center rounded-lg shadow-sm flex flex-col items-center justify-center">
                <svg className="w-10 h-10 text-slate-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 16l2.879-2.879m0 0a3 3 0 104.243-4.242 3 3 0 00-4.243 4.242zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <h3 className="text-slate-700 font-medium mb-1">{t(language, 'lbl_no_recent_queries')}</h3>
                <p className="text-sm text-slate-500">{t(language, 'lbl_recent_search_hint')}</p>
                <button onClick={() => navigate('/assistant')} className="mt-4 text-sm text-navy-600 font-medium hover:underline">{t(language, 'lbl_ask_assistant')}</button>
              </div>
            ) : (
              <div className="bg-white border border-slate-200 rounded-lg shadow-sm overflow-hidden divide-y divide-slate-100">
                {history.map((h, i) => (
                  <div key={i} className="p-4 hover:bg-slate-50 transition-colors flex justify-between items-center group cursor-pointer" onClick={() => navigate('/assistant', { state: { prefill: h.query } })}>
                    <div className="pr-4">
                      <p className="text-slate-800 text-sm font-medium">{h.query}</p>
                      <p className="text-slate-400 text-[11px] mt-1">
                        {new Date(h.timestamp).toLocaleString()}
                      </p>
                    </div>
                    <div className="text-navy-600 opacity-0 group-hover:opacity-100 transition-opacity">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                      </svg>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
