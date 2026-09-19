import { useState } from 'react'
import { NavLink } from 'react-router-dom'
import { t, LANGUAGES } from '../i18n.js'

const linkClass = ({ isActive }) =>
  `px-2 h-full flex items-center justify-center text-[13px] font-bold uppercase tracking-wider transition-colors border-b-2 ${
    isActive
      ? 'text-[#0B1E40] bg-[#E8EDF2] border-[#0B1E40]'
      : 'text-slate-600 border-transparent hover:text-[#0B1E40] hover:bg-[#EEF2F6] hover:border-slate-300'
  }`

export default function Navbar({ language, setLanguage }) {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const closeMenu = () => setIsMobileMenuOpen(false)

  return (
    <header className="sticky top-0 z-40 bg-[#F5F7FA] border-b border-slate-200 shadow-sm">
      <div className="w-full">
        {/* MOBILE LAYOUT */}
        <div className="flex lg:hidden items-center justify-between h-[68px] px-4">
          <div className="flex items-center shrink-0">
            <NavLink to="/" onClick={closeMenu} className="flex items-center gap-2.5">
            <svg width="28" height="28" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg" className="shrink-0">
              <rect width="30" height="30" rx="4" fill="#0B1E40" />
              <path d="M8 21V9L15 15L22 9V21" stroke="#F7F8FA" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <circle cx="22" cy="9" r="2.2" fill="#E08A2C" />
            </svg>
            <span className="font-extrabold text-[19px] sm:text-[20px] text-[#0B1E40] tracking-tight truncate shrink-0">ManakAI</span>
            </NavLink>
          </div>
          <div className="flex items-center">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="p-2 -mr-2 text-[#0B1E40] hover:bg-slate-100 rounded-sm focus:outline-none"
              aria-label="Toggle menu"
            >
              <svg className="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                {isMobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>

        {/* DESKTOP LAYOUT */}
        <div className="hidden lg:grid grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)] items-center h-[68px] px-6">

          {/* LEFT ZONE: BRAND */}
          <div className="flex justify-center items-center h-full">
            <div className="w-[192px] flex items-center justify-start">
              <NavLink to="/" onClick={closeMenu} className="flex items-center gap-2.5 shrink-0">
                <svg width="28" height="28" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg" className="shrink-0">
                  <rect width="30" height="30" rx="4" fill="#0B1E40" />
                  <path d="M8 21V9L15 15L22 9V21" stroke="#F7F8FA" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                  <circle cx="22" cy="9" r="2.2" fill="#E08A2C" />
                </svg>
                <span className="font-extrabold text-[19px] sm:text-[20px] text-[#0B1E40] tracking-tight truncate shrink-0">ManakAI</span>
              </NavLink>
            </div>
          </div>

          {/* CENTER ZONE: DESKTOP NAV */}
          <div className="flex justify-center h-full">
            <nav className="flex items-center justify-center h-full gap-3">
              <NavLink to="/" className={linkClass} end>{t(language, 'nav_home')}</NavLink>
              <NavLink to="/finder" className={linkClass}>{t(language, 'nav_finder')}</NavLink>
              <NavLink to="/services" className={linkClass}>{t(language, 'nav_services')}</NavLink>
              <NavLink to="/learning" className={linkClass}>{t(language, 'nav_learning')}</NavLink>
              <NavLink to="/about" className={linkClass}>{t(language, 'nav_about')}</NavLink>
            </nav>
          </div>

          {/* RIGHT ZONE: UTILITIES */}
          <div className="flex justify-center items-center h-full">
            <div className="w-[192px] flex items-center justify-end gap-3">
              {setLanguage && (
                <div className="flex items-center bg-white px-2 border border-slate-200 rounded-sm shadow-sm h-[38px]">
                  <label htmlFor="nav-lang-select" className="sr-only">Language</label>
                  <select
                    id="nav-lang-select"
                    value={language}
                    onChange={(e) => setLanguage(e.target.value)}
                    className="bg-transparent border-none text-[#1C4E80] text-[13px] font-bold py-0 h-full focus:outline-none focus:ring-0 cursor-pointer"
                  >
                    {LANGUAGES.map((l) => (
                      <option key={l.code} value={l.code}>{l.label}</option>
                    ))}
                  </select>
                </div>
              )}
              <NavLink to="/dashboard" className="h-[38px] flex items-center text-[13px] font-bold text-white bg-[#1C4E80] hover:bg-[#0B1E40] transition-colors px-4 rounded-sm shadow-sm whitespace-nowrap">
                {t(language, 'nav_dashboard')}
              </NavLink>
            </div>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        {isMobileMenuOpen && (
          <div className="lg:hidden border-t border-slate-200 bg-white absolute left-0 right-0 top-[68px] shadow-lg flex flex-col max-h-[calc(100vh-68px)] overflow-y-auto">
            <nav className="flex flex-col p-4 gap-2">
              <NavLink to="/" onClick={closeMenu} className={({ isActive }) => `px-4 py-3 text-[14px] font-bold uppercase tracking-wider rounded-sm ${isActive ? 'text-[#0B1E40] bg-[#E8EDF2]' : 'text-slate-600 hover:bg-slate-50'}`} end>{t(language, 'nav_home')}</NavLink>
              <NavLink to="/finder" onClick={closeMenu} className={({ isActive }) => `px-4 py-3 text-[14px] font-bold uppercase tracking-wider rounded-sm ${isActive ? 'text-[#0B1E40] bg-[#E8EDF2]' : 'text-slate-600 hover:bg-slate-50'}`}>{t(language, 'nav_finder')}</NavLink>
              <NavLink to="/services" onClick={closeMenu} className={({ isActive }) => `px-4 py-3 text-[14px] font-bold uppercase tracking-wider rounded-sm ${isActive ? 'text-[#0B1E40] bg-[#E8EDF2]' : 'text-slate-600 hover:bg-slate-50'}`}>{t(language, 'nav_services')}</NavLink>
              <NavLink to="/learning" onClick={closeMenu} className={({ isActive }) => `px-4 py-3 text-[14px] font-bold uppercase tracking-wider rounded-sm ${isActive ? 'text-[#0B1E40] bg-[#E8EDF2]' : 'text-slate-600 hover:bg-slate-50'}`}>{t(language, 'nav_learning')}</NavLink>
              <NavLink to="/about" onClick={closeMenu} className={({ isActive }) => `px-4 py-3 text-[14px] font-bold uppercase tracking-wider rounded-sm ${isActive ? 'text-[#0B1E40] bg-[#E8EDF2]' : 'text-slate-600 hover:bg-slate-50'}`}>{t(language, 'nav_about')}</NavLink>

              <div className="my-2 border-t border-slate-100"></div>

              <div className="flex flex-col gap-3 px-2">
                {setLanguage && (
                  <div className="flex items-center bg-slate-50 px-3 py-1 border border-slate-200 rounded-sm">
                    <label htmlFor="nav-lang-select-mobile" className="sr-only">Language</label>
                    <select
                      id="nav-lang-select-mobile"
                      value={language}
                      onChange={(e) => { setLanguage(e.target.value); closeMenu(); }}
                      className="bg-transparent border-none text-[#1C4E80] text-[14px] font-bold py-2 focus:outline-none focus:ring-0 cursor-pointer w-full"
                    >
                      {LANGUAGES.map((l) => (
                        <option key={l.code} value={l.code}>{l.label}</option>
                      ))}
                    </select>
                  </div>
                )}
                <NavLink to="/dashboard" onClick={closeMenu} className="text-[14px] font-bold text-center text-white bg-[#1C4E80] hover:bg-[#0B1E40] transition-colors px-4 py-3 rounded-sm shadow-sm">
                  {t(language, 'nav_dashboard')}
                </NavLink>
              </div>
            </nav>
          </div>
        )}
      </div>
    </header>
  )
}
