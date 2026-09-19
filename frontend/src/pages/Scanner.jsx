import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ComplianceJourney from '../components/ComplianceJourney.jsx';
import EvidencePanel from '../components/EvidencePanel.jsx';
import MsmeComplianceRoadmap from '../components/MsmeComplianceRoadmap.jsx';
import NoVerifiedMatch from '../components/NoVerifiedMatch.jsx';
import { api } from '../api.js';

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

  // Rendering
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 min-h-[80vh]">
      <div className="mb-6">
         <button onClick={() => navigate(-1)} className="text-[#1C4E80] hover:underline font-medium">&larr; Back</button>
      </div>

      {mode === 'select' && (
        <div className="bg-white border border-slate-200 shadow-sm p-8 text-center rounded-md">
          <h1 className="text-2xl font-bold text-[#0B1E40] mb-4">📷 Scan & Understand Product</h1>
          <p className="text-slate-600 mb-8 max-w-lg mx-auto">Upload a product photo, use your camera, or upload a product document (PDF) to verify BIS compliance requirements.</p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button onClick={startCamera} className="bg-[#0B1E40] hover:bg-[#152F5A] text-white px-6 py-3 rounded-md font-semibold shadow-sm flex items-center justify-center gap-2">
              📷 Scan with Camera
            </button>
            <label className="bg-white border-2 border-[#1C4E80] text-[#1C4E80] hover:bg-slate-50 px-6 py-3 rounded-md font-semibold cursor-pointer shadow-sm flex items-center justify-center gap-2">
              📁 Upload Product
              <input type="file" accept="image/jpeg,image/png,image/webp,application/pdf" className="hidden" onChange={handleFileUpload} />
            </label>
          </div>
          <p className="text-xs text-slate-500 mt-6">Supported: JPG • JPEG • PNG • WEBP • PDF (Max 10MB)</p>
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
          {/* Top Section */}
          <div className="bg-white border border-slate-200 p-6 rounded-md shadow-sm">
            <h2 className="text-sm font-bold text-[#1C4E80] uppercase tracking-wider mb-4 border-b border-slate-100 pb-2">Product Identified</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div><span className="block text-xs text-slate-500">Product</span><span className="font-semibold text-slate-900">{results.product_identification.name}</span></div>
              <div><span className="block text-xs text-slate-500">Brand</span><span className="font-semibold text-slate-900">{results.product_identification.brand}</span></div>
              <div><span className="block text-xs text-slate-500">Model</span><span className="font-semibold text-slate-900">{results.product_identification.model}</span></div>
              <div><span className="block text-xs text-slate-500">Confidence</span><span className="font-semibold text-slate-900">{(results.product_identification.confidence * 100).toFixed(0)}%</span></div>
            </div>

            <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">Product Attributes</h3>
            <div className="bg-slate-50 p-4 rounded-sm text-sm text-slate-700 font-mono">
               {Object.entries(results.attributes || {}).map(([k, v]) => (
                 <div key={k} className="flex"><span className="w-32 font-bold capitalize">{k}:</span> <span>{typeof v === 'object' ? JSON.stringify(v) : v}</span></div>
               ))}
            </div>
          </div>

          {/* Compliance Results */}
          {!results.match_found ? (
            <NoVerifiedMatch
              language={language}
              fallbackQuery={results.product_identification.name}
            />
          ) : (
            <>
              {/* Applicability */}
              <div className="bg-white border border-[#E08A2C] p-6 rounded-md shadow-sm">
                <h2 className="text-sm font-bold text-[#E08A2C] uppercase tracking-wider mb-4">BIS Applicability</h2>
                <div className="text-lg font-bold text-slate-900 mb-2">{results.applicable_standard}</div>
                <div className="text-slate-700 mb-4">{results.why_applicable}</div>
                <div className="inline-block bg-slate-100 text-slate-800 text-xs px-2 py-1 rounded border border-slate-200">Scheme: {results.scheme}</div>
              </div>

              {/* A-to-Z Journey */}
              {results.structured_compliance_journey && (
                 <ComplianceJourney
                    steps={results.structured_compliance_journey}
                    language={language}
                 />
              )}

              {/* Documents */}
              {results.structured_documents && results.structured_documents.length > 0 && (
                <div className="bg-white border border-slate-200 p-6 rounded-md shadow-sm">
                  <h3 className="text-lg font-bold text-[#0B1E40] mb-4">Required Documents</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {results.structured_documents.map((d, i) => (
                      <div key={i} className="border border-slate-200 p-4 rounded-sm">
                        <div className="font-semibold text-slate-800 mb-1">{d.title}</div>
                        <div className="text-sm text-slate-600 mb-2">{d.status_reason}</div>
                        {d.official_url && <a href={d.official_url} target="_blank" rel="noreferrer" className="text-sm text-blue-600 hover:underline">Official Source</a>}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Testing */}
              {results.structured_testing && (
                <div className="bg-white border border-slate-200 p-6 rounded-md shadow-sm">
                   <h3 className="text-lg font-bold text-[#0B1E40] mb-4">Testing</h3>
                   <div className="text-slate-700 mb-2 font-medium">Testing Required: {results.structured_testing.required ? "Yes" : "No"}</div>
                   <div className="text-slate-600 mb-4">{results.structured_testing.laboratory_guidance || "Specific laboratory selection is not verified in the current knowledge base."}</div>
                   {results.structured_testing.official_source_url && (
                     <a href={results.structured_testing.official_source_url} target="_blank" rel="noreferrer" className="text-blue-600 font-medium hover:underline">View BIS Recognized Laboratories</a>
                   )}
                </div>
              )}

              {/* Official Links */}
              {results.official_links && results.official_links.length > 0 && (
                <div className="bg-slate-50 border border-slate-200 p-6 rounded-md shadow-sm">
                  <h3 className="text-lg font-bold text-[#0B1E40] mb-4">Official Sources</h3>
                  <ul className="space-y-2">
                    {results.official_links.map((lnk, i) => (
                       <li key={i}>
                         <a href={lnk.url} target="_blank" rel="noreferrer" className="text-blue-700 hover:underline font-medium">{lnk.title}</a>
                       </li>
                    ))}
                  </ul>
                </div>
              )}
            </>
          )}

          <div className="bg-white border-t border-slate-200 pt-6">
            <h3 className="text-md font-bold text-slate-800 mb-2">What should I do next?</h3>
            <ul className="list-disc pl-5 text-slate-600 space-y-1">
               {results.next_actions?.map((na, i) => <li key={i}>{na}</li>)}
            </ul>
          </div>
        </div>
      )}

    </div>
  );
}
