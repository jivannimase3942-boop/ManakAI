import React from 'react';
import { t } from '../i18n.js';
import { useLocalData } from '../hooks/useLocalData.js';

export default function DecisionCard({ message, language = 'en' }) {
  const { isSaved, saveStandard, removeStandard } = useLocalData();
  const hasStandard = message.applicable_standard && message.applicable_standard !== 'N/A';
  const saved = hasStandard ? isSaved(message.applicable_standard) : false;

  const handleSaveToggle = () => {
    if (!hasStandard) return;
    if (saved) {
      removeStandard(message.applicable_standard);
    } else {
      saveStandard({
        title: message.product || message.topic || message.product_category,
        standard_number: message.applicable_standard,
        scheme: message.scheme
      });
    }
  };

  const isMatched = message.match_found;

  if (!isMatched) {
    return (
      <div className="flex flex-col animate-fade-in mb-8 w-full font-sans">
        <div className="bg-white border border-slate-200 rounded-sm shadow-sm overflow-hidden mb-6">
          <div className="bg-slate-50 border-b border-slate-200 px-6 py-4 flex justify-between items-center">
             <h3 className="font-bold text-[15px] uppercase tracking-wider text-slate-800">
               {language === 'hi' ? 'कोई सत्यापित मिलान नहीं' : language === 'mr' ? 'कोणताही सत्यापित जुळणारा आढळला नाही' : 'No Verified Match'}
             </h3>
          </div>
          <div className="p-6 text-slate-800">
             <p className="text-[15px] text-slate-700 font-medium leading-relaxed whitespace-pre-wrap mb-4">
               {language === 'hi' 
                 ? "मैं उपलब्ध सत्यापित जानकारी से किसी प्रासंगिक BIS मानक की पुष्टि नहीं कर सका।"
                 : language === 'mr' 
                 ? "उपलब्ध सत्यापित माहितीवरून मी कोणत्याही संबंधित BIS मानकाची पडताळणी करू शकलो नाही."
                 : "I couldn't verify a relevant BIS standard from the available verified information."}
             </p>
             <p className="text-[14px] text-slate-600">
               {language === 'hi'
                 ? "कृपया कोई अन्य स्पष्ट चित्र आज़माएं, उत्पाद का वर्णन करें, या आधिकारिक BIS सेवाओं का अन्वेषण करें।"
                 : language === 'mr'
                 ? "कृपया दुसरे स्पष्ट चित्र वापरून पहा, उत्पादनाचे वर्णन करा किंवा अधिकृत BIS सेवा एक्सप्लोर करा."
                 : "Try another clear image, refine the product description, or explore official BIS services."}
             </p>
          </div>
        </div>
      </div>
    );
  }

  const sProduct = message.product || message.topic || "Unknown";
  const sStandard = message.applicable_standard || "N/A";
  const sScheme = message.scheme && message.scheme !== 'N/A' ? message.scheme : (message.certification_steps?.length > 0 ? message.certification_steps.join(' → ') : null);
  
  const sTesting = message.structured_testing;
  const testingText = sTesting?.guidance || (message.testing?.length > 0 ? message.testing.join(' ') : null);
  const testingLink = sTesting?.source_url;
  const testingSourceName = sTesting?.source_name;

  const sDocs = message.structured_documents;
  const sJourney = message.structured_compliance_journey;

  return (
    <div className="flex flex-col animate-fade-in mb-8 w-full font-sans">

      {/* PRIMARY STEPPER JOURNEY */}
      <div className="w-full bg-white border border-slate-200 rounded-sm shadow-sm overflow-hidden mb-6">
        <div className="bg-[#0B1E40] border-b border-[#0B1E40] px-6 py-5 flex justify-between items-center">
          <h3 className="font-bold text-[16px] uppercase tracking-wider text-white">
            {language === 'hi' ? 'आपकी अनुपालन यात्रा' : language === 'mr' ? 'तुमचा अनुपालन प्रवास' : 'Your Compliance Journey'}
          </h3>
        </div>

        <div className="p-0">
          
          {/* STEP 1 */}
          <div className="border-b border-slate-100 p-6 hover:bg-slate-50 transition-colors">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-[#1C4E80] text-white font-bold flex items-center justify-center shrink-0 mt-1">1</div>
              <div>
                <h4 className="text-[12px] font-bold text-slate-500 uppercase tracking-wider mb-1">{language === 'hi' ? 'उत्पाद पहचानें' : language === 'mr' ? 'उत्पादन ओळखा' : 'Identify Product'}</h4>
                <div className="text-[16px] font-bold text-slate-900 mb-1">{sProduct}</div>
                <div className="text-[14px] text-slate-600">{language === 'hi' ? `आप ${sProduct} प्रमाणित करना चाहते हैं।` : language === 'mr' ? `तुम्ही ${sProduct} प्रमाणित करू इच्छिता.` : `You are looking to certify a ${sProduct.toLowerCase()}.`}</div>
              </div>
            </div>
          </div>

          {/* STEP 2 */}
          <div className="border-b border-slate-100 p-6 hover:bg-slate-50 transition-colors">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-[#1C4E80] text-white font-bold flex items-center justify-center shrink-0 mt-1">2</div>
              <div>
                <h4 className="text-[12px] font-bold text-slate-500 uppercase tracking-wider mb-1">{language === 'hi' ? 'लागू मानक' : language === 'mr' ? 'लागू मानक' : 'Applicable Standard'}</h4>
                <div className="text-[16px] font-bold text-slate-900 mb-2">{sStandard}</div>
                {message.why_applicable && (
                  <div className="text-[14px] text-slate-600 bg-white border border-slate-200 p-4 rounded-sm shadow-sm">
                    <p className="font-bold text-[#0B1E40] mb-1 text-[13px] uppercase tracking-wider">{language === 'hi' ? 'यह मानक क्यों?' : language === 'mr' ? 'हे मानक का?' : 'Why this standard?'}</p>
                    <p>{message.why_applicable}</p>
                    {message.sources && message.sources.length > 0 && message.sources[0].source_url && (
                      <div className="mt-3">
                        <a href={message.sources[0].source_url} target="_blank" rel="noopener noreferrer" className="text-[#1C4E80] font-bold text-[13px] hover:underline inline-flex items-center gap-1">
                          {language === 'hi' ? 'आधिकारिक स्रोत खोलें' : language === 'mr' ? 'अधिकृत स्रोत उघडा' : 'Open Official Source'} <span className="text-[10px]">↗</span>
                        </a>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* STEP 3 */}
          <div className="border-b border-slate-100 p-6 hover:bg-slate-50 transition-colors">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-[#1C4E80] text-white font-bold flex items-center justify-center shrink-0 mt-1">3</div>
              <div className="w-full">
                <h4 className="text-[12px] font-bold text-slate-500 uppercase tracking-wider mb-1">{language === 'hi' ? 'अनुपालन मार्ग' : language === 'mr' ? 'अनुपालन मार्ग' : 'Compliance Pathway'}</h4>
                {sScheme ? (
                  <>
                    <div className="text-[16px] font-bold text-slate-900 mb-2">{sScheme}</div>
                    <div className="text-[14px] text-slate-600 mb-4">
                      {language === 'hi' ? `${sProduct} ManakAI ज्ञानकोष में दर्शाए गए लागू ${sScheme} मार्ग के अंतर्गत आता है।` : language === 'mr' ? `${sProduct} ManakAI ज्ञानकोशामध्ये दर्शविलेल्या लागू ${sScheme} मार्गांतर्गत येतो.` : `${sProduct} falls under the applicable ${sScheme} pathway represented in the curated ManakAI knowledge base.`}
                    </div>
                    {sJourney?.scheme_source_url && (
                      <a href={sJourney.scheme_source_url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 bg-[#E08A2C] text-white px-4 py-2 rounded-sm text-[13px] font-bold hover:bg-[#c97a24] transition-colors shadow-sm">
                        {language === 'hi' ? `आधिकारिक ${sJourney.scheme_source_name || 'पोर्टल'} खोलें` : language === 'mr' ? `अधिकृत ${sJourney.scheme_source_name || 'पोर्टल'} उघडा` : `Open Official ${sJourney.scheme_source_name || 'Portal'}`} <span className="text-[10px]">↗</span>
                      </a>
                    )}
                  </>
                ) : (
                  <div className="text-[14px] text-slate-600 italic">{language === 'hi' ? 'विवरण की पुष्टि आवश्यक है।' : language === 'mr' ? 'तपशीलांना पुष्टीकरण आवश्यक आहे.' : 'Details require confirmation.'}</div>
                )}
              </div>
            </div>
          </div>

          {/* STEP 4 */}
          <div className="border-b border-slate-100 p-6 hover:bg-slate-50 transition-colors">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-[#1C4E80] text-white font-bold flex items-center justify-center shrink-0 mt-1">4</div>
              <div className="w-full">
                <h4 className="text-[12px] font-bold text-slate-500 uppercase tracking-wider mb-1">{language === 'hi' ? 'उत्पाद परीक्षण' : language === 'mr' ? 'उत्पादन चाचणी' : 'Product Testing'}</h4>
                {testingText ? (
                  <>
                    <div className="text-[14px] text-slate-700 mb-4">
                      {testingText}
                      {testingLink && (
                        <p className="mt-2 text-[13px] text-slate-500">
                          {language === 'hi' ? 'आगे बढ़ने से पहले एक मान्यता प्राप्त प्रयोगशाला की पहचान करने और उसके दायरे की जांच करने के लिए BIS प्रयोगशाला निर्देशिका का उपयोग करें।' : language === 'mr' ? 'पुढे जाण्यापूर्वी मान्यताप्राप्त प्रयोगशाळा ओळखण्यासाठी आणि तिची व्याप्ती तपासण्यासाठी BIS प्रयोगशाळा निर्देशिकेचा वापर करा.' : 'Use the BIS laboratory directory to identify a recognized laboratory and check its scope before proceeding.'}
                        </p>
                      )}
                    </div>
                    {testingLink && (
                      <a href={testingLink} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 bg-white border border-slate-300 text-slate-700 px-4 py-2 rounded-sm text-[13px] font-bold hover:bg-slate-50 hover:border-slate-400 transition-colors shadow-sm">
                        {language === 'hi' ? `खोजें ${testingSourceName || "BIS-मान्यता प्राप्त प्रयोगशालाएं"}` : language === 'mr' ? `शोधा ${testingSourceName || "BIS-मान्यताप्राप्त प्रयोगशाळा"}` : `Find ${testingSourceName || "BIS-Recognized Laboratories"}`} <span className="text-[10px]">↗</span>
                      </a>
                    )}
                  </>
                ) : (
                  <div className="text-[14px] text-slate-600 italic">{language === 'hi' ? 'विवरण की पुष्टि आवश्यक है।' : language === 'mr' ? 'तपशीलांना पुष्टीकरण आवश्यक आहे.' : 'Details require confirmation.'}</div>
                )}
              </div>
            </div>
          </div>

          {/* STEP 5 */}
          <div className="border-b border-slate-100 p-6 hover:bg-slate-50 transition-colors bg-slate-50/50">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-[#1C4E80] text-white font-bold flex items-center justify-center shrink-0 mt-1">5</div>
              <div className="w-full">
                <h4 className="text-[12px] font-bold text-slate-500 uppercase tracking-wider mb-4">{language === 'hi' ? 'आवश्यक दस्तावेज़' : language === 'mr' ? 'आवश्यक कागदपत्रे' : "Documents You'll Need"}</h4>
                {sDocs && sDocs.length > 0 ? (
                  <div className="grid grid-cols-1 gap-4">
                    {sDocs.map((doc, idx) => (
                      <div key={idx} className="bg-white border border-slate-200 rounded-sm p-4 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4 hover:border-[#1C4E80]/40 transition-colors">
                        <div className="flex items-start gap-3">
                          <div className="mt-0.5 text-green-600 font-bold">✓</div>
                          <div>
                            <div className="font-bold text-[14px] text-slate-900">{doc.title}</div>
                            {doc.source_name && (
                              <div className="text-[12px] text-slate-500 font-medium">{doc.source_name}</div>
                            )}
                            {doc.purpose && (
                              <div className="text-[13px] text-slate-600 mt-1">{doc.purpose}</div>
                            )}
                            {!doc.source_url && !doc.purpose && doc.source_name && doc.source_name.includes("brand") && (
                              <div className="text-[13px] text-slate-600 mt-1">{language === 'hi' ? 'ब्रांड स्वामी/निर्माता से प्राप्त करें।' : language === 'mr' ? 'ब्रँड मालक/निर्माता कडून मिळवा.' : 'Obtain from the brand owner/manufacturer.'}</div>
                            )}
                          </div>
                        </div>
                        {doc.source_url && (
                          <div className="shrink-0">
                            <a href={doc.source_url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1.5 bg-white border border-[#1C4E80] text-[#1C4E80] px-3 py-1.5 rounded-sm text-[12px] font-bold hover:bg-[#1C4E80] hover:text-white transition-colors">
                              Open {doc.title === 'PAN' ? 'PAN Service' : doc.title === 'GST' ? 'GST Portal' : doc.title === 'Incorporation' ? 'MCA' : doc.source_name} <span className="text-[10px]">↗</span>
                            </a>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-[14px] text-slate-600 italic">{language === 'hi' ? 'विवरण की पुष्टि आवश्यक है।' : language === 'mr' ? 'तपशीलांना पुष्टीकरण आवश्यक आहे.' : 'Details require confirmation.'}</div>
                )}
              </div>
            </div>
          </div>

          {/* STEP 6 */}
          <div className="p-6 hover:bg-slate-50 transition-colors">
            <div className="flex items-start gap-4">
              <div className="w-8 h-8 rounded-full bg-[#1C4E80] text-white font-bold flex items-center justify-center shrink-0 mt-1">6</div>
              <div className="w-full">
                <h4 className="text-[12px] font-bold text-slate-500 uppercase tracking-wider mb-4">{language === 'hi' ? 'आगे क्या करें' : language === 'mr' ? 'पुढे काय करावे' : 'What To Do Next'}</h4>
                {sJourney?.steps && sJourney.steps.length > 0 ? (
                  <ol className="list-decimal list-inside space-y-2 mb-6 text-[14px] text-slate-700 font-medium ml-1">
                    {sJourney.steps.map((step, idx) => (
                      <li key={idx} className="pl-2">{step}</li>
                    ))}
                  </ol>
                ) : (
                  <ul className="list-disc list-inside space-y-2 mb-6 text-[14px] text-slate-700 font-medium ml-1">
                    {message.next_actions?.map((act, idx) => (
                      <li key={idx}>{act}</li>
                    ))}
                  </ul>
                )}

                <div className="flex flex-wrap gap-3">
                  {sJourney?.scheme_source_url && (
                    <a href={sJourney.scheme_source_url} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 bg-[#0B1E40] text-white px-5 py-2.5 rounded-sm text-[13px] font-bold hover:bg-[#152F5A] transition-colors shadow-sm">
                      {language === 'hi' ? `आधिकारिक ${sJourney.scheme_source_name || 'पोर्टल'} खोलें` : language === 'mr' ? `अधिकृत ${sJourney.scheme_source_name || 'पोर्टल'} उघडा` : `Open Official ${sJourney.scheme_source_name || 'Portal'}`} <span className="text-[10px]">↗</span>
                    </a>
                  )}
                  {testingLink && (
                    <a href={testingLink} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 bg-white border border-slate-300 text-slate-700 px-5 py-2.5 rounded-sm text-[13px] font-bold hover:bg-slate-50 transition-colors shadow-sm">
                      {language === 'hi' ? 'BIS-मान्यता प्राप्त प्रयोगशालाएं खोजें' : language === 'mr' ? 'BIS-मान्यताप्राप्त प्रयोगशाळा शोधा' : 'Find BIS-Recognized Laboratories'} <span className="text-[10px]">↗</span>
                    </a>
                  )}
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  );
}
