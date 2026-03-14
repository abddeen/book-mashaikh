export function renderInline(text) {
  if (!text) return ''
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/(?<!\*)\*([^*\n]+?)\*(?!\*)/g, '<em>$1</em>')
}

export function Prose({ text, as: Tag = 'span', className = '' }) {
  if (!text) return null
  return <Tag className={className} dangerouslySetInnerHTML={{ __html: renderInline(text) }} />
}
