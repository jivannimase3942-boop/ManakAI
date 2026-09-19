import React from 'react';

import { t } from '../i18n.js';



export default function ComplianceJourney({ message, language = 'en' }) {





  const standard = message.applicable_standard || message.scheme;



  if (!standard && !message.product) return null;



  const journeySteps = [

    {

      title: t(language, 'product'),

      content: message.product ? <p className="text-[13px] text-slate-600 font-medium">{message.product}</p> : <p className="text-[13px] text-slate-400 italic">{t(language, 'not_verified')}</p>

    },

    {

      title: t(language, 'standard'),

      content: standard ? <p className="text-[13px] text-slate-600 font-medium">{standard}</p> : <p className="text-[13px] text-slate-400 italic">{t(language, 'not_verified')}</p>

    },

    {

      title: t(language, 'bis_pathway'),

      content: (message.compliance_journey && message.compliance_journey.scheme) ?

        <p className="text-[13px] text-slate-600 font-medium">{message.compliance_journey.scheme}</p> :

        <p className="text-[13px] text-slate-400 italic">{t(language, 'not_verified')}</p>

    },

    {

      title: t(language, 'testing'),

      content: (message.compliance_journey && message.compliance_journey.testing && message.compliance_journey.testing.required) ? (

        <ul className="space-y-1">

          <li className="text-[13px] text-slate-600 flex items-start">

            <span className="mr-2 text-slate-400 mt-0.5">•</span>

            <span>{message.compliance_journey.testing.laboratory_type}</span>

          </li>

          <li className="text-[13px] text-slate-600 flex items-start">

            <span className="mr-2 text-slate-400 mt-0.5">•</span>

            <span>{message.compliance_journey.testing.guidance}</span>

          </li>

        </ul>

      ) : <p className="text-[13px] text-slate-400 italic">{t(language, 'not_verified')}</p>

    },

    {

      title: t(language, 'documents'),

      content: (message.compliance_journey && message.compliance_journey.documents && message.compliance_journey.documents.length > 0) ? (

        <ul className="space-y-1">

          {message.compliance_journey.documents.map((doc, i) => (

            <li key={i} className="text-[13px] text-slate-600 flex items-start">

              <span className="mr-2 text-slate-400 mt-0.5">•</span>

              <span>{doc}</span>

            </li>

          ))}

        </ul>

      ) : <p className="text-[13px] text-slate-400 italic">{t(language, 'not_verified')}</p>

    },

    {

      title: t(language, 'next_action'),

      content: (message.compliance_journey && message.compliance_journey.steps && message.compliance_journey.steps.length > 0) ? (

        <ul className="space-y-1">

          {message.compliance_journey.steps.map((step, i) => (

            <li key={i} className="text-[13px] text-slate-600 flex items-start">

              <span className="mr-2 text-slate-400 mt-0.5">•</span>

              <span>{step}</span>

            </li>

          ))}

        </ul>

      ) : <p className="text-[13px] text-slate-400 italic">{t(language, 'not_verified')}</p>

    }

  ];



  return (

    <div className="mb-6 mt-4">

      <div className="space-y-0 relative before:absolute before:inset-0 before:ml-3 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-slate-200">

        {journeySteps.map((step, index) => (

          <div key={index} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group pb-6">

            <div className="flex items-center justify-center w-6 h-6 rounded-full border border-white bg-[#1C4E80] text-white shadow-sm shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">

              <span className="text-[10px] font-bold">0{index + 1}</span>

            </div>

            <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] p-4 rounded-sm border border-slate-200 bg-white shadow-sm ml-4 md:ml-0 md:mr-0">

              <h5 className="font-bold text-[#1C4E80] text-[12px] uppercase tracking-wide mb-2">

                {step.title}

              </h5>

              {step.content}

            </div>

          </div>

        ))}

      </div>

    </div>

  );

}
