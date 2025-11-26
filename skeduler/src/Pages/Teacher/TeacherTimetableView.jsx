import React, { useState, useEffect } from 'react';
import { useAuth, apiClient } from '../../contexts/AuthContext';
import TeacherNavbar from './TeacherNavbar';
import './TeacherTimetableView.css';

function TeacherTimetableView() {
  const { teacher } = useAuth();
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(true);
  const [unifiedSchedule, setUnifiedSchedule] = useState({});
  const [totalPeriods, setTotalPeriods] = useState(0);

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
        buildUnifiedSchedule(response.data.schedule);
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching timetable:', err);
      setLoading(false);
    }
  };

  const buildUnifiedSchedule = (scheduleData) => {
    const unified = {};
    let count = 0;

    // Initialize empty schedule
    for (let day = 0; day < 6; day++) {
      unified[day] = {};
      for (let period = 0; period < 7; period++) {
        unified[day][period] = null;
      }
    }

    // Fill in teacher's periods from all classes
    Object.entries(scheduleData).forEach(([className, classData]) => {
      classData.periods.forEach(period => {
        unified[period.day][period.period] = {
          class: className,
          subject: period.subject
        };
        count++;
      });
    });

    setUnifiedSchedule(unified);
    setTotalPeriods(count);
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

  return (
    <>
      <TeacherNavbar />
      <div className="teacher-page">
        <div className="timetable-header">
          <h1>My Weekly Schedule</h1>
          <p>Teaching {Object.keys(schedule).length} classes with {totalPeriods} periods per week</p>
        </div>

        <div className="timetable-container">
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
                  const periodData = unifiedSchedule[dayIdx]?.[periodIdx];

                  return (
                    <div
                      key={`${dayIdx}-${periodIdx}`}
                      className={`timetable-cell content-cell ${periodData ? 'teacher-period' : 'free-period'} ${periodData?.subject.toLowerCase().includes('lab') ? 'lab-cell' : ''} ${periodData?.subject.toLowerCase().includes('tutorial') ? 'tutorial-cell' : ''}`}
                    >
                      {periodData ? (
                        <>
                          <div className="class-name">{periodData.class}</div>
                          <div className="subject-name">{periodData.subject}</div>
                        </>
                      ) : (
                        <span className="free-text">Free</span>
                      )}
                    </div>
                  );
                })}
              </React.Fragment>
            ))}
          </div>

          <div className="legend">
            <div className="legend-item">
              <div className="legend-color teacher-highlight"></div>
              <span>Your Classes</span>
            </div>
            <div className="legend-item">
              <div className="legend-color lab-highlight"></div>
              <span>Lab Periods</span>
            </div>
            <div className="legend-item">
              <div className="legend-color free-highlight"></div>
              <span>Free Periods</span>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default TeacherTimetableView;
