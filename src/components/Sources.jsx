import { renderInline } from '../lib/markdown'

export default function Sources({ sources }) {
  if (!sources || sources.length === 0) return null

  return (
    <div className="mt-10">
      <h3 className="text-[1.08rem] font-normal italic text-accent mb-4 pb-1 border-b border-book-border">
        Sources &amp; References
      </h3>
      <ol className="list-none m-0 p-0 text-[0.875rem] leading-[1.7] border-t border-book-border pt-2">
        {sources.map((source, i) => (
          <li
            key={i}
            className="flex gap-2 py-1 border-b border-dotted border-book-border last:border-b-0 text-muted"
          >
            <span className="shrink-0 text-accent font-semibold text-[0.8rem] min-w-[2.2rem] pt-0.5 tabular-nums">
              [{i + 1}]
            </span>
            <span>
              {source.url ? (
                <a
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-ink no-underline border-b border-book-border hover:text-accent hover:border-accent font-medium"
                >
                  {source.label}
                </a>
              ) : (
                <span className="text-ink font-medium">{source.label}</span>
              )}
              {source.unverified && (
                <span className="text-[0.72rem] text-gold italic ml-1">
                  [unverified URL]
                </span>
              )}
              {source.description && (
                <span
                  dangerouslySetInnerHTML={{
                    __html: ' \u2014 ' + renderInline(source.description),
                  }}
                />
              )}
            </span>
          </li>
        ))}
      </ol>
    </div>
  )
}
