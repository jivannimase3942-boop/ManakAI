import { LANGUAGES, t } from '../i18n.js'

export default function TopBar({ language, setLanguage, textSize, setTextSize }) {
  return (
    <div className="bg-navy-900 text-white text-[13px] font-medium py-1.5 px-4 sm:px-6 lg:px-8 flex justify-between items-center z-50 relative">
      <div className="flex gap-4 items-center">
        <a href="#main-content" className="sr-only focus:not-sr-only focus:absolute focus:bg-white focus:text-navy-900 focus:px-3 focus:py-1 focus:rounded-sm focus:z-50">
          {t(language, 'skip_main')}
        </a>
        <div className="hidden sm:flex items-center gap-3 border-r border-navy-700 pr-4">
          <span className="text-navy-300">{t(language, 'accessibility')}:</span>
          <div className="flex gap-1">
            <button
              onClick={() => setTextSize('small')}
              className={`w-6 h-6 flex items-center justify-center rounded-sm transition-colors ${textSize === 'small' ? 'bg-navy-700' : 'hover:bg-navy-800'}`}
              aria-label="Decrease text size"
            >
              A-
            </button>
            <button
              onClick={() => setTextSize('normal')}
              className={`w-6 h-6 flex items-center justify-center rounded-sm transition-colors ${textSize === 'normal' ? 'bg-navy-700' : 'hover:bg-navy-800'}`}
              aria-label="Normal text size"
            >
              A
            </button>
            <button
              onClick={() => setTextSize('large')}
              className={`w-6 h-6 flex items-center justify-center rounded-sm transition-colors ${textSize === 'large' ? 'bg-navy-700' : 'hover:bg-navy-800'}`}
              aria-label="Increase text size"
            >
              A+
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
