import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { t } from '../i18n.js'
import { api } from '../api.js'
import EvidencePanel from '../components/EvidencePanel.jsx'

export default function Consumer({ language }) {
  const navigate = useNavigate()
  const [kbybInput, setKbybInput] = useState('')
  const [kbybResult, setKbybResult] = useState(null)
  const [kbybLoading, setKbybLoading] = useState(false)
  const [kbybNotFound, setKbybNotFound] = useState(false)

  const [verifyInput, setVerifyInput] = useState('')
  const [verifyResult, setVerifyResult] = useState(null)
  const [verifyLoading, setVerifyLoading] = useState(false)
  const [verifyNotFound, setVerifyNotFound] = useState(false)

  const [complaintInput, setComplaintInput] = useState('')
  const [complaintResult, setComplaintResult] = useState(null)
  const [complaintLoading, setComplaintLoading] = useState(false)
  const [complaintNotFound, setComplaintNotFound] = useState(false)

  async function handleKbybSearch() {
    if (!kbybInput.trim() || kbybLoading) return
    setKbybLoading(true)
    setKbybNotFound(false)
    setKbybResult(null)
    try {
      const res = await api.standardSearch(kbybInput, language)
      if (res.confidence === 'none') {
        setKbybNotFound(true)
      } else {
        setKbybResult(res)
      }
    } catch (e) {
      setKbybNotFound(true)
    } finally {
      setKbybLoading(false)
    }
  }

  async function handleComplaintSearch() {
    if (!complaintInput.trim() || complaintLoading) return
    setComplaintLoading(true)
    setComplaintNotFound(false)
    setComplaintResult(null)
    try {
      const res = await api.assistantQuery({ query: complaintInput, language })
      if (!res.answer || res.confidence === 'none' || res.answer.includes("NO VERIFIED MATCH")) {
        setComplaintNotFound(true)
      } else {
        setComplaintResult(res)
      }
    } catch (e) {
      setComplaintNotFound(true)
    } finally {
      setComplaintLoading(false)
    }
  }

  async function handleVerifySearch() {
    if (!verifyInput.trim() || verifyLoading) return
    setVerifyLoading(true)
    setVerifyNotFound(false)
    setVerifyResult(null)
    try {
      const res = await api.standardSearch(verifyInput, language)
      if (res.confidence === 'none') {
        setVerifyNotFound(true)
      } else {
        setVerifyResult(res)
      }
    } catch (e) {
      setVerifyNotFound(true)
    } finally {
      setVerifyLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">{t(language, 'con_title')}</h1>
      <p className="text-slate-600 mb-8">{t(language, 'con_sub')}</p>

      {/* Verified Safety & Consumer Guidance */}
      <div className="bg-white border border-red-200 rounded-xl p-6 shadow-sm mb-6 relative overflow-hidden">
        <div className="absolute top-0 left-0 w-1 h-full bg-red-500"></div>
        <h2 className="text-xl font-bold text-slate-800 mb-2 flex items-center gap-2">
          <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          {t(language, 'safety_heading')}
        </h2>
        <p className="text-slate-600 text-[14px] mb-5">
          {t(language, 'safety_disclaimer')}
        </p>

        <div className="space-y-4">
          {/* Item 1 */}
          <div className="bg-red-50/50 border border-red-100 rounded-lg p-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-bold text-red-900 text-[15px]">{t(language, 'con_pc')}</h3>
              <span className="text-[11px] font-bold bg-white text-red-700 border border-red-200 px-2 py-0.5 rounded">IS 2347</span>
            </div>
            <p className="text-[13px] text-slate-700 mb-3"><strong>Safety {t(language, 'con_cmp_lbl_guidance')}</strong> {t(language, 'con_pc_desc')}</p>
            <div className="bg-white rounded border border-red-100 p-3 text-[13px]">
              <h4 className="font-bold text-slate-800 mb-1">{t(language, 'safety_what_to_do')}</h4>
              <ul className="list-disc pl-4 text-slate-600 space-y-1">
                <li>{t(language, 'con_pc_do')}</li>
                <li>{t(language, 'con_pc_valve')}</li>
              </ul>
            </div>
            <div className="mt-3 text-[11px] text-slate-500 font-medium">{t(language, 'lbl_source')}: BIS Compulsory Certification (kb-014)</div>
          </div>

          {/* Item 2 */}
          <div className="bg-red-50/50 border border-red-100 rounded-lg p-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-bold text-red-900 text-[15px]">{t(language, 'con_toys')}</h3>
              <span className="text-[11px] font-bold bg-white text-red-700 border border-red-200 px-2 py-0.5 rounded">IS 9873</span>
            </div>
            <p className="text-[13px] text-slate-700 mb-3"><strong>Safety {t(language, 'con_cmp_lbl_guidance')}</strong> {t(language, 'con_toys_desc')}</p>
            <div className="bg-white rounded border border-red-100 p-3 text-[13px]">
              <h4 className="font-bold text-slate-800 mb-1">{t(language, 'safety_what_to_do')}</h4>
              <ul className="list-disc pl-4 text-slate-600 space-y-1">
                <li>{t(language, 'con_toys_do')}</li>
                <li>{t(language, 'con_toys_age')}</li>
              </ul>
            </div>
            <div className="mt-3 text-[11px] text-slate-500 font-medium">{t(language, 'lbl_source')}: Toys (Quality Control) Order, 2020 (kb-010)</div>
          </div>

          {/* Item 3 */}
          <div className="bg-red-50/50 border border-red-100 rounded-lg p-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-bold text-red-900 text-[15px]">{t(language, 'con_lpg')}</h3>
              <span className="text-[11px] font-bold bg-white text-red-700 border border-red-200 px-2 py-0.5 rounded">IS 3196</span>
            </div>
            <p className="text-[13px] text-slate-700 mb-3"><strong>Safety {t(language, 'con_cmp_lbl_guidance')}</strong> {t(language, 'con_lpg_desc')}</p>
            <div className="bg-white rounded border border-red-100 p-3 text-[13px]">
              <h4 className="font-bold text-slate-800 mb-1">{t(language, 'safety_what_to_do')}</h4>
              <ul className="list-disc pl-4 text-slate-600 space-y-1">
                <li>{t(language, 'con_lpg_do')}</li>
                <li>{t(language, 'con_lpg_cml')}</li>
              </ul>
            </div>
            <div className="mt-3 text-[11px] text-slate-500 font-medium">{t(language, 'lbl_source')}: BIS Compulsory Certification (kb-015)</div>
          </div>
        </div>
      </div>

      {/* Know Before You Buy */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm mb-6">
        <h2 className="text-xl font-bold text-slate-800 mb-3">{t(language, 'con_kbyb_title')}</h2>
        <p className="text-slate-600 text-[15px] mb-5">
          {t(language, 'con_kbyb_desc')}
        </p>
        <div className="flex flex-col sm:flex-row gap-2 bg-slate-50 border border-slate-300 rounded-lg p-1.5 focus-within:border-navy-500 focus-within:ring-1 focus-within:ring-navy-500 mb-6">
          <input
            value={kbybInput}
            onChange={(e) => setKbybInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleKbybSearch()}
            placeholder={t(language, 'con_kbyb_ph')}
            className="flex-1 px-3.5 py-2.5 text-[15px] text-slate-900 placeholder-slate-400 focus:outline-none bg-transparent"
          />
          <button
            onClick={handleKbybSearch}
            disabled={kbybLoading}
            className="bg-navy-700 hover:bg-navy-800 disabled:opacity-50 text-white font-semibold text-sm px-6 py-2.5 rounded-md transition-colors whitespace-nowrap"
          >
            {kbybLoading ? 'Checking...' : 'Check Product'}
          </button>
        </div>

        {kbybNotFound && !kbybLoading && (
          <div className="bg-red-50 border border-red-200 rounded-lg py-6 px-4 text-center">
            <h3 className="text-red-800 font-bold mb-1 uppercase tracking-wider text-sm">{t(language, 'lbl_no_match')}</h3>
            <p className="text-red-700 text-[14px]">
              {t(language, 'con_kbyb_nf')}
            </p>
          </div>
        )}

        {kbybResult && !kbybLoading && (
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <div className="bg-navy-50 px-4 py-3 border-b border-slate-200">
              <span className="text-[11px] font-bold text-navy-800 uppercase tracking-wider">{t(language, 'lbl_standard')}</span>
              <div className="text-navy-900 font-bold text-lg">{kbybResult.applicable_standard || kbybResult.standard_number}</div>
            </div>
            <div className="p-4 space-y-4 text-[14px] text-slate-700">
              {kbybResult.scheme && (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'con_lbl_cert_mark')}</h4>
                  <p>{kbybResult.scheme}</p>
                </div>
              )}
              {kbybResult.explanation && (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'con_lbl_guidance')}</h4>
                  <p>{kbybResult.explanation}</p>
                </div>
              )}
              {kbybResult.requirements && kbybResult.requirements.length > 0 && (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'con_lbl_ensures')}</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    {kbybResult.requirements.map((r, i) => <li key={i}>{r}</li>)}
                  </ul>
                </div>
              )}
              <div className="mt-4 pt-4 border-t border-slate-200">
                <EvidencePanel sources={kbybResult.sources} />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Consumer Complaints */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm mb-6">
        <h2 className="text-xl font-bold text-slate-800 mb-3">{t(language, 'con_cmp_title')}</h2>
        <p className="text-slate-600 text-[15px] mb-5">
          {t(language, 'con_cmp_desc')}
        </p>
        <div className="flex flex-col sm:flex-row gap-2 bg-slate-50 border border-slate-300 rounded-lg p-1.5 focus-within:border-navy-500 focus-within:ring-1 focus-within:ring-navy-500 mb-6">
          <input
            value={complaintInput}
            onChange={(e) => setComplaintInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleComplaintSearch()}
            placeholder={t(language, 'con_cmp_ph')}
            className="flex-1 px-3.5 py-2.5 text-[15px] text-slate-900 placeholder-slate-400 focus:outline-none bg-transparent"
          />
          <button
            onClick={handleComplaintSearch}
            disabled={complaintLoading}
            className="bg-navy-700 hover:bg-navy-800 disabled:opacity-50 text-white font-semibold text-sm px-6 py-2.5 rounded-md transition-colors whitespace-nowrap"
          >
            {complaintLoading ? 'Getting Guidance...' : 'Get Guidance'}
          </button>
        </div>

        {complaintNotFound && !complaintLoading && (
          <div className="bg-red-50 border border-red-200 rounded-lg py-6 px-4 text-center">
            <h3 className="text-red-800 font-bold mb-1 uppercase tracking-wider text-sm">{t(language, 'lbl_no_match')}</h3>
            <p className="text-red-700 text-[14px]">
              {t(language, 'con_cmp_nf')}
            </p>
          </div>
        )}

        {complaintResult && !complaintLoading && (
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <div className="bg-blue-50 border-b border-blue-200 px-4 py-3">
              <p className="text-blue-900 text-sm font-semibold">
                {t(language, 'con_cmp_warn')}
              </p>
            </div>
            <div className="p-4 space-y-4 text-[14px] text-slate-700">
              <div>
                <h4 className="font-bold text-slate-800 mb-1">{t(language, 'con_cmp_lbl_guidance')}</h4>
                <div className="whitespace-pre-wrap">{complaintResult.answer}</div>
              </div>

              <div className="mt-4 pt-4 border-t border-slate-200">
                <EvidencePanel sources={complaintResult.sources} />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Product Verification Guidance */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm mb-6">
        <h2 className="text-xl font-bold text-slate-800 mb-3">{t(language, 'con_ver_title')}</h2>
        <p className="text-slate-600 text-[15px] mb-5">
          {t(language, 'con_ver_desc')}
        </p>
        <div className="flex flex-col sm:flex-row gap-2 bg-slate-50 border border-slate-300 rounded-lg p-1.5 focus-within:border-navy-500 focus-within:ring-1 focus-within:ring-navy-500 mb-6">
          <input
            value={verifyInput}
            onChange={(e) => setVerifyInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleVerifySearch()}
            placeholder={t(language, 'con_ver_ph')}
            className="flex-1 px-3.5 py-2.5 text-[15px] text-slate-900 placeholder-slate-400 focus:outline-none bg-transparent"
          />
          <button
            onClick={handleVerifySearch}
            disabled={verifyLoading}
            className="bg-navy-700 hover:bg-navy-800 disabled:opacity-50 text-white font-semibold text-sm px-6 py-2.5 rounded-md transition-colors whitespace-nowrap"
          >
            {verifyLoading ? 'Getting Guidance...' : 'Get Guidance'}
          </button>
        </div>

        {verifyNotFound && !verifyLoading && (
          <div className="bg-red-50 border border-red-200 rounded-lg py-6 px-4 text-center">
            <h3 className="text-red-800 font-bold mb-1 uppercase tracking-wider text-sm">{t(language, 'lbl_no_match')}</h3>
            <p className="text-red-700 text-[14px]">
              {t(language, 'con_ver_nf')}
            </p>
          </div>
        )}

        {verifyResult && !verifyLoading && (
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <div className="bg-blue-50 border-b border-blue-200 px-4 py-3">
              <p className="text-blue-900 text-sm font-semibold">
                {t(language, 'con_ver_warn')}
              </p>
            </div>
            <div className="bg-navy-50 px-4 py-3 border-b border-slate-200">
              <span className="text-[11px] font-bold text-navy-800 uppercase tracking-wider">{t(language, 'lbl_standard')}</span>
              <div className="text-navy-900 font-bold text-lg">{verifyResult.applicable_standard || verifyResult.standard_number}</div>
            </div>
            <div className="p-4 space-y-4 text-[14px] text-slate-700">
              {verifyResult.scheme && (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'con_ver_lbl_check')}</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    <li>{t(language, 'con_ver_valid')} <strong>{verifyResult.scheme}</strong> {t(language, 'con_ver_mark')}</li>
                    <li>{t(language, 'con_ver_is')} <strong>{verifyResult.applicable_standard || verifyResult.standard_number}</strong>.</li>
                    <li>A valid CM/L (licence number) or HUID underneath the {t(language, 'con_ver_mark')}</li>
                  </ul>
                </div>
              )}

              <div>
                <h4 className="font-bold text-slate-800 mb-1">{t(language, 'con_ver_src_lbl')}</h4>
                <p>{t(language, 'con_ver_src_desc')} <strong>{t(language, 'con_ver_app')}</strong> {t(language, 'con_ver_avail')}</p>
              </div>

              <div className="mt-4 pt-4 border-t border-slate-200">
                <EvidencePanel sources={verifyResult.sources} />
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
