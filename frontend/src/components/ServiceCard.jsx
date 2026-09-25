const ICONS = {
  book: (
    <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 19.5A2.5 2.5 0 0 0 6.5 22H20V2H6.5A2.5 2.5 0 0 0 4 4.5v15Z" />
  ),
  'badge-check': (
    <>
      <path d="m9 12 2 2 4-4" />
      <path d="M12 2 4 5v6c0 5.2 3.4 9.7 8 11 4.6-1.3 8-5.8 8-11V5l-8-3Z" />
    </>
  ),
  layers: (
    <>
      <path d="m12.83 2.18 8.49 4.24a1 1 0 0 1 0 1.79l-8.49 4.24a2 2 0 0 1-1.79 0L2.55 8.21a1 1 0 0 1 0-1.79l8.49-4.24a2 2 0 0 1 1.79 0Z" />
      <path d="m2.55 12.21 8.49 4.24a2 2 0 0 0 1.79 0l8.49-4.24" />
      <path d="m2.55 16.21 8.49 4.24a2 2 0 0 0 1.79 0l8.49-4.24" />
    </>
  ),
  flask: (
    <path d="M9 2v6.5L4.5 18a2 2 0 0 0 1.8 3h11.4a2 2 0 0 0 1.8-3L15 8.5V2M9 2h6M8 16h8" />
  ),
  gem: (
    <path d="m6 3 12 0 4 6-10 12L2 9Z M2 9h20 M9 3l-3 6 6 12 6-12-3-6" />
  ),
  users: (
    <>
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
    </>
  ),
}

export default function ServiceCard({ name, description, action, icon, onClick }) {
  return (
    <button
      onClick={onClick}
      className="text-left w-full h-full min-h-[250px] bg-white border border-navy-100 rounded-xl p-5 shadow-card hover:shadow-cardHover hover:border-navy-200 transition-all focus-visible:outline-2 focus-visible:outline-navy-500 flex flex-col"
    >
      <div className="w-10 h-10 rounded-lg bg-navy-50 flex items-center justify-center mb-3.5">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#1c3f74" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          {ICONS[icon] || ICONS.book}
        </svg>
      </div>
      <h3 className="font-semibold text-navy-900 text-[15px] mb-1">{name}</h3>
      <p className="text-sm text-navy-600 leading-relaxed flex-1">{description}</p>
      {action && <span className="mt-6 text-xs font-bold uppercase tracking-wider text-[#1C4E80]">{action} <span aria-hidden="true">→</span></span>}
    </button>
  )
}
