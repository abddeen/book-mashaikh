import { Link } from 'react-router-dom'
import chaptersIndex from '../data/chapters-index.json'
import { orderFamily, CANONICAL_ORDERS } from '../lib/orders'
import { renderInline } from '../lib/markdown'

export default function ByOrder() {
  // Group figures by canonical order family
  const orderIndex = {}
  CANONICAL_ORDERS.forEach((o, i) => { orderIndex[o.name] = i })
  orderIndex['Independent / Other'] = CANONICAL_ORDERS.length

  const groups = {}
  for (const fig of chaptersIndex) {
    const { name } = orderFamily(fig.tariqah)
    ;(groups[name] ||= []).push(fig)
  }

  const sortedGroups = Object.entries(groups).sort(
    ([a], [b]) => (orderIndex[a] ?? 999) - (orderIndex[b] ?? 999)
  )

  return (
    <div>
      <h1 className="text-[2.3rem] font-normal mb-3">By Sufi Order</h1>
      <p className="text-muted italic mb-10 pb-7 border-b border-book-border text-[0.95rem]">
        126 luminaries of Tasawwuf grouped by their primary spiritual affiliation,
        ordered from earliest to most recent order. Each name links to its chapter.
      </p>

      {sortedGroups.map(([famName, figs]) => {
        const { color } = orderFamily(figs[0].tariqah)
        const slug = famName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

        return (
          <div key={famName} id={`order-${slug}`} className="mb-14">
            <div
              className="flex items-baseline gap-3 mb-4 py-2 px-3.5 bg-parchment-alt border-l-4 border-b border-book-border"
              style={{ borderLeftColor: color }}
            >
              <span className="text-[1.2rem] font-normal text-ink">{famName}</span>
              <span className="text-[0.78rem] text-muted italic">
                {figs.length}&thinsp;figure{figs.length !== 1 ? 's' : ''}
              </span>
            </div>

            <div className="grid grid-cols-[repeat(auto-fill,minmax(200px,1fr))] gap-2">
              {figs.map(fig => {
                let bornDisp = fig.born
                if (bornDisp.length > 42) bornDisp = bornDisp.slice(0, 39) + '\u2026'

                return (
                  <div
                    key={fig.chapterNumber}
                    className="p-2.5 px-3.5 border border-book-border bg-parchment flex flex-col gap-0.5 transition-colors hover:bg-parchment-alt hover:border-[#c8a080]"
                  >
                    <span className="text-[0.62rem] uppercase tracking-[0.1em] text-accent">
                      Ch.&thinsp;{fig.chapterNumber}
                    </span>
                    <Link
                      to={`/part/${fig.part}#ch-${fig.chapterNumber}`}
                      className="text-[0.92rem] font-medium text-ink no-underline leading-[1.3] hover:text-accent"
                    >
                      {fig.name}
                    </Link>
                    <span className="font-arabic text-[0.82rem] text-muted" dir="rtl" style={{ textAlign: 'left' }}>
                      {fig.arabicName}
                    </span>
                    <span className="text-[0.72rem] text-muted italic">{bornDisp}</span>
                  </div>
                )
              })}
            </div>
          </div>
        )
      })}
    </div>
  )
}
