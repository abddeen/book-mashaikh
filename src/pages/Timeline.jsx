import { Link } from 'react-router-dom'
import chaptersIndex from '../data/chapters-index.json'
import parts from '../data/parts.json'
import { orderColor, LEGEND_ENTRIES } from '../lib/orders'

export default function Timeline() {
  const byPart = {}
  for (const fig of chaptersIndex) {
    ;(byPart[fig.part] ||= []).push(fig)
  }

  return (
    <div>
      <h1 className="text-[2.3rem] font-normal mb-3">Timeline of the Mashaikh</h1>
      <p className="text-muted italic mb-8 pb-7 border-b border-book-border text-[0.95rem]">
        126 luminaries arranged chronologically across 14 centuries. Each name links to its chapter.
      </p>

      {/* Legend */}
      <div className="flex flex-wrap gap-x-3 gap-y-1.5 mb-10 p-3 px-5 bg-parchment-alt border border-book-border text-[0.78rem]">
        {LEGEND_ENTRIES.map(({ label, color }) => (
          <span key={label} className="flex items-center gap-1.5 text-muted">
            <span
              className="w-[9px] h-[9px] rounded-full shrink-0"
              style={{ background: color }}
            />
            {label}
          </span>
        ))}
      </div>

      {/* Timeline */}
      <div className="relative pl-[115px] max-sm:pl-[75px]">
        {/* Spine */}
        <div className="absolute left-[107px] max-sm:left-[67px] top-0 bottom-0 w-0.5 bg-gradient-to-b from-accent via-book-border to-gold/40" />

        {parts.map(part => (
          <div key={part.number}>
            {/* Era banner */}
            <div className="relative ml-[-115px] max-sm:ml-[-75px] mt-11 mb-2">
              <div className="inline-flex items-baseline gap-2.5 bg-parchment-alt border border-book-border border-l-[3px] border-l-accent py-1.5 px-3 relative z-[1]">
                <span className="text-[0.65rem] uppercase tracking-[0.14em] text-accent font-semibold">
                  Part {part.number}
                </span>
                <span className="text-[0.95rem] text-ink italic">{part.name}</span>
                <span className="text-[0.73rem] text-muted">{part.dates}</span>
              </div>
            </div>

            {/* Entries */}
            {(byPart[part.number] || []).sort((a, b) => a.chapterNumber - b.chapterNumber).map(fig => {
              const color = orderColor(fig.tariqah)
              const approx = fig.born.includes('c.') ? 'c.\u202f' : ''
              const yearDisp = fig.ceYear
                ? `${approx}${fig.ceYear} CE`
                : '?'

              // Clean tariqah display
              let tariqahDisp = fig.tariqah
                .replace(/\s*\([^)]*\)/g, '')
                .trim()
              if (tariqahDisp.length > 48) tariqahDisp = tariqahDisp.slice(0, 45) + '\u2026'

              return (
                <div
                  key={fig.chapterNumber}
                  className="grid grid-cols-[103px_14px_1fr] max-sm:grid-cols-[63px_12px_1fr] gap-x-2.5 items-start py-0.5"
                >
                  <span className="text-right text-[0.7rem] max-sm:text-[0.62rem] text-muted pt-[5px] tabular-nums">
                    {yearDisp}
                  </span>
                  <span
                    className="w-2.5 h-2.5 rounded-full relative top-[5px] z-[2] border-2 border-parchment"
                    style={{ background: color }}
                  />
                  <div className="py-0.5 pb-[7px] pl-2.5 border-l-2 border-book-border flex flex-wrap items-baseline gap-x-2 gap-y-0.5">
                    <Link
                      to={`/part/${fig.part}#ch-${fig.chapterNumber}`}
                      className="text-[0.92rem] text-ink no-underline font-medium hover:text-accent hover:underline"
                    >
                      {fig.name}
                    </Link>
                    <span className="font-arabic text-[0.82rem] text-muted max-sm:hidden" dir="rtl">
                      {fig.arabicName}
                    </span>
                    <span className="text-[0.72rem] text-muted italic whitespace-nowrap max-sm:hidden before:content-['\u00b7\u0020']">
                      {fig.birthplace}
                    </span>
                    <span
                      className="text-[0.65rem] py-px px-[7px] rounded-[10px] border whitespace-nowrap mt-0.5"
                      style={{ borderColor: color, color }}
                    >
                      {tariqahDisp}
                    </span>
                  </div>
                </div>
              )
            })}
          </div>
        ))}
      </div>
    </div>
  )
}
