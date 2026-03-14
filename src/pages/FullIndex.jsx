import { Link } from 'react-router-dom'
import chaptersIndex from '../data/chapters-index.json'
import parts from '../data/parts.json'
import { renderInline } from '../lib/markdown'

export default function FullIndex() {
  const byPart = {}
  for (const fig of chaptersIndex) {
    ;(byPart[fig.part] ||= []).push(fig)
  }

  return (
    <div>
      <h1 className="text-[2.3rem] font-normal mb-8 pb-6 border-b-2 border-accent">
        Complete Index
      </h1>

      {parts.map(part => (
        <div key={part.number}>
          <h2 className="text-[1.2rem] font-normal text-ink mt-10 mb-3">
            Part {part.number}: {part.name}{' '}
            <span className="text-muted italic text-[0.9rem]">
              ({part.period})
            </span>
          </h2>

          <table className="w-full border-collapse text-[0.82rem]">
            <thead>
              <tr>
                {['#', 'Name', 'Born', 'Place', 'Tariqah'].map(h => (
                  <th
                    key={h}
                    className="text-left py-2.5 px-4 bg-parchment-alt border-b-2 border-book-border text-muted font-semibold text-[0.72rem] uppercase tracking-[0.09em]"
                  >
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {(byPart[part.number] || []).sort((a, b) => a.chapterNumber - b.chapterNumber).map(fig => (
                <tr key={fig.chapterNumber} className="hover:bg-parchment-alt group">
                  <td className="py-2 px-4 border-b border-book-border font-semibold whitespace-nowrap">
                    {fig.chapterNumber}
                  </td>
                  <td className="py-2 px-4 border-b border-book-border">
                    <Link
                      to={`/part/${fig.part}#ch-${fig.chapterNumber}`}
                      className="text-ink no-underline hover:text-accent font-medium"
                    >
                      {fig.name}
                    </Link>
                    {fig.arabicName && (
                      <span className="font-arabic text-[0.82rem] text-muted ml-2" dir="rtl">
                        ({fig.arabicName})
                      </span>
                    )}
                  </td>
                  <td className="py-2 px-4 border-b border-book-border text-muted align-top">
                    {fig.born}
                  </td>
                  <td className="py-2 px-4 border-b border-book-border text-muted align-top">
                    {fig.birthplace}
                  </td>
                  <td
                    className="py-2 px-4 border-b border-book-border text-muted align-top"
                    dangerouslySetInnerHTML={{ __html: renderInline(fig.tariqah) }}
                  />
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ))}
    </div>
  )
}
