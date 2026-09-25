import { useNavigate, useSearchParams } from 'react-router-dom'
import { t } from '../i18n.js'
import ServiceCard from '../components/ServiceCard.jsx'

const services = [
  { id: 'standards', title: 'service_standards', description: 'service_standards_desc', action: 'service_standards_action', route: '/finder', icon: 'book' },
  { id: 'certification', title: 'service_certification', description: 'service_certification_desc', action: 'service_certification_action', route: '/industry', icon: 'badge-check' },
  { id: 'schemes', title: 'service_schemes', description: 'service_schemes_desc', action: 'service_schemes_action', route: '/industry', icon: 'layers' },
  { id: 'testing', title: 'service_testing', description: 'service_testing_desc', action: 'service_testing_action', route: '/industry', icon: 'flask' },
  { id: 'hallmarking', title: 'service_hallmarking', description: 'service_hallmarking_desc', action: 'service_hallmarking_action', route: '/consumer', icon: 'gem' },
  { id: 'consumer-services', title: 'service_consumer', description: 'service_consumer_desc', action: 'service_consumer_action', route: '/consumer', icon: 'users' },
]

export default function Services({ language }) {
  const navigate = useNavigate()
  const [params] = useSearchParams()
  const selected = services.find((service) => service.id === params.get('feature'))

  if (selected) {
    return (
      <div className="min-h-screen bg-[#F7F9FC]">
        <div className="mx-auto max-w-4xl px-5 py-12 sm:px-8 lg:py-16">
          <button onClick={() => navigate('/services')} className="text-sm font-bold text-[#1C4E80] hover:underline">← {t(language, 'service_back')}</button>
          <div className="mt-8 border border-slate-200 bg-white p-7 shadow-sm sm:p-10">
            <p className="text-xs font-bold uppercase tracking-[0.18em] text-[#1C4E80]">{t(language, 'service_label')}</p>
            <h1 className="mt-3 text-3xl font-extrabold text-[#0B1E40]">{t(language, selected.title)}</h1>
            <p className="mt-4 max-w-2xl text-base leading-7 text-slate-600">{t(language, selected.description)}</p>
            <div className="mt-8 border-l-4 border-[#E08A2C] bg-[#FFF9F1] p-5">
              <p className="text-sm leading-6 text-slate-700">{t(language, 'service_explicit_action')}</p>
              <button onClick={() => navigate(selected.route)} className="mt-5 min-h-11 bg-[#0B1E40] px-5 py-3 text-sm font-bold text-white hover:bg-[#152F5A]">{t(language, selected.action)} →</button>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#F7F9FC]">
      <div className="mx-auto max-w-[1360px] px-5 py-12 sm:px-8 lg:px-12 lg:py-16">
        <div className="max-w-3xl"><p className="text-xs font-bold uppercase tracking-[0.18em] text-[#1C4E80]">{t(language, 'nav_services')}</p><h1 className="mt-3 text-3xl font-extrabold tracking-tight text-[#0B1E40] sm:text-4xl">{t(language, 'service_choose')}</h1><p className="mt-4 text-base leading-7 text-slate-600">{t(language, 'service_intro')}</p></div>
        <div className="mt-9 grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
          {services.map((service) => <ServiceCard key={service.id} name={t(language, service.title)} description={t(language, service.description)} action={t(language, service.action)} icon={service.icon} onClick={() => navigate(`/services?feature=${service.id}`)} />)}
        </div>
      </div>
    </div>
  )
}
