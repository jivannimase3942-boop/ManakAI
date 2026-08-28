import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import ServiceCard from '../components/ServiceCard.jsx'
import { t } from '../i18n.js'
import { api } from '../api.js'

export default function Services({ language }) {
  const navigate = useNavigate()
  const [services, setServices] = useState([])

  useEffect(() => {
    api.services().then(setServices).catch(() => {})
  }, [])

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <h1 className="text-2xl font-bold text-navy-900">{t(language, 'services_page_title')}</h1>
      <p className="text-navy-600 text-sm mt-1.5">{t(language, 'services_page_sub')}</p>

      <div className="mt-8 grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {services.map((s) => (
          <ServiceCard
            key={s.id}
            name={s.name}
            description={s.description}
            icon={s.icon}
            onClick={() => navigate('/assistant', { state: { prefill: s.name } })}
          />
        ))}
      </div>
    </div>
  )
}
