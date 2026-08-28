import { NavLink } from 'react-router-dom'
import { t, LANGUAGES } from '../i18n.js'

const linkClass = ({ isActive }) =>
  `px-3 py-2 text-sm font-medium rounded-md transition-colors ${
    isActive ? 'text-navy-800 bg-navy-50' : 'text-navy-600 hover:text-navy-800 hover:bg-navy-50'
  }`

export default function Navbar({ language, setLanguage }) {
  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur border-b border-navy-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <NavLink to="/" className="flex items-center gap-2.5 shrink-0">
            <svg width="30" height="30" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="30" height="30" rx="6" fill="#152F5A" />
              <path d="M8 21V9L15 15L22 9V21" stroke="#F7F8FA" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <circle cx="22" cy="9" r="2.2" fill="#E08A2C" />
            </svg>
            <span className="font-bold text-lg text-navy-900 tracking-tight">ManakAI</span>
          </NavLink>

          <nav className="hidden md:flex items-center gap-1">
            <NavLink to="/" className={linkClass} end>{t(language, 'nav_home')}</NavLink>
            <NavLink to="/assistant" className={linkClass}>{t(language, 'nav_assistant')}</NavLink>
            <NavLink to="/finder" className={linkClass}>{t(language, 'nav_finder')}</NavLink>
            <NavLink to="/services" className={linkClass}>{t(language, 'nav_services')}</NavLink>
            <NavLink to="/about" className={linkClass}>{t(language, 'nav_about')}</NavLink>
          </nav>

          <div className="flex items-center gap-2">
            <label className="sr-only" htmlFor="lang-select">Language</label>
            <select
              id="lang-select"
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="text-sm border border-navy-200 rounded-md pl-2.5 pr-7 py-1.5 bg-white text-navy-700 font-medium focus:outline-none focus:ring-2 focus:ring-navy-500"
            >
              {LANGUAGES.map((l) => (
                <option key={l.code} value={l.code}>{l.label}</option>
              ))}
            </select>
          </div>
        </div>

        <nav className="md:hidden flex items-center gap-1 pb-2 overflow-x-auto">
          <NavLink to="/" className={linkClass} end>{t(language, 'nav_home')}</NavLink>
          <NavLink to="/assistant" className={linkClass}>{t(language, 'nav_assistant')}</NavLink>
          <NavLink to="/finder" className={linkClass}>{t(language, 'nav_finder')}</NavLink>
          <NavLink to="/services" className={linkClass}>{t(language, 'nav_services')}</NavLink>
          <NavLink to="/about" className={linkClass}>{t(language, 'nav_about')}</NavLink>
        </nav>
      </div>
    </header>
  )
}
