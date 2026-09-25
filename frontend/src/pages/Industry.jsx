import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { t } from '../i18n.js'
import { api } from '../api.js'
import EvidencePanel from '../components/EvidencePanel.jsx'

export default function Industry({ language, audience = 'industry' }) {
  const navigate = useNavigate()
  const [compInput, setCompInput] = useState('')
  const [compResult, setCompResult] = useState(null)
  const [compLoading, setCompLoading] = useState(false)
  const [compNotFound, setCompNotFound] = useState(false)

  const [labInput, setLabInput] = useState('')
  const [labResult, setLabResult] = useState(null)
  const [labLoading, setLabLoading] = useState(false)
  const [labNotFound, setLabNotFound] = useState(false)

  async function handleCompSearch() {
    if (!compInput.trim() || compLoading) return
    setCompLoading(true)
    setCompNotFound(false)
    setCompResult(null)
    try {
      const res = await api.standardSearch(compInput, language)
      if (res.confidence === 'none') {
        setCompNotFound(true)
      } else {
        setCompResult(res)
      }
    } catch (e) {
      setCompNotFound(true)
    } finally {
      setCompLoading(false)
    }
  }

  async function handleLabSearch() {
    if (!labInput.trim() || labLoading) return
    setLabLoading(true)
    setLabNotFound(false)
    setLabResult(null)
    try {
      const res = await api.standardSearch(labInput, language)
      if (res.confidence === 'none') {
        setLabNotFound(true)
      } else {
        setLabResult(res)
      }
    } catch (e) {
      setLabNotFound(true)
    } finally {
      setLabLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">{audience === 'msme' ? t(language, 'home_msme_title') : t(language, 'industry_title')}</h1>
      <p className="text-slate-600 mb-8">{audience === 'msme' ? t(language, 'home_msme_desc') : t(language, 'industry_sub')}</p>

      {/* Compliance Guidance */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm mb-6">
        <h2 className="text-xl font-bold text-slate-800 mb-3">{t(language, 'comp_title')}</h2>
        <p className="text-slate-600 text-[15px] mb-5">
          {t(language, 'comp_desc')}
        </p>
        <div className="flex flex-col sm:flex-row gap-2 bg-slate-50 border border-slate-300 rounded-lg p-1.5 focus-within:border-navy-500 focus-within:ring-1 focus-within:ring-navy-500 mb-6">
          <input
            value={compInput}
            onChange={(e) => setCompInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleCompSearch()}
            placeholder={t(language, 'comp_ph')}
            className="flex-1 px-3.5 py-2.5 text-[15px] text-slate-900 placeholder-slate-400 focus:outline-none bg-transparent"
          />
          <button
            onClick={handleCompSearch}
            disabled={compLoading}
            className="bg-navy-700 hover:bg-navy-800 disabled:opacity-50 text-white font-semibold text-sm px-6 py-2.5 rounded-md transition-colors whitespace-nowrap"
          >
            {compLoading ? t(language, 'comp_loading') : t(language, 'comp_btn')}
          </button>
        </div>

        {compNotFound && (
          <div className="text-sm text-red-600 bg-red-50 p-4 rounded-lg border border-red-100">
            {t(language, 'ind_no_match')}
          </div>
        )}

        {compResult && !compLoading && (
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <div className="bg-navy-50 px-4 py-3 border-b border-slate-200">
              <span className="text-[11px] font-bold text-navy-800 uppercase tracking-wider">{t(language, 'ind_lbl_app_std')}</span>
              <div className="text-navy-900 font-bold text-lg">{compResult.applicable_standard || 'General Compliance'}</div>
            </div>
            <div className="p-4 space-y-4 text-[14px] text-slate-700">
              {compResult.scheme && (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'ind_lbl_cert_sch')}</h4>
                  <p>{compResult.scheme}</p>
                </div>
              )}
              {compResult.why_applicable && (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'ind_lbl_comp_guidance')}</h4>
                  <p>{compResult.why_applicable}</p>
                </div>
              )}
              {compResult.certification_steps && compResult.certification_steps.length > 0 && (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'ind_lbl_cert_steps')}</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    {compResult.certification_steps.map((step, idx) => <li key={idx}>{step}</li>)}
                  </ul>
                </div>
              )}
              {compResult.next_actions && compResult.next_actions.length > 0 && (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'ind_lbl_next_act')}</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    {compResult.next_actions.map((act, idx) => <li key={idx}>{act}</li>)}
                  </ul>
                </div>
              )}
              <div className="mt-4 pt-4 border-t border-slate-200">
                <EvidencePanel sources={compResult.sources} />
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Testing & Laboratory Guidance */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm mb-6">
        <h2 className="text-xl font-bold text-slate-800 mb-3">{t(language, 'lab_title')}</h2>
        <p className="text-slate-600 text-[15px] mb-5">
          {t(language, 'lab_desc')}
        </p>
        <div className="flex flex-col sm:flex-row gap-2 bg-slate-50 border border-slate-300 rounded-lg p-1.5 focus-within:border-navy-500 focus-within:ring-1 focus-within:ring-navy-500 mb-6">
          <input
            value={labInput}
            onChange={(e) => setLabInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleLabSearch()}
            placeholder={t(language, 'lab_ph')}
            className="flex-1 px-3.5 py-2.5 text-[15px] text-slate-900 placeholder-slate-400 focus:outline-none bg-transparent"
          />
          <button
            onClick={handleLabSearch}
            disabled={labLoading}
            className="bg-navy-700 hover:bg-navy-800 disabled:opacity-50 text-white font-semibold text-sm px-6 py-2.5 rounded-md transition-colors whitespace-nowrap"
          >
            {labLoading ? t(language, 'comp_loading') : t(language, 'lab_btn')}
          </button>
        </div>

        {labNotFound && (
          <div className="text-sm text-red-600 bg-red-50 p-4 rounded-lg border border-red-100">
            {t(language, 'ind_no_match')}
          </div>
        )}

        {labResult && !labLoading && (
          <div className="border border-slate-200 rounded-lg overflow-hidden">
            <div className="bg-navy-50 px-4 py-3 border-b border-slate-200">
              <span className="text-[11px] font-bold text-navy-800 uppercase tracking-wider">{t(language, 'ind_lbl_app_top')}</span>
              <div className="text-navy-900 font-bold text-lg">{labResult.applicable_standard && labResult.applicable_standard !== "N/A" ? labResult.applicable_standard : labResult.product || 'Laboratory Testing'}</div>
            </div>
            <div className="p-4 space-y-4 text-[14px] text-slate-700">

              {labResult.testing && labResult.testing.length > 0 ? (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'ind_lbl_test_guidance')}</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    {labResult.testing.map((test, idx) => <li key={idx}>{test}</li>)}
                  </ul>
                </div>
              ) : (
                labResult.why_applicable && (
                  <div>
                    <h4 className="font-bold text-slate-800 mb-1">{t(language, 'ind_lbl_guidance')}</h4>
                    <p>{labResult.why_applicable}</p>
                  </div>
                )
              )}

              {labResult.next_actions && labResult.next_actions.length > 0 && (
                <div>
                  <h4 className="font-bold text-slate-800 mb-1">{t(language, 'ind_lbl_what_next')}</h4>
                  <ul className="list-disc pl-5 space-y-1">
                    {labResult.next_actions.map((act, idx) => <li key={idx}>{act}</li>)}
                  </ul>
                </div>
              )}
              <div className="mt-4 pt-4 border-t border-slate-200">
                <EvidencePanel sources={labResult.sources} />
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-slate-800 mb-2">{t(language, 'ind_isi_title')}</h2>
          <p className="text-slate-600 text-[14px] mb-5">
            {t(language, 'ind_isi_desc')}
          </p>
          <button
            onClick={() => navigate('/assistant', { state: { prefill: 'How to apply for ISI Mark certification' } })}
            className="bg-navy-600 hover:bg-navy-700 text-white font-medium text-sm px-4 py-2 rounded-lg transition-colors w-full"
          >
            {t(language, 'ind_isi_btn')}
          </button>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-slate-800 mb-2">{t(language, 'ind_crs_title')}</h2>
          <p className="text-slate-600 text-[14px] mb-5">
            {t(language, 'ind_crs_desc')}
          </p>
          <button
            onClick={() => navigate('/assistant', { state: { prefill: 'What is the Compulsory Registration Scheme (CRS)?' } })}
            className="bg-navy-600 hover:bg-navy-700 text-white font-medium text-sm px-4 py-2 rounded-lg transition-colors w-full"
          >
            {t(language, 'ind_crs_btn')}
          </button>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
          <h2 className="text-lg font-bold text-slate-800 mb-2">{t(language, 'ind_fmcs_title')}</h2>
          <p className="text-slate-600 text-[14px] mb-5">
            {t(language, 'ind_fmcs_desc')}
          </p>
          <button
            onClick={() => navigate('/assistant', { state: { prefill: 'Foreign Manufacturers Certification Scheme (FMCS) details' } })}
            className="bg-navy-600 hover:bg-navy-700 text-white font-medium text-sm px-4 py-2 rounded-lg transition-colors w-full"
          >
            {t(language, 'ind_fmcs_btn')}
          </button>
        </div>
      </div>
    </div>
  )
}
