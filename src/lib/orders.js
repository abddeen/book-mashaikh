const ORDER_COLORS = [
  ['pre-tariqa', '#7a6248'],
  ['qadiri', '#2d6a4f'],
  ['chishti', '#c07030'],
  ['naqshbandi', '#2c5f8a'],
  ['shadhili', '#3a7878'],
  ["ba'alawi", '#7a1a1a'],
  ['alawi', '#7a1a1a'],
  ['tijani', '#9a7010'],
  ['mourid', '#1a6b42'],
  ['mevlevi', '#b86820'],
  ["rifa'i", '#5a7030'],
  ['rifa', '#5a7030'],
  ['kubra', '#5a3d7a'],
  ['suhrawardi', '#7a4a8a'],
  ['khalwati', '#2d4a70'],
  ['yasawi', '#8b5a2b'],
  ['sanusi', '#4a6b8a'],
  ['inayati', '#8a3d6b'],
  ['maryami', '#3d5a8a'],
  ['universal', '#8a3d6b'],
]

export function orderColor(tariqah) {
  const t = tariqah.toLowerCase()
  for (const [key, color] of ORDER_COLORS) {
    if (t.includes(key)) return color
  }
  return '#8a6840'
}

export const CANONICAL_ORDERS = [
  { name: 'Pre-Tariqa Era', color: '#7a6248', keywords: ['pre-tariqa'] },
  { name: 'Qadiriyya', color: '#2d6a4f', keywords: ['qadiri'] },
  { name: 'Chishtiyya', color: '#c07030', keywords: ['chishti'] },
  { name: 'Naqshbandiyya', color: '#2c5f8a', keywords: ['naqshbandi'] },
  { name: 'Shadhiliyya / Alawiyya', color: '#3a7878', keywords: ['shadhili'] },
  { name: "Ba'alawiyya", color: '#7a1a1a', keywords: ["ba'alawi", 'alawi'] },
  { name: 'Suhrawardiyya / Kubrawiyya', color: '#7a4a8a', keywords: ['suhrawardi', 'kubra'] },
  { name: 'Khalwatiyya', color: '#2d4a70', keywords: ['khalwati'] },
  { name: "Rifa'iyya", color: '#5a7030', keywords: ["rifa'i", 'rifa'] },
  { name: 'Mevleviyya', color: '#b86820', keywords: ['mevlevi'] },
  { name: 'Yasawiyya', color: '#8b5a2b', keywords: ['yasawi'] },
  { name: 'Tijaniyya', color: '#9a7010', keywords: ['tijani'] },
  { name: 'Mouridiyya', color: '#1a6b42', keywords: ['mourid'] },
  { name: 'Sanusiyya', color: '#4a6b8a', keywords: ['sanusi'] },
  { name: 'Universal Sufi / Inayati', color: '#8a3d6b', keywords: ['inayati', 'maryami', 'universal'] },
]

export function orderFamily(tariqah) {
  const t = tariqah.toLowerCase()
  for (const order of CANONICAL_ORDERS) {
    if (order.keywords.some(kw => t.includes(kw))) {
      return { name: order.name, color: order.color }
    }
  }
  return { name: 'Independent / Other', color: '#8a6840' }
}

export const LEGEND_ENTRIES = [
  { label: 'Pre-tariqa era', color: '#7a6248' },
  { label: 'Qadiriyya', color: '#2d6a4f' },
  { label: 'Chishtiyya', color: '#c07030' },
  { label: 'Naqshbandiyya', color: '#2c5f8a' },
  { label: 'Shadhiliyya / Alawiyya', color: '#3a7878' },
  { label: "Ba'alawiyya", color: '#7a1a1a' },
  { label: 'Tijaniyya', color: '#9a7010' },
  { label: 'Mouridiyya', color: '#1a6b42' },
  { label: "Mevleviyya / Rifa'iyya", color: '#b86820' },
  { label: 'Suhrawardiyya / Kubrawiyya', color: '#7a4a8a' },
  { label: 'Khalwatiyya', color: '#2d4a70' },
  { label: 'Others', color: '#8a6840' },
]
