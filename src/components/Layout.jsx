import { useState } from 'react'
import { Outlet, useLocation } from 'react-router-dom'
import { useEffect } from 'react'
import Sidebar from './Sidebar'

export default function Layout() {
  const [menuOpen, setMenuOpen] = useState(false)
  const location = useLocation()

  // Close menu on navigation
  useEffect(() => {
    setMenuOpen(false)
  }, [location.pathname])

  // Scroll to hash on navigation
  useEffect(() => {
    if (location.hash) {
      const el = document.getElementById(location.hash.slice(1))
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    } else {
      window.scrollTo(0, 0)
    }
  }, [location])

  return (
    <div className="lg:grid lg:grid-cols-[265px_1fr] min-h-screen">
      <button
        onClick={() => setMenuOpen(!menuOpen)}
        className="lg:hidden fixed top-4 left-4 z-50 bg-sidebar text-sidebar-text w-10 h-10 flex items-center justify-center rounded text-lg"
        aria-label="Toggle menu"
      >
        {menuOpen ? '\u2715' : '\u2630'}
      </button>

      <aside
        className={`
          fixed inset-y-0 left-0 z-40 w-[265px] bg-sidebar overflow-y-auto sidebar-scroll
          transform transition-transform duration-200
          ${menuOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 lg:sticky lg:top-0 lg:h-screen
        `}
      >
        <Sidebar />
      </aside>

      {menuOpen && (
        <div
          className="fixed inset-0 bg-black/40 z-30 lg:hidden"
          onClick={() => setMenuOpen(false)}
        />
      )}

      <main className="min-w-0 px-6 py-12 pt-16 lg:pt-[4.5rem] lg:px-[5.5rem] lg:py-[4.5rem] lg:pb-28 max-w-[820px]">
        <Outlet />
      </main>
    </div>
  )
}
