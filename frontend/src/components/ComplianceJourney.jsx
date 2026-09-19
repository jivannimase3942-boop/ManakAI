import React from 'react';

export default function ComplianceJourney({ message }) {
  const isStructured = message.structured_compliance_journey && message.structured_compliance_journey.length > 0;

  // Fallback to legacy fields if not structured
  const hasRequirements = message.requirements && message.requirements.length > 0;
  const hasDocuments = message.required_documents && message.required_documents.length > 0;
  const hasTesting = message.testing && message.testing.length > 0;
  const hasCertification = message.certification_steps && message.certification_steps.length > 0;
  const standard = message.applicable_standard || message.scheme;

  const showJourney = isStructured || standard || hasRequirements || hasDocuments || hasTesting || hasCertification;

  if (!showJourney) return null;

  // Mock runtime profile resolution as requested in Phase 2F
  const getUserProfileStatus = (reqId) => {
    // In the future this checks the actual user profile Context.
    return 'UNKNOWN'; // Always UNKNOWN for now since we don't have user auth yet.
  };

  return (
    <div className="mb-6">
      <h4 className="text-[13px] font-semibold uppercase tracking-wider text-slate-700 mb-4 border-b border-slate-200 pb-2">
        Compliance Journey
      </h4>

      <div className="space-y-0 relative before:absolute before:inset-0 before:ml-3 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-slate-200">

        {isStructured ? (
          message.structured_compliance_journey.map((stepData, index) => (
            <div key={index} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group pb-6">
              <div className="flex items-center justify-center w-6 h-6 rounded-full border border-white bg-navy-600 text-white shadow-sm shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                <span className="text-[10px] font-bold">{stepData.step || index + 1}</span>
              </div>
              <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] p-4 rounded-sm border border-slate-200 bg-white shadow-sm ml-4 md:ml-0 md:mr-0">
                <h5 className="font-bold text-slate-800 text-[12px] uppercase tracking-wide mb-1">
                  Step {stepData.step || index + 1}: {stepData.title}
                </h5>
                {stepData.description && <p className="text-[13px] text-slate-600 mb-3">{stepData.description}</p>}

                {stepData.requirements && stepData.requirements.length > 0 && (
                  <div className="space-y-3 mt-3">
                    {stepData.requirements.map((req, i) => {
                      const currentStatus = getUserProfileStatus(req.id);

                      return (
                        <div key={i} className="border border-slate-100 rounded bg-slate-50 p-3">
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-semibold text-[13px] text-slate-800">{req.name}</span>
                            {currentStatus === 'MISSING' ? (
                              <span className="text-[11px] font-bold text-red-600 uppercase">Missing ❌</span>
                            ) : currentStatus === 'READY' ? (
                              <span className="text-[11px] font-bold text-green-600 uppercase">Ready ✓</span>
                            ) : (
                              <span className="text-[11px] font-bold text-amber-600 uppercase">Status Not Provided</span>
                            )}
                          </div>

                          <p className="text-[12px] text-slate-500 mb-2">
                            {currentStatus === 'UNKNOWN' ? 'Required — status not provided' :
                             currentStatus === 'MISSING' && req.if_missing?.message ? req.if_missing.message : ''}
                          </p>

                          {req.missing_action && req.verified_url && (
                             <a
                               href={req.verified_url}
                               target="_blank"
                               rel="noopener noreferrer"
                               className="inline-flex items-center text-[12px] font-semibold text-blue-600 hover:text-blue-800"
                             >
                               {req.missing_action} →
                             </a>
                          )}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          ))
        ) : (
          /* LEGACY RENDERING BELOW */
          <>
            {/* IDENTIFY */}
            {standard && (
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group pb-6">
                <div className="flex items-center justify-center w-6 h-6 rounded-full border border-white bg-slate-200 text-slate-600 shadow-sm shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <span className="text-[10px] font-bold">1</span>
                </div>
                <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] p-4 rounded-sm border border-slate-200 bg-white shadow-sm ml-4 md:ml-0 md:mr-0">
                  <h5 className="font-bold text-slate-800 text-[12px] uppercase tracking-wide mb-1">Identify</h5>
                  <p className="text-[13px] text-slate-600">{standard}</p>
                </div>
              </div>
            )}

            {/* REQUIREMENTS */}
            {hasRequirements && (
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group pb-6">
                <div className="flex items-center justify-center w-6 h-6 rounded-full border border-white bg-slate-200 text-slate-600 shadow-sm shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <span className="text-[10px] font-bold">2</span>
                </div>
                <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] p-4 rounded-sm border border-slate-200 bg-white shadow-sm ml-4 md:ml-0 md:mr-0">
                  <h5 className="font-bold text-slate-800 text-[12px] uppercase tracking-wide mb-2">Requirements</h5>
                  <ul className="space-y-1.5">
                    {message.requirements.map((req, i) => (
                      <li key={i} className="text-[13px] text-slate-600 flex items-start">
                        <span className="mr-2 text-slate-400 mt-0.5">•</span>
                        <span>{req}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* REQUIRED DOCUMENTS */}
            {hasDocuments && (
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group pb-6">
                <div className="flex items-center justify-center w-6 h-6 rounded-full border border-white bg-slate-200 text-slate-600 shadow-sm shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <span className="text-[10px] font-bold">3</span>
                </div>
                <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] p-4 rounded-sm border border-slate-200 bg-white shadow-sm ml-4 md:ml-0 md:mr-0">
                  <h5 className="font-bold text-slate-800 text-[12px] uppercase tracking-wide mb-2">Required Documents</h5>
                  <ul className="space-y-1.5">
                    {message.required_documents.map((doc, i) => (
                      <li key={i} className="text-[13px] text-slate-600 flex items-start">
                        <span className="mr-2 text-slate-400 mt-0.5">•</span>
                        <span>{doc}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* TESTING */}
            {hasTesting && (
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group pb-6">
                <div className="flex items-center justify-center w-6 h-6 rounded-full border border-white bg-slate-200 text-slate-600 shadow-sm shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <span className="text-[10px] font-bold">4</span>
                </div>
                <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] p-4 rounded-sm border border-slate-200 bg-white shadow-sm ml-4 md:ml-0 md:mr-0">
                  <h5 className="font-bold text-slate-800 text-[12px] uppercase tracking-wide mb-2">Testing</h5>
                  <ul className="space-y-1.5">
                    {message.testing.map((tItem, i) => (
                      <li key={i} className="text-[13px] text-slate-600 flex items-start">
                        <span className="mr-2 text-slate-400 mt-0.5">•</span>
                        <span>{tItem}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}

            {/* CERTIFICATION */}
            {hasCertification && (
              <div className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group pb-6">
                <div className="flex items-center justify-center w-6 h-6 rounded-full border border-white bg-slate-200 text-slate-600 shadow-sm shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 z-10">
                  <span className="text-[10px] font-bold">5</span>
                </div>
                <div className="w-[calc(100%-2.5rem)] md:w-[calc(50%-1.5rem)] p-4 rounded-sm border border-slate-200 bg-white shadow-sm ml-4 md:ml-0 md:mr-0">
                  <h5 className="font-bold text-slate-800 text-[12px] uppercase tracking-wide mb-2">Certification</h5>
                  <ul className="space-y-1.5">
                    {message.certification_steps.map((step, i) => (
                      <li key={i} className="text-[13px] text-slate-600 flex items-start">
                        <span className="mr-2 text-slate-400 font-medium">{i+1}.</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
