import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ComplianceJourney from '../components/ComplianceJourney.jsx';
import { api } from '../api.js';
import { t } from '../i18n.js';

export default function Scanner({ language }) {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [mode, setMode] = useState('select'); // select, camera, upload, processing, results, error, multiple
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [results, setResults] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');
  const [uploadQuery, setUploadQuery] = useState('');

  // Camera handling
  const startCamera = async () => {
    setMode('camera');
    try {
      const ms = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
      streamRef.current = ms;
      if (videoRef.current) {
        videoRef.current.srcObject = ms;
      }
    } catch (err) {
      setErrorMsg('Camera access denied or unavailable.');
      setMode('error');
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop());
      streamRef.current = null;
    }
  };

  const capturePhoto = () => {
    if (!videoRef.current) return;
    const canvas = document.createElement('canvas');
    canvas.width = videoRef.current.videoWidth;
    canvas.height = videoRef.current.videoHeight;
    canvas.getContext('2d').drawImage(videoRef.current, 0, 0);
    canvas.toBlob((blob) => {
      const f = new File([blob], 'camera-capture.jpg', { type: 'image/jpeg' });
      setFile(f);
      setPreview(URL.createObjectURL(blob));
      stopCamera();
      setMode('upload');
    }, 'image/jpeg', 0.9);
  };

  useEffect(() => {
    return () => stopCamera();
  }, []);

  const handleFileUpload = (e) => {
    const f = e.target.files[0];
    if (!f) return;
    if (f.size > 10 * 1024 * 1024) {
      setErrorMsg('File too large (max 10MB)');
      setMode('error');
      return;
    }
    setFile(f);
    if (f.type.startsWith('image/')) {
      setPreview(URL.createObjectURL(f));
    } else {
      setPreview(null);
    }
    setMode('upload');
  };

  const submitAnalysis = async (selectedProductQuery = '') => {
    setMode('processing');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('language', language);
    if (selectedProductQuery || uploadQuery) {
        formData.append('query', selectedProductQuery || uploadQuery);
    }

    try {
      const data = await api.analyzeProduct(formData);
      if (data.product_identification?.status === 'multiple_products') {
          setResults(data);
          setMode('multiple');
      } else {
          setResults(data);
          setMode('results');
      }
    } catch (err) {
      setErrorMsg(err.message || 'Analysis failed. Backend unavailable.');
      setMode('error');
    }
  };

  const confidenceLevel = results?.confidence_level || (
    (results?.product_identification?.confidence || 0) >= 0.75 ? 'high' :
    (results?.product_identification?.confidence || 0) >= 0.50 ? 'medium' : 'low'
  );
  const confidencePercent = Math.round((results?.product_identification?.confidence || 0) * 100);

  // Rendering
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 min-h-[80vh]">
      <div className="mb-6">
         <button onClick={() => navigate(-1)} className="text-[#1C4E80] hover:underline font-medium">&larr; Back</button>
      </div>

      {mode === 'select' && (
        <div className="bg-white border border-slate-200 shadow-sm p-8 text-center rounded-md">
          <h1 className="text-2xl font-bold text-[#0B1E40] mb-4">{t(language, 'scanner_title')}</h1>
          <p className="text-slate-600 mb-8 max-w-lg mx-auto">{t(language, 'scanner_description')}</p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button onClick={startCamera} className="bg-[#0B1E40] hover:bg-[#152F5A] text-white px-6 py-3 rounded-md font-semibold shadow-sm flex items-center justify-center gap-2">
              {t(language, 'scanner_camera')}
            </button>
            <label className="bg-white border-2 border-[#1C4E80] text-[#1C4E80] hover:bg-slate-50 px-6 py-3 rounded-md font-semibold cursor-pointer shadow-sm flex items-center justify-center gap-2">
              {t(language, 'scanner_upload')}
              <input type="file" accept="image/jpeg,image/png,image/webp,application/pdf" className="hidden" onChange={handleFileUpload} />
            </label>
          </div>
          <p className="text-xs text-slate-500 mt-6">{t(language, 'scanner_supported')}</p>
        </div>
      )}

      {mode === 'camera' && (
        <div className="bg-black text-white p-4 rounded-md flex flex-col items-center">
          <video ref={videoRef} autoPlay playsInline className="max-w-full h-auto max-h-[60vh] object-contain mb-4 rounded-sm bg-slate-900" />
          <div className="flex gap-4">
            <button onClick={capturePhoto} className="bg-white text-black px-6 py-2 rounded-full font-bold">Capture</button>
            <button onClick={() => {stopCamera(); setMode('select')}} className="bg-red-600 px-6 py-2 rounded-full font-bold">Cancel</button>
          </div>
        </div>
      )}

      {mode === 'upload' && (
        <div className="bg-white border border-slate-200 shadow-sm p-8 text-center rounded-md max-w-2xl mx-auto">
          {preview ? (
            <img src={preview} alt="Preview" className="max-w-full h-auto max-h-64 mx-auto mb-4 rounded-sm border border-slate-300" />
          ) : (
            <div className="h-32 bg-slate-100 flex items-center justify-center mb-4 rounded-sm border border-slate-300">
               <span className="text-slate-500 font-medium">{file?.name}</span>
            </div>
          )}

          <div className="mb-6 text-left">
            <label className="block text-sm font-semibold text-slate-700 mb-2">Optional: Describe your product (Manual Override)</label>
            <input
              type="text"
              value={uploadQuery}
              onChange={(e) => setUploadQuery(e.target.value)}
              placeholder="e.g. I am checking a 20L packaged drinking water bottle"
              className="w-full border border-slate-300 rounded-sm px-4 py-2"
            />
          </div>

          <div className="flex gap-4 justify-center">
            <button onClick={() => submitAnalysis()} className="bg-[#0B1E40] text-white px-8 py-3 rounded-md font-bold shadow-sm">Analyze Product</button>
            <button onClick={() => {setFile(null); setPreview(null); setMode('select')}} className="border border-slate-300 px-6 py-3 rounded-md font-semibold text-slate-700">Cancel</button>
          </div>
        </div>
      )}

      {mode === 'processing' && (
        <div className="text-center py-20">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-[#1C4E80] mb-4"></div>
          <h2 className="text-xl font-bold text-[#1C4E80]">Analyzing product...</h2>
          <p className="text-slate-600">Reading visible information and checking BIS knowledge base.</p>
        </div>
      )}

      {mode === 'error' && (
        <div className="bg-red-50 border-l-4 border-red-600 p-6 rounded-r-md">
          <h3 className="text-red-800 font-bold text-lg mb-2">Analysis Failed</h3>
          <p className="text-red-700 mb-4">{errorMsg}</p>
          <button onClick={() => setMode('select')} className="bg-red-100 text-red-800 px-4 py-2 rounded-sm font-medium hover:bg-red-200">Try Again</button>
        </div>
      )}

      {mode === 'multiple' && results && (
        <div className="bg-white border border-slate-200 p-6 rounded-md">
          <h2 className="text-xl font-bold text-[#0B1E40] mb-4">Multiple products detected</h2>
          <p className="text-slate-600 mb-6">We identified multiple products in this file. Please select one for detailed BIS analysis.</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {results.multiple_candidates?.map((cand, i) => (
              <button key={i} onClick={() => submitAnalysis(cand.name)} className="border border-slate-300 p-4 rounded-md hover:border-[#1C4E80] hover:bg-slate-50 text-left transition-colors">
                <div className="font-bold text-[#0B1E40]">{cand.name}</div>
                <div className="text-sm text-slate-500">{cand.category}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      {mode === 'results' && results && (
        <div className="space-y-8">
          {/* Product identification */}
          <div className="bg-white border border-slate-200 p-6 rounded-md shadow-sm">
            <h2 className="text-sm font-bold text-[#1C4E80] uppercase tracking-wider mb-4 border-b border-slate-100 pb-2">{t(language, confidenceLevel === 'high' ? 'scanner_identified' : confidenceLevel === 'medium' ? 'scanner_possible' : 'scanner_unable')}</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div><span className="block text-xs text-slate-500">{t(language, 'scanner_product')}</span><span className="font-semibold text-slate-900">{results.product_identification.name}</span></div>
              <div><span className="block text-xs text-slate-500">{t(language, 'scanner_category')}</span><span className="font-semibold text-slate-900">{results.product_identification.category}</span></div>
              <div><span className="block text-xs text-slate-500">{t(language, 'scanner_confidence')}</span><span className="font-semibold text-slate-900">{confidencePercent}%</span></div>
              <div><span className="block text-xs text-slate-500">{t(language, 'scanner_status')}</span><span className={`font-semibold ${confidenceLevel === 'low' ? 'text-amber-700' : 'text-emerald-700'}`}>{t(language, `scanner_${confidenceLevel}`)}</span></div>
            </div>
            {preview && <img src={preview} alt={t(language, 'scanner_preview')} className="max-w-full h-auto max-h-72 mx-auto rounded-sm border border-slate-300" />}
          </div>

          {/* Detected information */}
          <div className="bg-white border border-slate-200 p-6 rounded-md shadow-sm">
            <h2 className="text-sm font-bold text-[#1C4E80] uppercase tracking-wider mb-4">{t(language, 'scanner_detected_information')}</h2>
            <div className="space-y-3 text-sm text-slate-700">
              <div><span className="font-bold">{t(language, 'scanner_ocr')}:</span> {results.detected_information?.ocr_text || t(language, 'scanner_not_detected')}</div>
              <div><span className="font-bold">{t(language, 'scanner_brand')}:</span> {results.detected_information?.brand || results.product_identification.brand || t(language, 'scanner_not_detected')}</div>
              <div><span className="font-bold">{t(language, 'scanner_model')}:</span> {results.detected_information?.model || results.product_identification.model || t(language, 'scanner_not_detected')}</div>
              <div><span className="font-bold">{t(language, 'scanner_bis_info')}:</span> {(results.detected_information?.bis_information || []).join(', ') || t(language, 'scanner_not_detected')}</div>
              <div><span className="font-bold">{t(language, 'scanner_attributes')}:</span> {Object.entries(results.attributes || {}).map(([key, value]) => `${key}: ${typeof value === 'object' ? JSON.stringify(value) : value}`).join('; ') || t(language, 'scanner_not_detected')}</div>
            </div>
          </div>

          {/* BIS compliance guidance */}
          {confidenceLevel === 'low' ? (
            <div className="bg-amber-50 border border-amber-300 p-6 rounded-md shadow-sm">
              <p className="font-semibold text-amber-900">{t(language, 'scanner_retry_message')}</p>
              <div className="mt-4 flex flex-col sm:flex-row gap-3">
                <button onClick={() => { setResults(null); startCamera(); }} className="border border-amber-700 text-amber-900 px-4 py-2 rounded-sm font-bold">{t(language, 'scanner_retake')}</button>
                <label className="border border-amber-700 text-amber-900 px-4 py-2 rounded-sm font-bold cursor-pointer text-center">{t(language, 'scanner_upload_another')}<input type="file" accept="image/jpeg,image/png,image/webp,application/pdf" className="hidden" onChange={handleFileUpload} /></label>
              </div>
            </div>
          ) : !results.match_found ? (
            <div className="bg-white border border-slate-200 p-6 rounded-md shadow-sm">
              <h2 className="text-sm font-bold text-[#1C4E80] uppercase tracking-wider mb-3">{t(language, 'scanner_bis_guidance')}</h2>
              <p className="font-semibold text-slate-900">{t(language, 'scanner_no_verified_info')}</p>
              <div className="mt-5 flex flex-col sm:flex-row gap-3"><button onClick={() => navigate('/assistant', { state: { prefill: results.product_identification.name } })} className="px-4 py-2 bg-[#0B1E40] text-white font-bold rounded-sm">{t(language, 'scanner_ask')}</button><button onClick={() => navigate('/assistant', { state: { prefill: `Please help me identify the applicable BIS information for ${results.product_identification.name}.` } })} className="px-4 py-2 border border-[#1C4E80] text-[#1C4E80] font-bold rounded-sm">{t(language, 'scanner_detailed_query')}</button><button onClick={() => navigate('/services')} className="px-4 py-2 border border-[#1C4E80] text-[#1C4E80] font-bold rounded-sm">{t(language, 'scanner_service')}</button></div>
            </div>
          ) : (
            <>
              {/* Applicability */}
              <div className="bg-white border border-[#E08A2C] p-6 rounded-md shadow-sm">
                <h2 className="text-sm font-bold text-[#E08A2C] uppercase tracking-wider mb-4">{t(language, 'why_this_standard')}</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-700">
                  <div className="font-bold">{t(language, 'product_identified')}:</div>
                  <div>{results.product_identification.name}</div>
                  <div className="font-bold">{t(language, 'applicable_standard')}:</div>
                  <div className="text-lg text-slate-900 font-bold">{results.applicable_standard}</div>
                  <div className="font-bold">{t(language, 'reason')}:</div>
                  <div>{results.why_applicable || 'Based on BIS CRS/ISI guidelines for this product category.'}</div>
                  <div className="font-bold">{t(language, 'evidence')}:</div>
                  <div>Official BIS Knowledge Base</div>
                  <div className="font-bold">{t(language, 'source_status')}:</div>
                  <div className="text-green-700 font-bold">Verified</div>
                </div>
                {results.official_links && results.official_links.length > 0 && (
                  <div className="mt-4">
                    <a href={results.official_links[0].url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-2 bg-[#1C4E80] text-white px-4 py-2 rounded-sm text-xs font-bold uppercase tracking-wider hover:bg-[#0B1E40] transition-colors">
                      OPEN OFFICIAL SOURCE
                    </a>
                  </div>
                )}
              </div>

              {/* A-to-Z Journey */}
              <ComplianceJourney
                message={{
                  product: results.product_identification.name,
                  applicable_standard: results.applicable_standard,
                  scheme: results.scheme,
                  compliance_journey: {
                    scheme: results.scheme,
                    next_action: results.next_actions?.[0],
                    steps: results.next_actions || []
                  },
                  structured_compliance_journey: results.structured_compliance_journey,
                  structured_testing: results.structured_testing,
                  structured_documents: results.structured_documents,
                  official_sources: results.sources
                }}
                language={language}
              />
            </>
          )}

          {results.reference_guidance && (
            <div className="bg-white border border-[#E08A2C] p-6 rounded-md shadow-sm">
              <h2 className="text-sm font-bold text-[#E08A2C] uppercase tracking-wider mb-2">{t(language, 'scanner_reference_guidance')}</h2>
              <p className="text-sm font-semibold text-slate-800 mb-4">{results.reference_guidance.status}</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-700">
                <div><span className="font-bold">{t(language, 'scanner_validity')}:</span> {results.reference_guidance.validity}</div>
                <div><span className="font-bold">{t(language, 'scanner_regulatory_status')}:</span> {results.reference_guidance.regulatory_status}</div>
                <div><span className="font-bold">{t(language, 'scanner_bis_scheme')}:</span> {results.reference_guidance.scheme}</div>
                <div><span className="font-bold">{t(language, 'scanner_applicant')}:</span> {results.reference_guidance.applicant}</div>
                <div><span className="font-bold">{t(language, 'scanner_testing')}:</span> {results.reference_guidance.testing}</div>
                <div><span className="font-bold">{t(language, 'scanner_fees')}:</span> {results.reference_guidance.fees}</div>
              </div>
              <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-700">
                <div><span className="font-bold">{t(language, 'scanner_documents')}:</span><ul className="list-disc pl-5 mt-1">{results.reference_guidance.documents?.map((item) => <li key={item}>{item}</li>)}</ul></div>
                <div><span className="font-bold">{t(language, 'scanner_application_process')}:</span><ol className="list-decimal pl-5 mt-1">{results.reference_guidance.application_process?.map((item) => <li key={item}>{item}</li>)}</ol></div>
              </div>
              <p className="mt-4 text-sm text-slate-700"><span className="font-bold">{t(language, 'scanner_marking')}:</span> {results.reference_guidance.marking}</p>
              <p className="mt-2 text-sm text-slate-700"><span className="font-bold">{t(language, 'scanner_post_registration')}:</span> {results.reference_guidance.post_registration?.join(' ')}</p>
              <p className="mt-3 text-sm text-amber-800">{results.reference_guidance.important}</p>
            </div>
          )}

          <div className="bg-slate-50 border border-slate-200 p-6 rounded-md shadow-sm">
            <h2 className="text-sm font-bold text-[#1C4E80] uppercase tracking-wider mb-3">{t(language, 'scanner_sources')}</h2>
            <p className="text-sm text-slate-700">{t(language, 'scanner_ai_evidence')}: {(results.product_identification.evidence || []).join(', ') || t(language, 'scanner_not_detected')}</p>
            <p className="text-sm text-slate-700 mt-2">{t(language, 'scanner_verified_sources')}: {results.match_found ? (results.sources?.map((source) => source.source_name || source.title).join(', ') || t(language, 'scanner_not_detected')) : t(language, 'scanner_no_verified_info')}</p>
            {results.official_links?.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-3">
                {results.official_links.map((source) => <a key={source.url} href={source.url} target="_blank" rel="noreferrer" className="text-sm font-bold text-[#1C4E80] underline">{source.title || source.url}</a>)}
              </div>
            )}
          </div>

        </div>
      )}

    </div>
  );
}
