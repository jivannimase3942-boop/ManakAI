import { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Footer from './components/Footer.jsx'
import Home from './pages/Home.jsx'
import Assistant from './pages/Assistant.jsx'
import StandardFinder from './pages/StandardFinder.jsx'
import Services from './pages/Services.jsx'
import About from './pages/About.jsx'

export default function App() {
  const [language, setLanguage] = useState(() => localStorage.getItem('manakai_lang') || 'en')

  useEffect(() => {
    localStorage.setItem('manakai_lang', language)
    document.documentElement.lang = language
  }, [language])

  return (
    <div className={`min-h-screen flex flex-col ${language !== 'en' ? `lang-${language}` : ''}`}>
      <Navbar language={language} setLanguage={setLanguage} />
      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Home language={language} />} />
          <Route path="/assistant" element={<Assistant language={language} />} />
          <Route path="/finder" element={<StandardFinder language={language} />} />
          <Route path="/services" element={<Services language={language} />} />
          <Route path="/about" element={<About language={language} />} />
        </Routes>
      </main>
      <Footer language={language} />
    </div>
  )
}
