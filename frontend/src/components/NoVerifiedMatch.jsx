import React from 'react';

import { t } from '../i18n.js';



export default function NoVerifiedMatch({ message, language = 'en' }) {





  return (

    <div className="flex flex-col animate-fade-in mb-8 w-full font-sans mt-4">

      <div className="w-full bg-white border border-slate-200 rounded-sm shadow-sm overflow-hidden">

        {/* Header */}

        <div className="bg-slate-50 text-slate-800 border-b border-slate-200 px-6 py-4 flex justify-between items-center">

          <h3 className="font-bold text-[15px] uppercase tracking-wider text-[#0B1E40]">

            {t(language, 'no_verified_match')}

          </h3>

        </div>



        <div className="p-6 space-y-6">

          <p className="text-slate-800 text-[15px] font-medium">

            {t(language, 'no_verified_match_desc')}

          </p>



          <p className="text-slate-600 text-[14px]">

            {t(language, 'no_verified_match_sub')}

          </p>

        </div>



        {/* Disclaimer */}

        <div className="bg-slate-50 border-t border-slate-200 px-6 py-4">

          <p className="text-[11px] text-slate-500 font-medium text-center italic">

            "Evidence-backed guidance based on verified BIS information. Official decisions and live verification remain with BIS."

          </p>

        </div>

      </div>

    </div>

  );

}
