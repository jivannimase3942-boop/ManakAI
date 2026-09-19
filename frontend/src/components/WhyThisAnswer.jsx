import React, { useState } from 'react';

export default function WhyThisAnswer({ message }) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="border border-slate-200 rounded-sm mb-8 bg-white shadow-sm">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="w-full flex items-center justify-between px-5 py-3 text-left focus:outline-none"
      >
        <span className="text-[13px] font-bold uppercase tracking-wider text-[#0B1E40]">Why this answer?</span>
        <span className="text-[#1C4E80] font-bold text-lg leading-none">{isOpen ? '−' : '+'}</span>
      </button>

      {isOpen && (
        <div className="px-5 pb-5 border-t border-slate-200 pt-4 space-y-4">
          <div className="space-y-3">
            <div>
              <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider flex items-center gap-2"><span className="w-1.5 h-1.5 bg-[#1C4E80] rounded-full inline-block"></span>Detected Intent</p>
              <p className="text-[14px] text-slate-800 font-medium">{message.intent}</p>
            </div>
            <div>
              <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider flex items-center gap-2"><span className="w-1.5 h-1.5 bg-[#1C4E80] rounded-full inline-block"></span>Matched Entity</p>
              <p className="text-[14px] text-slate-800 font-medium">{message.product}</p>
            </div>
            <div>
              <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider flex items-center gap-2"><span className="w-1.5 h-1.5 bg-[#1C4E80] rounded-full inline-block"></span>Verified Record</p>
              <p className="text-[14px] text-slate-800 font-medium">{message.applicable_standard || message.scheme || 'N/A'}</p>
            </div>
            {message.why_applicable && (
              <div>
                <p className="text-[11px] text-[#1C4E80] font-bold uppercase tracking-wider flex items-center gap-2"><span className="w-1.5 h-1.5 bg-[#1C4E80] rounded-full inline-block"></span>Explanation</p>
                <p className="text-[14px] text-slate-800 font-medium">{message.why_applicable}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
