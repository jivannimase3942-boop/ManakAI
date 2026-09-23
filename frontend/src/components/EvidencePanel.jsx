import React from 'react';

export default function EvidencePanel({ sources }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mb-8">
      <h4 className="text-[13px] font-bold uppercase tracking-wider text-[#0B1E40] mb-3 border-b border-slate-200 pb-2 flex items-center gap-2">
        <span className="w-1 h-3 bg-[#1C4E80] inline-block"></span>
        Official Evidence
      </h4>
      <div className="space-y-3">
        {sources.map((s, idx) => (
          <div key={idx} className="bg-white border border-slate-200 rounded-sm p-4 flex flex-col items-start shadow-sm hover:border-[#1C4E80] transition-colors">
            <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider mb-1 flex items-center gap-2">
              <span className="w-1.5 h-1.5 bg-[#1C4E80] rounded-full inline-block"></span>Official BIS Source
            </p>
            <p className="text-[14px] font-medium text-slate-800 mb-1">
              {s.title}
              {s.standard_number && <span className="ml-1 text-slate-500 font-normal">({s.standard_number})</span>}
            </p>
            {s.source_url && (
              <a
                href={s.source_url}
                target="_blank"
                rel="noreferrer"
                className="text-[13px] text-[#1C4E80] hover:underline underline-offset-2 flex items-center mt-1 font-semibold"
              >
                View official BIS source
                <svg className="w-3.5 h-3.5 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                </svg>
              </a>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
