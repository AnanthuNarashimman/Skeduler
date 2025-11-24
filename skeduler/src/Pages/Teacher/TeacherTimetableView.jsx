import React, { useState, useEffect } from 'react';
import { useAuth, apiClient } from '../../contexts/AuthContext';
import TeacherNavbar from './TeacherNavbar';
import './TeacherTimetableView.css';

function TeacherTimetableView() {
  const { teacher } = useAuth();
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedClass, setSelectedClass] = useState(null);

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const periods = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'];

  useEffect(() => {
    fetchTimetable();
  }, []);

  const fetchTimetable = async () => {
    try {
      const response = await apiClient.get('/api/teacher/timetable');
      if (response.data.status === 'success') {
        setSchedule(response.data.schedule);
        // Set first class as default
        const firstClass = Object.keys(response.data.schedule)[0];
        if (firstClass) {
          setSelectedClass(firstClass);
        }
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching timetable:', err);
      setLoading(false);
    }
  };

  const isTeacherPeriod = (dayIdx, periodIdx) => {
    if (!schedule || !selectedClass) return false;
    const classData = schedule[selectedClass];
    return classData.periods.some(
      period => period.day === dayIdx && period.period === periodIdx
    );
  };

  if (loading) {
    return (
      <>
        <TeacherNavbar />
        <div className="teacher-page">
          <div className="loading-container">
            <div className="spinner-large"></div>
            <p>Loading timetable...</p>
          </div>
        </div>
      </>
    );
  }

  if (!schedule || Object.keys(schedule).length === 0) {
    return (
      <>
        <TeacherNavbar />
        <div className="teacher-page">
          <div className="no-timetable">
            <h2>No Timetable Available</h2>
            <p>You don't have any classes assigned yet.</p>
          </div>
        </div>
      </>
    );
  }

  const currentClassSchedule = schedule[selectedClass];

  return (
    <>
      <TeacherNavbar />
      <div className="teacher-page">
        <div className="timetable-header">
          <h1>My Timetable</h1>
          <p>Your assigned classes and periods</p>
        </div>

        <div className="class-selector">
          {Object.keys(schedule).map(className => (
            <button
              key={className}
              className={`class-selector-btn ${selectedClass === className ? 'active' : ''}`}
              onClick={() => setSelectedClass(className)}
            >
              {className}
            </button>
          ))}
        </div>

        <div className="timetable-container">
          <div className="timetable-info">
            <h3>{selectedClass}</h3>
            <p>{currentClassSchedule.periods.length} periods per week</p>
          </div>

          <div className="timetable-grid">
            <div className="timetable-cell header-cell">Day/Period</div>
            {periods.map(period => (
              <div key={period} className="timetable-cell header-cell">
                {period}
              </div>
            ))}

            {days.map((day, dayIdx) => (
              <React.Fragment key={day}>
                <div className="timetable-cell day-cell">{day}</div>
                {periods.map((_, periodIdx) => {
                  const isTeacher = isTeacherPeriod(dayIdx, periodIdx);
                  const daySchedule = currentClassSchedule.full_schedule[dayIdx];
                  const periodContent = daySchedule ? daySchedule[periodIdx] : '--- FREE ---';

                  return (
                    <div
                      key={`${dayIdx}-${periodIdx}`}
                      className={`timetable-cell content-cell ${isTeacher ? 'teacher-period' : ''} ${periodContent.toLowerCase().includes('lab') ? 'lab-cell' : ''}`}
                    >
                      {periodContent}
                    </div>
                  );
                })}
              </React.Fragment>
            ))}
          </div>

          <div className="legend">
            <div className="legend-item">
              <div className="legend-color teacher-highlight"></div>
              <span>Your Periods</span>
            </div>
            <div className="legend-item">
              <div className="legend-color lab-highlight"></div>
              <span>Lab Periods</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default TeacherTimetableView;
