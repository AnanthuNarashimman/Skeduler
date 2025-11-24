import { useState } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";


import LandingPage from './Pages/LandingPage';
import Test from './Pages/Test';
import AdminDashboard from './admin/AdminDashboard';
import CreateTimetable from './Pages/CreateTimetable';
import ViewTimetables from './Pages/ViewTimetables';

function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/test" element={<Test />} />
        <Route path='/admin/dashboard' element={<AdminDashboard />} />
        <Route path='/create' element={<CreateTimetable />} />
        <Route path='/view' element={<ViewTimetables />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
