import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Part from './pages/Part'
import Timeline from './pages/Timeline'
import ByOrder from './pages/ByOrder'
import Relationships from './pages/Relationships'
import FullIndex from './pages/FullIndex'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="part/:id" element={<Part />} />
        <Route path="timeline" element={<Timeline />} />
        <Route path="by-order" element={<ByOrder />} />
        <Route path="relationships" element={<Relationships />} />
        <Route path="full-index" element={<FullIndex />} />
      </Route>
    </Routes>
  )
}
