import { NavLink } from 'react-router-dom'
import { t } from '../i18n.js'

export default function Footer({ language }) {
  return (
    <footer className="bg-[#0B1E40] border-t border-slate-900 text-slate-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">

          <div className="md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <span className="font-extrabold text-white text-[18px] tracking-wide">ManakAI</span>
            </div>
            <p className="text-[12px] text-slate-400 leading-relaxed max-w-xs">
              {t(language, 'ft_desc')}
            </p>
          </div>

          <div>
            <h3 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-4">{t(language, 'ft_product')}</h3>
            <ul className="space-y-3 text-[13px] font-medium text-slate-300">
              <li><NavLink to="/finder" className="hover:text-white transition-colors">{t(language, 'nav_finder')}</NavLink></li>
              <li><NavLink to="/services" className="hover:text-white transition-colors">{t(language, 'nav_services')}</NavLink></li>
              <li><NavLink to="/learning" className="hover:text-white transition-colors">{t(language, 'nav_learning')}</NavLink></li>
            </ul>
          </div>

          <div>
            <h3 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-4">{t(language, 'ft_guidance')}</h3>
            <ul className="space-y-3 text-[13px] font-medium text-slate-300">
              <li><NavLink to="/consumer" className="hover:text-white transition-colors">{t(language, 'srv_card5_t')}</NavLink></li>
              <li><NavLink to="/industry" className="hover:text-white transition-colors">{t(language, 'srv_card6_t')}</NavLink></li>
              <li><NavLink to="/assistant" state={{ prefill: 'I need testing guidance' }} className="hover:text-white transition-colors">{t(language, 'srv_card3_t')}</NavLink></li>
            </ul>
          </div>

          <div>
            <h3 className="text-[11px] font-bold uppercase tracking-wider text-slate-500 mb-4">{t(language, 'ft_info')}</h3>
            <ul className="space-y-3 text-[13px] font-medium text-slate-300">
              <li><NavLink to="/about" className="hover:text-white transition-colors">{t(language, 'abt_title')}</NavLink></li>
              <li><NavLink to="/dashboard" className="hover:text-white transition-colors">{t(language, 'nav_dashboard')}</NavLink></li>
              <li><a href="#" className="hover:text-white transition-colors">{t(language, 'ft_accessibility')}</a></li>
            </ul>
          </div>

        </div>

        <div className="pt-8 border-t border-slate-800/50">
          <div className="bg-[#08152e] p-5 rounded-sm border border-slate-800">
            <h4 className="text-[10px] font-bold text-slate-500 uppercase tracking-wider mb-2">{t(language, 'ft_disclaimer_title')}</h4>
            <p className="text-[11px] text-slate-400 leading-relaxed">
              {t(language, 'ft_disc')}
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
