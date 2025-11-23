import { useState } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";


import LandingPage from './Pages/LandingPage';
import Test from './Pages/Test';
import AdminDashboard from './admin/AdminDashboard';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/test" element={<Test />} />
        <Route path='/admin-dash' element={<AdminDashboard />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
