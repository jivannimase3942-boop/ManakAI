import { t } from '../i18n.js'

export default function Footer({ language }) {
  return (
    <footer className="border-t border-navy-100 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex items-center gap-2">
          <svg width="20" height="20" viewBox="0 0 30 30" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="30" height="30" rx="6" fill="#152F5A" />
            <path d="M8 21V9L15 15L22 9V21" stroke="#F7F8FA" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            <circle cx="22" cy="9" r="2.2" fill="#E08A2C" />
          </svg>
          <span className="font-semibold text-navy-800 text-sm">ManakAI</span>
        </div>
        <p className="text-xs text-navy-500 text-center sm:text-right max-w-xl">
          {t(language, 'footer_note')}
        </p>
      </div>
    </footer>
  )
}
