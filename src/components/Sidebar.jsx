import { Link, NavLink, useParams } from 'react-router-dom'
import parts from '../data/parts.json'

const refLinks = [
  { to: '/relationships', label: 'Relationship Graphs' },
  { to: '/timeline', label: 'Timeline' },
  { to: '/by-order', label: 'By Sufi Order' },
  { to: '/full-index', label: 'Full Index' },
]

function navClass({ isActive }) {
  return `block py-1 px-6 pl-7 text-[0.9rem] leading-[1.45] border-l-[3px] transition-colors no-underline ${
    isActive
      ? 'text-sidebar-text border-l-sidebar-accent bg-[rgba(200,152,14,0.08)]'
      : 'border-transparent text-sidebar-link hover:text-sidebar-text hover:border-l-sidebar-accent hover:bg-[rgba(200,152,14,0.08)]'
  }`
}

export default function Sidebar() {
  const params = useParams()
  const currentPartId = params.id ? parseInt(params.id) : null

  return (
    <div className="pb-12">
      <div className="px-6 pt-7 pb-5 border-b border-sidebar-accent/[0.18]">
        <Link
          to="/"
          className="block text-sidebar-accent no-underline text-[0.7rem] uppercase tracking-[0.15em] mb-2 hover:text-sidebar-text"
        >
          &larr; Home
        </Link>
        <span className="block text-sidebar-text text-[0.95rem] leading-[1.45]">
          The Book of<br />the Mashaikh
        </span>
      </div>

      <nav className="py-3">
        <span className="block text-[0.68rem] uppercase tracking-[0.18em] text-sidebar-accent/60 px-6 pt-4 pb-1">
          Parts
        </span>

        {parts.map(part => (
          <div key={part.number}>
            <NavLink to={`/part/${part.number}`} className={navClass}>
              Part {part.number}: {part.name}
            </NavLink>
            {currentPartId === part.number &&
              part.chapters.map(ch => (
                <a
                  key={ch.number}
                  href={`#ch-${ch.number}`}
                  className="block py-0.5 px-6 pl-10 text-[0.82rem] text-[#8a6840] hover:text-sidebar-text transition-colors no-underline"
                >
                  Ch.{ch.number} &middot;{' '}
                  {ch.name.length > 28 ? ch.name.slice(0, 26) + '\u2026' : ch.name}
                </a>
              ))}
          </div>
        ))}

        <span className="block text-[0.68rem] uppercase tracking-[0.18em] text-sidebar-accent/60 px-6 pt-4 pb-1">
          Reference
        </span>

        {refLinks.map(({ to, label }) => (
          <NavLink key={to} to={to} className={navClass}>
            {label}
          </NavLink>
        ))}
      </nav>
    </div>
  )
}
