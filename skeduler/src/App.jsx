import './App.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

import LandingPage from './Pages/LandingPage'
import Test from './Pages/Test'
import AdminDashboard from './admin/AdminDashboard'
import StaffPage from './Pages/StaffPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/test" element={<Test />} />
        <Route path="/admin-dash" element={<AdminDashboard />} />
        <Route path="/staff" element={<StaffPage />} />
      </Routes>
    </BrowserRouter>
  )
}
export default App