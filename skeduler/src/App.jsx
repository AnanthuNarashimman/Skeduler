import { useState } from 'react';
import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

import LandingPage from './Pages/LandingPage';
import Test from './Pages/Test';
import AdminDashboard from './admin/AdminDashboard';
import CreateTimetable from './Pages/CreateTimetable';
import ViewTimetables from './Pages/ViewTimetables';

// Teacher components
import TeacherLogin from './Pages/Teacher/TeacherLogin';
import TeacherDashboard from './Pages/Teacher/TeacherDashboard';
import TeacherTimetableView from './Pages/Teacher/TeacherTimetableView';
import TeacherProfile from './Pages/Teacher/TeacherProfile';

function App() {

  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/test" element={<Test />} />
          <Route path='/admin/dashboard' element={<AdminDashboard />} />
          <Route path='/create' element={<CreateTimetable />} />
          <Route path='/view' element={<ViewTimetables />} />

          {/* Teacher Routes */}
          <Route path='/teacher/login' element={<TeacherLogin />} />
          <Route path='/teacher/dashboard' element={
            <ProtectedRoute>
              <TeacherDashboard />
            </ProtectedRoute>
          } />
          <Route path='/teacher/timetable' element={
            <ProtectedRoute>
              <TeacherTimetableView />
            </ProtectedRoute>
          } />
          <Route path='/teacher/profile' element={
            <ProtectedRoute>
              <TeacherProfile />
            </ProtectedRoute>
          } />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
