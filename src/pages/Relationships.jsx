import { useEffect, useRef } from 'react'
import relationships from '../data/relationships.json'
import { renderInline } from '../lib/markdown'

export default function Relationships() {
  const containerRef = useRef(null)

  useEffect(() => {
    import('mermaid').then(({ default: mermaid }) => {
      mermaid.initialize({
        startOnLoad: false,
        theme: 'base',
        themeVariables: {
          primaryColor: '#f1e8d3',
          primaryTextColor: '#1e1609',
          primaryBorderColor: '#c8a890',
          lineColor: '#9a7010',
          secondaryColor: '#f9f5eb',
          tertiaryColor: '#f1e8d3',
          clusterBkg: '#faf7f0',
          clusterBorder: '#d8c8a4',
          edgeLabelBackground: '#f9f5eb',
          titleColor: '#1e1609',
          fontFamily: 'EB Garamond, Georgia, serif',
          fontSize: '15px',
        },
      })
      if (containerRef.current) {
        mermaid.run({ nodes: containerRef.current.querySelectorAll('.mermaid') })
      }
    })
  }, [])

  return (
    <div ref={containerRef}>
      <h1 className="text-[2.3rem] font-normal mb-3">Relationship Graphs by Era</h1>

      {relationships.map((section, i) => (
        <div key={i}>
          <h2 className="text-[1.45rem] font-normal text-ink mt-14 mb-5 pb-2 border-b border-book-border">
            {section.title}
          </h2>

          {section.mermaidDiagrams.map((diagram, j) => (
            <div
              key={j}
              className="mermaid bg-parchment-alt border border-book-border rounded-sm p-6 overflow-x-auto my-3 text-[0.875rem]"
            >
              {diagram}
            </div>
          ))}

          {section.notes.map((note, j) => {
            // Table rows
            if (note.startsWith('|') && note.endsWith('|')) {
              const cells = note.slice(1, -1).split('|').map(c => c.trim())
              // Skip separator rows
              if (cells.every(c => /^[-:]+$/.test(c))) return null
              const isHeader = j === 0 || (section.notes[j - 1] && !section.notes[j - 1].startsWith('|'))
              return (
                <div key={j} className="text-[0.88rem] text-muted">
                  <div className="flex gap-4">
                    {cells.map((cell, k) => (
                      <span
                        key={k}
                        className={isHeader ? 'font-semibold text-ink' : ''}
                        dangerouslySetInnerHTML={{ __html: renderInline(cell) }}
                      />
                    ))}
                  </div>
                </div>
              )
            }
            return (
              <p
                key={j}
                className="text-[0.88rem] text-muted mt-2 leading-[1.65]"
                dangerouslySetInnerHTML={{ __html: renderInline(note) }}
              />
            )
          })}
        </div>
      ))}
    </div>
  )
}
