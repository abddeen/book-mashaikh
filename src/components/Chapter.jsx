import { Prose } from '../lib/markdown'
import Sources from './Sources'

function Section({ title, children }) {
  return (
    <div className="mt-10">
      <h3 className="text-[1.08rem] font-normal italic text-accent mb-4 pb-1 border-b border-book-border">
        {title}
      </h3>
      {children}
    </div>
  )
}

function Paragraphs({ items }) {
  return items.map((p, i) => (
    <Prose key={i} text={p} as="p" className="mb-4 last:mb-0" />
  ))
}

const META_DISPLAY = [
  ['fullName', 'Full Name'],
  ['born', 'Born'],
  ['died', 'Died'],
  ['sufiOrder', 'Sufi Order'],
  ['titles', 'Titles'],
  ['teachers', 'Teachers'],
  ['notableStudents', 'Notable Students'],
  ['majorWorks', 'Major Works'],
  ['burial', 'Burial'],
]

export default function Chapter({ chapter }) {
  const meta = chapter.metadata || {}

  return (
    <>
      <div className="mb-24 pt-6" id={`ch-${chapter.number}`}>
        {/* Header */}
        <div className="mb-7">
          <span className="block text-[0.68rem] uppercase tracking-[0.16em] text-accent mb-2">
            Chapter {chapter.number}
          </span>
          <h2 className="text-[1.95rem] font-normal leading-[1.25] text-ink">
            {chapter.name}
          </h2>
          {chapter.arabicName && (
            <span
              className="block font-arabic text-[1.4rem] text-muted mt-1"
              dir="rtl"
              style={{ textAlign: 'right' }}
            >
              {chapter.arabicName}
            </span>
          )}
        </div>

        {/* Metadata */}
        {Object.keys(meta).length > 0 && (
          <div className="my-7 py-5 px-7 bg-parchment-alt border-l-[3px] border-gold text-[0.9rem]">
            {META_DISPLAY.map(([key, label]) => {
              const value = meta[key]
              if (!value) return null
              return (
                <div key={key} className="grid grid-cols-[150px_1fr] gap-x-3 py-0.5 leading-[1.6]">
                  <span className="font-semibold text-muted text-[0.78rem] uppercase tracking-[0.04em] pt-0.5">
                    {label}
                  </span>
                  <Prose text={value} className="text-ink" />
                </div>
              )
            })}
          </div>
        )}

        {/* Biography */}
        {chapter.biography && (
          <Section title="Biography">
            <Paragraphs items={chapter.biography} />
          </Section>
        )}

        {/* Key Teachings */}
        {chapter.keyTeachings && (
          <Section title="Key Teachings">
            <Paragraphs items={chapter.keyTeachings} />
          </Section>
        )}

        {/* Famous Stories */}
        {chapter.famousStories?.length > 0 && (
          <Section title="Famous Stories">
            {chapter.famousStories.map((story, i) => (
              <div key={i} className="my-5 py-4 px-5 pl-5 bg-gold/5 border-l-2 border-gold">
                <Prose
                  text={`**${story.title}:** ${story.content}`}
                  as="p"
                />
              </div>
            ))}
          </Section>
        )}

        {/* Major Works */}
        {(chapter.majorWorksList || chapter.majorWorksText) && (
          <Section title="Major Works">
            {chapter.majorWorksList ? (
              <ul className="my-2 ml-6 space-y-1">
                {chapter.majorWorksList.map((w, i) => (
                  <li key={i}>
                    <Prose text={`**${w.title}:** ${w.description}`} />
                  </li>
                ))}
              </ul>
            ) : (
              <Paragraphs items={chapter.majorWorksText} />
            )}
          </Section>
        )}

        {/* Legacy */}
        {chapter.legacy && (
          <Section title="Legacy">
            <Paragraphs items={chapter.legacy} />
          </Section>
        )}

        {/* Sources */}
        {chapter.sources && <Sources sources={chapter.sources} />}
      </div>
      <hr className="border-t border-book-border" />
    </>
  )
}
