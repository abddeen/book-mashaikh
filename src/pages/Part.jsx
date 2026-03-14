import { useState, useEffect } from 'react'
import { useParams, useLocation, Link } from 'react-router-dom'
import parts from '../data/parts.json'
import Chapter from '../components/Chapter'
import { Prose } from '../lib/markdown'

const partModules = {
  1: () => import('../data/part1.json'),
  2: () => import('../data/part2.json'),
  3: () => import('../data/part3.json'),
  4: () => import('../data/part4.json'),
  5: () => import('../data/part5.json'),
  6: () => import('../data/part6.json'),
  7: () => import('../data/part7.json'),
}

export default function Part() {
  const { id } = useParams()
  const { hash } = useLocation()
  const partNum = parseInt(id)
  const part = parts.find(p => p.number === partNum)
  const [chapters, setChapters] = useState(null)

  useEffect(() => {
    setChapters(null)
    const loader = partModules[partNum]
    if (loader) {
      loader().then(mod => setChapters(mod.default))
    }
  }, [partNum])

  // Scroll to hash after chapters finish loading
  useEffect(() => {
    if (chapters && hash) {
      const el = document.getElementById(hash.slice(1))
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    }
  }, [chapters, hash])

  if (!part) {
    return <p>Part not found.</p>
  }

  return (
    <>
      {/* Part Header */}
      <header className="mb-14 pb-8 border-b-2 border-accent">
        <span className="block text-[0.7rem] uppercase tracking-[0.16em] text-accent mb-3">
          Part {part.number}
        </span>
        <h1 className="text-[2.5rem] font-normal leading-[1.2] text-ink mb-1">
          {part.name}
        </h1>
        <p className="text-[1rem] text-muted italic">
          {part.period} &middot; {part.chapterRange}
        </p>
      </header>

      {/* Historical Context */}
      {part.historicalContext?.length > 0 && (
        <div className="mb-16">
          <h2 className="text-[1.05rem] font-normal italic text-muted mb-5 pb-1 border-b border-book-border">
            Historical Context
          </h2>
          {part.historicalContext.map((p, i) => (
            <Prose key={i} text={p} as="p" className="mb-4 last:mb-0" />
          ))}
        </div>
      )}

      {/* Chapters */}
      {!chapters ? (
        <p className="text-muted italic">Loading chapters...</p>
      ) : (
        chapters.map(ch => <Chapter key={ch.number} chapter={ch} />)
      )}

      {/* Afterword */}
      {part.afterword && chapters && (
        <div className="mt-16 pt-10 border-t-2 border-accent">
          <h2 className="text-[1.8rem] font-normal mb-6">{part.afterword.title}</h2>
          {part.afterword.paragraphs.map((p, i) => (
            <Prose key={i} text={p} as="p" className="mb-4 last:mb-0" />
          ))}
        </div>
      )}

      {/* Page Navigation */}
      <nav className="flex justify-between items-center mt-20 pt-7 border-t border-book-border text-[0.875rem]">
        <span>
          {partNum > 1 ? (
            <Link to={`/part/${partNum - 1}`} className="no-underline hover:underline">
              &larr; Part {partNum - 1}
            </Link>
          ) : (
            <Link to="/" className="no-underline hover:underline">
              &larr; Contents
            </Link>
          )}
        </span>
        <span>
          {partNum < 7 ? (
            <Link to={`/part/${partNum + 1}`} className="no-underline hover:underline">
              Part {partNum + 1} &rarr;
            </Link>
          ) : (
            <Link to="/relationships" className="no-underline hover:underline">
              Relationship Graphs &rarr;
            </Link>
          )}
        </span>
      </nav>
    </>
  )
}
