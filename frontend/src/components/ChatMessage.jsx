import SourceCard from './SourceCard.jsx'
import { t } from '../i18n.js'

export default function ChatMessage({ message, language }) {
  const isUser = message.role === 'user'

  if (isUser) {
    return (
      <div className="flex justify-end animate-fade-in mb-6">
        <div className="max-w-[85%] sm:max-w-[70%] bg-navy-700 text-white rounded-2xl px-5 py-3 text-[16px] leading-relaxed shadow-sm">
          {message.content}
        </div>
      </div>
    )
  }

  // If there's an error or generic message
  if (!message.intent) {
    return (
      <div className="flex justify-start animate-fade-in mb-6">
        <div className="max-w-full bg-white border border-red-200 rounded-xl px-5 py-4 shadow-card w-full text-red-700">
          <p>{message.content || 'An error occurred.'}</p>
        </div>
      </div>
    )
  }

  const intent = message.intent;
  const isUnknown = !message.match_found;
  
  // Visibility logic based on intent
  const showFullWorkflow = ['REQUIREMENTS', 'GENERAL_INFORMATION'].includes(intent);
  
  const showRequirements = showFullWorkflow || ['STANDARD_IDENTIFICATION'].includes(intent);
  const showDocuments = showFullWorkflow || ['DOCUMENTS', 'LICENSING', 'CERTIFICATION'].includes(intent);
  const showTesting = showFullWorkflow || ['TESTING', 'CERTIFICATION'].includes(intent);
  const showCertification = showFullWorkflow || ['CERTIFICATION', 'LICENSING', 'SCHEME_IDENTIFICATION', 'HALLMARKING'].includes(intent);

  return (
    <div className="flex flex-col animate-fade-in mb-8 w-full">
      <div className="w-full bg-white border border-navy-200 rounded-xl shadow-lg overflow-hidden">
        
        {/* Header */}
        <div className="bg-navy-900 text-white px-6 py-4 flex justify-between items-center">
          <h3 className="font-bold text-lg tracking-wide">
            {isUnknown ? t(language, 'lbl_no_match') : t(language, 'lbl_decision')}
          </h3>
          <span className="text-[10px] font-bold uppercase tracking-wider bg-navy-700 px-3 py-1 rounded-full">
            {t(language, 'lbl_confidence')}: {message.confidence} | {message.mode === 'llm' ? t(language, 'lbl_llm_explanation') : t(language, 'lbl_verified_knowledge')}
          </span>
        </div>

        <div className="p-6 space-y-6">
          {/* Product & Standard */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 border-b border-gray-100 pb-6">
            <div>
              <p className="text-xs text-navy-400 font-bold uppercase tracking-wider mb-1">{t(language, 'lbl_product')}</p>
              <p className="text-navy-900 font-semibold text-lg">{message.product}</p>
            </div>
            <div>
              <p className="text-xs text-navy-400 font-bold uppercase tracking-wider mb-1">{t(language, 'lbl_standard')}</p>
              <p className="text-navy-900 font-semibold text-lg">{message.applicable_standard}</p>
            </div>
          </div>

          {/* Why this applies */}
          {!isUnknown && message.why_applicable && (
            <div className="border-b border-gray-100 pb-6">
              <p className="text-xs text-navy-400 font-bold uppercase tracking-wider mb-2">{t(language, 'lbl_why')}</p>
              <p className="text-navy-800 text-[15px]">{message.why_applicable}</p>
            </div>
          )}

          {isUnknown && message.why_applicable && (
            <div className="border-b border-gray-100 pb-6">
              <p className="text-navy-800 text-[15px]">{message.why_applicable}</p>
            </div>
          )}

          {/* Compliance Status */}
          {message.compliance_status && message.compliance_status.length > 0 && (
            <div className="border-b border-gray-100 pb-6">
              <p className="text-xs text-navy-400 font-bold uppercase tracking-wider mb-3">{t(language, 'lbl_status')}</p>
              <ul className="space-y-1.5 bg-slate-50 border border-slate-200 rounded-lg p-4">
                {message.compliance_status.map((status, idx) => {
                  let colorClass = "text-navy-700"
                  if (status.startsWith('✓')) colorClass = "text-green-700 font-medium"
                  else if (status.startsWith('⚠')) colorClass = "text-orange-600 font-medium"
                  else if (status.startsWith('ⓘ')) colorClass = "text-blue-600 font-medium"

                  return (
                    <li key={idx} className={`text-[14px] flex items-start ${colorClass}`}>
                       {status}
                    </li>
                  )
                })}
              </ul>
            </div>
          )}

          {/* Requirements */}
          {!isUnknown && showRequirements && (
            <div className="border-b border-gray-100 pb-6">
              <p className="text-xs text-navy-400 font-bold uppercase tracking-wider mb-3">{t(language, 'lbl_reqs')}</p>
              {message.requirements && message.requirements.length > 0 ? (
                <ul className="space-y-2">
                  {message.requirements.map((req, idx) => (
                    <li key={idx} className="flex items-start text-[14px] text-navy-800">
                      <span className="text-green-600 mr-2 font-bold">✓</span>
                      {req}
                    </li>
                  ))}
                </ul>
              ) : (
                 <p className="text-[13px] text-navy-500 font-medium">None explicitly specified for this query.</p>
              )}
            </div>
          )}

          {/* Documents */}
          {!isUnknown && showDocuments && (
            <div className="border-b border-gray-100 pb-6">
              <p className="text-xs text-navy-400 font-bold uppercase tracking-wider mb-3">{t(language, 'lbl_docs')}</p>
              {message.required_documents && message.required_documents.length > 0 ? (
                <ul className="space-y-2">
                  {message.required_documents.map((doc, idx) => (
                    <li key={idx} className="flex items-start text-[14px] text-navy-800">
                      <span className="text-green-600 mr-2 font-bold">✓</span>
                      {doc}
                    </li>
                  ))}
                </ul>
              ) : (
                 <p className="flex items-center text-[13px] text-orange-600 font-medium">
                   <span className="mr-1.5">⚠</span> Exact verified checklist unavailable. Next action: Check current BIS application requirements for this product.
                 </p>
              )}
            </div>
          )}

          {/* Testing */}
          {!isUnknown && showTesting && (
            <div className="border-b border-gray-100 pb-6">
              <p className="text-xs text-navy-400 font-bold uppercase tracking-wider mb-3">{t(language, 'lbl_testing')}</p>
              {message.testing && message.testing.length > 0 ? (
                <ul className="space-y-2">
                  {message.testing.map((tItem, idx) => (
                    <li key={idx} className="flex items-start text-[14px] text-navy-800">
                      <span className="text-blue-600 mr-2 font-bold">•</span>
                      {tItem}
                    </li>
                  ))}
                </ul>
              ) : (
                 <p className="flex items-center text-[13px] text-navy-500 font-medium">
                   Not specifically mandated in the current verified KB for this query.
                 </p>
              )}
            </div>
          )}

          {/* Certification */}
          {!isUnknown && showCertification && (
            <div className="border-b border-gray-100 pb-6">
              <p className="text-xs text-navy-400 font-bold uppercase tracking-wider mb-3">{t(language, 'lbl_cert')}</p>
              <p className="text-[14px] text-navy-800 mb-2"><strong>Scheme:</strong> {message.scheme}</p>
              {message.certification_steps && message.certification_steps.length > 0 && (
                <ol className="list-decimal list-inside space-y-1 text-[14px] text-navy-800 ml-1">
                  {message.certification_steps.map((step, idx) => (
                    <li key={idx}>{step}</li>
                  ))}
                </ol>
              )}
            </div>
          )}

          {/* What Is Missing */}
          {message.missing_information && message.missing_information.length > 0 && (
            <div className="border-b border-gray-100 pb-6">
              <p className="text-xs text-red-600 font-bold uppercase tracking-wider mb-3">{t(language, 'lbl_missing')}</p>
              <ul className="space-y-2 bg-red-50 border border-red-100 rounded-lg p-4">
                {message.missing_information.map((item, idx) => (
                  <li key={idx} className="flex items-start text-[13px] text-red-800 font-medium">
                    <span className="mr-2">⚠</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Next Actions */}
          <div className="bg-blue-50 border border-blue-100 rounded-lg p-5">
            <p className="text-xs text-blue-800 font-bold uppercase tracking-wider mb-3">{t(language, 'lbl_next')}</p>
            {message.next_actions && message.next_actions.length > 0 ? (
              <ol className="space-y-2 text-[14px] text-blue-900 font-medium">
                {message.next_actions.map((action, idx) => (
                  <li key={idx} className="flex items-start">
                    <span className="bg-blue-200 text-blue-800 rounded-full w-5 h-5 flex items-center justify-center text-xs mr-2 flex-shrink-0 mt-0.5">
                      {idx + 1}
                    </span>
                    {action}
                  </li>
                ))}
              </ol>
            ) : (
              <p className="text-sm text-blue-800">No clear next actions identified.</p>
            )}
          </div>

          {/* Evidence */}
          {!isUnknown && (
            <div>
              <p className="text-xs text-navy-400 font-bold uppercase tracking-wider mb-3">{t(language, 'lbl_evidence')}</p>
              {message.sources && message.sources.length > 0 && (
                <SourceCard sources={message.sources} language={language} />
              )}
            </div>
          )}

        </div>

        {/* Disclaimer */}
        <div className="bg-gray-50 border-t border-gray-200 px-6 py-3">
          <p className="text-[11px] text-gray-500 font-medium text-center">{message.disclaimer}</p>
        </div>
      </div>
    </div>
  )
}
