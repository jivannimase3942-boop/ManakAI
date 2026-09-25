import { useState, useEffect } from 'react'
import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Footer from './components/Footer.jsx'
import Home from './pages/Home.jsx'
import Scanner from './pages/Scanner.jsx'
import Assistant from './pages/Assistant.jsx'
import StandardFinder from './pages/StandardFinder.jsx'
import Services from './pages/Services.jsx'
import About from './pages/About.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Learning from './pages/Learning.jsx'
import Consumer from './pages/Consumer.jsx'
import Industry from './pages/Industry.jsx'

export default function App() {
  const [language, setLanguage] = useState(() => localStorage.getItem('manakai_lang') || 'en')
  const [textSize, setTextSize] = useState('large')

  useEffect(() => {
    localStorage.setItem('manakai_lang', language)
    document.documentElement.lang = language
  }, [language])

  return (
    <div className={`min-h-screen flex flex-col size-${textSize} ${language !== 'en' ? `lang-${language}` : ''}`}>
      <Navbar language={language} setLanguage={setLanguage} />
      <main id="main-content" className="flex-1 focus:outline-none">
        <Routes>
          <Route path="/" element={<Home language={language} />} />
          <Route path="/scan" element={<Scanner language={language} />} />
          <Route path="/assistant" element={<Assistant language={language} />} />
          <Route path="/finder" element={<StandardFinder language={language} />} />
          <Route path="/services" element={<Services language={language} />} />
          <Route path="/industry" element={<Industry language={language} />} />
          <Route path="/msme" element={<Industry language={language} audience="msme" />} />
          <Route path="/consumer" element={<Consumer language={language} />} />
          <Route path="/dashboard" element={<Dashboard language={language} />} />
          <Route path="/learning" element={<Learning language={language} />} />
          <Route path="/about" element={<About language={language} />} />
        </Routes>
      </main>
      <Footer language={language} />
    </div>
  )
}
