import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, apiClient } from '../../contexts/AuthContext';
import TeacherNavbar from './TeacherNavbar';
import { FaChalkboardTeacher, FaClock, FaBook } from 'react-icons/fa';
import './TeacherDashboard.css';

function TeacherDashboard() {
  const { teacher } = useAuth();
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    fetchTimetable();
  }, []);

  const fetchTimetable = async () => {
    try {
      const response = await apiClient.get('/api/teacher/timetable');
      if (response.data.status === 'success') {
        setSchedule(response.data.schedule);
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching timetable:', err);
      setError('Failed to load timetable');
      setLoading(false);
    }
  };

  const calculateTotalPeriods = () => {
    if (!schedule) return 0;
    return Object.values(schedule).reduce((total, classData) => {
      return total + classData.periods.length;
    }, 0);
  };

  if (loading) {
    return (
      <>
        <TeacherNavbar />
        <div className="teacher-page">
          <div className="loading-container">
            <div className="spinner-large"></div>
            <p>Loading your timetable...</p>
          </div>
        </div>
      </>
    );
  }

  return (
    <>
      <TeacherNavbar />
      <div className="teacher-page">
        <div className="dashboard-header">
          <h1>Welcome, {teacher?.name}!</h1>
          <p>Here's your teaching schedule overview</p>
        </div>

        {error && (
          <div className="error-message">
            <p>{error}</p>
          </div>
        )}

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #6ba3d8, #4a8bc2)' }}>
              <FaChalkboardTeacher />
            </div>
            <div className="stat-content">
              <h3>{schedule ? Object.keys(schedule).length : 0}</h3>
              <p>Classes Assigned</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #10b981, #059669)' }}>
              <FaClock />
            </div>
            <div className="stat-content">
              <h3>{calculateTotalPeriods()}</h3>
              <p>Weekly Periods</p>
            </div>
          </div>

          <div className="stat-card">
            <div className="stat-icon" style={{ background: 'linear-gradient(135deg, #f59e0b, #d97706)' }}>
              <FaBook />
            </div>
            <div className="stat-content">
              <h3>{teacher?.department}</h3>
              <p>Department</p>
            </div>
          </div>
        </div>

        <div className="classes-section">
          <h2>Your Classes</h2>
          {!schedule || Object.keys(schedule).length === 0 ? (
            <div className="no-classes">
              <p>No classes assigned yet</p>
            </div>
          ) : (
            <div className="classes-grid">
              {Object.entries(schedule).map(([className, classData]) => (
                <div key={className} className="class-card" onClick={() => navigate('/teacher/timetable', { state: { className } })}>
                  <div className="class-card-header">
                    <h3>{className}</h3>
                    <span className="period-badge">{classData.periods.length} periods</span>
                  </div>
                  <div className="class-card-body">
                    <p><strong>Department:</strong> {classData.department}</p>
                    <p><strong>Academic Year:</strong> {classData.academic_year || 'N/A'}</p>
                  </div>
                  <div className="class-card-footer">
                    <button className="view-button">View Timetable →</button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default TeacherDashboard;
