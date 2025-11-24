import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './StaffDashboard.css';
import StaffNavbar from './StaffNavbar';
import { useNavigate } from 'react-router-dom';

import Create from "../assets/Images/Create.png";
import Manage from "../assets/Images/Manage.png";
import Staffs from "../assets/Images/Staffs.png";
import Announce from "../assets/Images/Announcements.png";

const StaffDashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [myTimetablesCount, setMyTimetablesCount] = useState(0);
  const [showComingSoonModal, setShowComingSoonModal] = useState(false);

  useEffect(() => {
    fetchMyTimetables();
  }, []);

  const fetchMyTimetables = async () => {
    try {
      // sample endpoint - adjust to your backend
      const res = await axios.get('http://localhost:5000/api/my-timetables');
      if (res.data && Array.isArray(res.data.timetables)) {
        setMyTimetablesCount(res.data.timetables.length);
      }
    } catch (err) {
      // fallback: try general timetables endpoint
      try {
        const res2 = await axios.get('http://localhost:5000/api/timetables');
        if (res2.data && Array.isArray(res2.data.timetables)) {
          setMyTimetablesCount(res2.data.timetables.length);
        }
      } catch (e) {
        console.warn('Could not fetch timetables', e);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <StaffNavbar activePage="Dashboard" />
      <div className="staff-dashboard">
        <div className="dashboard-header">
          <h1>Staff Dashboard</h1>
          <p className="dashboard-subtitle">Your schedules and quick actions</p>
        </div>

        <div className="stats-container">
          <div className="stat-card stat-card-single">
            <div className="stat-icon">📚</div>
            <div className="stat-content">
              <h3>My Timetables</h3>
              <p className="stat-number">{loading ? '...' : myTimetablesCount}</p>
              <p className="stat-description">Timetables assigned to you</p>
            </div>
          </div>
        </div>

        <div className="action-cards-container">
          <div className="action-card">
            <div className="action-card-left">
              <div className="action-card-content">
                <h2>View My Timetable</h2>
                <p>Open your personal timetable and download your schedule for the week.</p>
                <button className="action-button" onClick={() => navigate('/staff/timetables')}>
                  View
                  <span className="button-arrow">→</span>
                </button>
              </div>
            </div>
            <div className="action-card-image">
              <img src={Manage} alt="View Timetable" className="card-image" />
            </div>
          </div>

          <div className="action-card">
            <div className="action-card-left">
              <div className="action-card-content">
                <h2>My Classes</h2>
                <p>See classes you teach and quick links to class pages.</p>
                <button className="action-button" onClick={() => setShowComingSoonModal(true)}>
                  Open
                  <span className="button-arrow">→</span>
                </button>
              </div>
            </div>
            <div className="action-card-image">
              <img src={Staffs} alt="My Classes" className="card-image" />
            </div>
          </div>

          <div className="action-card">
            <div className="action-card-left">
              <div className="action-card-content">
                <h2>Announcements</h2>
                <p>View important announcements from administration relevant to staff.</p>
                <button className="action-button" onClick={() => setShowComingSoonModal(true)}>
                  View
                  <span className="button-arrow">→</span>
                </button>
              </div>
            </div>
            <div className="action-card-image">
              <img src={Announce} alt="Announcements" className="card-image" />
            </div>
          </div>
        </div>

        {showComingSoonModal && (
          <div className="modal-overlay" onClick={() => setShowComingSoonModal(false)}>
            <div className="coming-soon-modal" onClick={(e) => e.stopPropagation()}>
              <div className="modal-icon">🔔</div>
              <h3>Coming Soon!</h3>
              <p>This feature will be available soon for staff users.</p>
              <button className="close-modal-button" onClick={() => setShowComingSoonModal(false)}>Got it</button>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default StaffDashboard;
