import React, { useState } from 'react';

export default function ComplaintCopilot({ message }) {
  const [showDraft, setShowDraft] = useState(false);

  // We only use the verified URL if the message specifically matched a complaint source
  // Otherwise we explicitly document that no URL is verified for this exact product context.
  const isOfficialSource = message.sources && message.sources.some(s => s.source_url && s.source_url.includes('bis.gov.in'));
  const officialUrl = isOfficialSource ? message.sources.find(s => s.source_url)?.source_url : null;

  return (
    <div className="mb-8 border border-slate-200 rounded-sm bg-white overflow-hidden shadow-sm">
      <div className="bg-slate-50 px-4 py-3 border-b border-slate-200 flex justify-between items-center cursor-pointer hover:bg-slate-100 transition-colors"
           onClick={() => setShowDraft(!showDraft)}>
        <h4 className="font-semibold text-slate-800 text-[14px]">Complaint Drafting Copilot</h4>
        <button className="text-slate-500 hover:text-slate-700 font-medium text-[12px] uppercase tracking-wider">
          {showDraft ? 'Hide Draft' : 'Start Draft'}
        </button>
      </div>

      {showDraft && (
        <div className="p-4 space-y-4 animate-fade-in text-[13px] text-slate-700">
          <p className="bg-blue-50 border border-blue-100 text-blue-800 p-3 rounded-sm leading-relaxed">
            Use this checklist to prepare the necessary information before registering your complaint.
            <strong className="block mt-1">Note: This prototype does not submit complaints to BIS.</strong>
          </p>

          <div>
            <h5 className="font-semibold mb-2 uppercase tracking-wider text-[11px] text-slate-500">Preparation Checklist</h5>
            <ul className="space-y-2">
              <li className="flex items-start">
                <input type="checkbox" className="mt-1 mr-2" />
                <span><strong>Product Details:</strong> Name, brand, and exact model/batch number.</span>
              </li>
              <li className="flex items-start">
                <input type="checkbox" className="mt-1 mr-2" />
                <span><strong>Identifiers:</strong> The ISI mark CM/L (licence) number, or gold/silver HUID.</span>
              </li>
              <li className="flex items-start">
                <input type="checkbox" className="mt-1 mr-2" />
                <span><strong>Purchase Proof:</strong> Keep a clear photo or copy of your invoice/bill.</span>
              </li>
              <li className="flex items-start">
                <input type="checkbox" className="mt-1 mr-2" />
                <span><strong>Evidence:</strong> Clear photos showing the defect or substandard quality.</span>
              </li>
              <li className="flex items-start">
                <input type="checkbox" className="mt-1 mr-2" />
                <span><strong>Issue Description:</strong> A factual description of why the product is substandard.</span>
              </li>
            </ul>
          </div>

          <div className="mt-4 pt-4 border-t border-slate-100">
            {officialUrl ? (
              <div className="bg-slate-50 p-3 rounded-sm border border-slate-200">
                <p className="mb-2 font-medium">Proceed to Official Service:</p>
                <a href={officialUrl} target="_blank" rel="noopener noreferrer" className="inline-block bg-slate-800 text-white px-4 py-2 rounded-sm text-[12px] font-bold uppercase tracking-wider hover:bg-slate-700 transition-colors">
                  Open Official BIS Source
                </a>
              </div>
            ) : (
              <div className="bg-yellow-50 p-3 rounded-sm border border-yellow-200">
                <p className="text-yellow-800">
                  <span className="font-bold">Limitation:</span> An official complaint URL could not be verified for this exact product context in the current prototype. Please visit the main BIS website (bis.gov.in) or use the BIS Care App to proceed.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
