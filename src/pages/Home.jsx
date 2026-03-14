import { Link } from 'react-router-dom'
import parts from '../data/parts.json'

export default function Home() {
  return (
    <>
      {/* Cover */}
      <div className="text-center py-16 pb-14 border-b border-book-border mb-16">
        <span className="block font-arabic text-[2.2rem] text-muted mb-8" dir="rtl">
          {'\u0628\u0650\u0633\u0652\u0645\u0650 \u0627\u0644\u0644\u0651\u064e\u0647\u0650 \u0627\u0644\u0631\u0651\u064e\u062d\u0652\u0645\u064e\u0670\u0646\u0650 \u0627\u0644\u0631\u0651\u064e\u062d\u0650\u064a\u0645\u0650'}
        </span>
        <h1 className="text-[3.1rem] font-normal leading-[1.15] text-ink">
          The Book of the Mashaikh
        </h1>
        <span className="block font-arabic text-[1.9rem] text-muted mt-1" dir="rtl">
          {'\u0643\u0650\u062a\u064e\u0627\u0628\u064f \u0627\u0644\u0652\u0645\u064e\u0634\u064e\u0627\u064a\u0650\u062e'}
        </span>
        <span className="block text-gold text-[1.4rem] my-6 tracking-[0.4em]">
          &#10086; &#10086; &#10086;
        </span>
        <p className="text-[1.05rem] text-muted italic max-w-[480px] mx-auto">
          A comprehensive guide to one hundred luminaries of Tasawwuf, arranged by era
        </p>
      </div>

      {/* Table of Contents */}
      <div>
        <h2 className="text-[0.75rem] uppercase tracking-[0.15em] text-muted font-normal mb-6">
          Contents
        </h2>
        <div className="grid grid-cols-[repeat(auto-fill,minmax(295px,1fr))] gap-4 mb-5">
          {parts.map(part => (
            <Link
              key={part.number}
              to={`/part/${part.number}`}
              className="block p-5 px-6 border border-book-border no-underline text-inherit bg-parchment relative transition-all hover:bg-parchment-alt hover:border-[#c8a080] hover:shadow-[0_2px_10px_rgba(0,0,0,0.07)] group"
            >
              <span className="absolute left-0 top-0 bottom-0 w-[3px] bg-accent opacity-0 group-hover:opacity-100 transition-opacity" />
              <span className="block text-[0.68rem] uppercase tracking-[0.14em] text-accent mb-1">
                Part {part.number}
              </span>
              <span className="block text-[1.1rem] text-ink leading-[1.3]">
                {part.name}
              </span>
              <span className="block text-[0.8rem] text-muted italic mt-0.5">
                {part.period} &middot; {part.chapterRange}
              </span>
            </Link>
          ))}
        </div>

        <div className="grid grid-cols-[repeat(auto-fill,minmax(200px,1fr))] gap-3">
          {[
            ['/relationships', 'Relationship Graphs by Era'],
            ['/timeline', 'Timeline of All 126 Figures'],
            ['/by-order', 'Figures by Sufi Order'],
            ['/full-index', 'Complete Index'],
          ].map(([to, label]) => (
            <Link
              key={to}
              to={to}
              className="block py-3 px-6 border border-book-border no-underline text-muted italic text-[0.93rem] text-center transition-colors hover:border-gold hover:text-gold"
            >
              {label}
            </Link>
          ))}
        </div>
      </div>
    </>
  )
}
