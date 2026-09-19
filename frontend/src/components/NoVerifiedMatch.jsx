import React from 'react';
import { t } from '../i18n.js';

export default function NoVerifiedMatch({ message, language = 'en' }) {
  return (
    <div className="flex flex-col animate-fade-in mb-8 w-full font-sans">
      <div className="w-full bg-white border border-slate-200 rounded-sm shadow-sm overflow-hidden">
        {/* Header */}
        <div className="bg-white text-slate-800 border-b border-slate-200 px-6 py-4 flex justify-between items-center">
          <h3 className="font-bold text-[15px] uppercase tracking-wider text-[#0B1E40]">
            {t(language, 'lbl_no_match')}
          </h3>
        </div>

        <div className="p-6 space-y-6">
          <p className="text-slate-800 text-[15px] font-medium border-l-4 border-red-500 pl-3">
            {t(language, 'no_verified_match')}
          </p>

          {/* Next Actions */}
          <div className="bg-slate-50 border border-slate-200 rounded-sm p-5">
            <p className="text-xs text-slate-600 font-bold uppercase tracking-wider mb-3">{t(language, 'dec_next_action')}</p>
            {message.next_actions && message.next_actions.length > 0 ? (
              <ul className="space-y-2 text-[14px] text-slate-700 list-disc list-inside ml-1">
                {message.next_actions.map((action, idx) => (
                  <li key={idx}>
                    {action}
                  </li>
                ))}
              </ul>
            ) : (
              <ul className="space-y-2 text-[14px] text-slate-700 list-disc list-inside ml-1">
                <li>Try a more specific product name</li>
                <li>Provide a standard number if known</li>
                <li>Search official BIS standards</li>
                <li>Visit relevant BIS service</li>
              </ul>
            )}
          </div>
        </div>

        {/* Disclaimer */}
        <div className="bg-slate-50 border-t border-slate-200 px-6 py-4">
          <p className="text-[11px] text-slate-500 font-medium text-center">
            {t(language, 'dec_disclaimer')}
          </p>
        </div>
      </div>
    </div>
  );
}
