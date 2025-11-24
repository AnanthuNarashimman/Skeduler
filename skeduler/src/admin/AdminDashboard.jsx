import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AdminDashboard.css';
import AdminNavbar from './AdminNavbar';
import { useNavigate } from 'react-router-dom';

import Create from "../assets/Images/Create.png";
import Manage from "../assets/Images/Manage.png";
import Staffs from "../assets/Images/Staffs.png";
import Announce from "../assets/Images/Announcements.png";

const AdminDashboard = () => {
  const navigate = useNavigate();
  const department = "Computer Science & Engineering";
  const [timetableCount, setTimetableCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [showComingSoonModal, setShowComingSoonModal] = useState(false);

  useEffect(() => {
    fetchTimetableCount();
  }, []);

  const fetchTimetableCount = async () => {
    try {
      const res = await axios.get('http://localhost:5000/api/timetables');
      if (res.data.status === 'success') {
        setTimetableCount(res.data.timetables.length);
      }
    } catch (err) {
      console.error('Error fetching timetables:', err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleCreateClick = () => {
    navigate('/create');
  };

  const handleManageClick = () => {
    navigate('/view');
  };

  const handleStaffsClick = () => {
    setShowComingSoonModal(true);
  };

  const handleAnnouncementClick = () => {
    setShowComingSoonModal(true);
  };
  
  return (
    <>
      <AdminNavbar activePage="Dashboard" />
      <div className="admin-dashboard">
      <div className="dashboard-header">
        <h1>Admin Dashboard</h1>
        <p className="dashboard-subtitle">Manage your department efficiently</p>
      </div>

      {/* Stats Cards */}
      <div className="stats-container">
        <div className="stat-card stat-card-single">
          <div className="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M3 9H21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M9 21V9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="stat-content">
            <h3>Total Timetables</h3>
            <p className="stat-number">{loading ? '...' : timetableCount}</p>
            <p className="stat-description">Active class timetables in system</p>
          </div>
        </div>
      </div>

      {/* Action Cards Grid */}
      <div className="action-cards-container">
        <div className="action-card">
          <div className="action-card-left">
            <div className="action-card-content">
              <h2>Create Timetable</h2>
              <p>Design and schedule timetables for all classes efficiently. Set up courses, assign time slots, and manage scheduling conflicts seamlessly.</p>
              <button className="action-button" onClick={handleCreateClick}>
                Create
                <span className="button-arrow">→</span>
              </button>
            </div>
          </div>
          <div className="action-card-image">
            <img src={Create} alt="Create Timetable" className="card-image" />
          </div>
        </div>

        <div className="action-card">
          <div className="action-card-left">
            <div className="action-card-content">
              <h2>Manage Timetable</h2>
              <p>View, edit, and update existing timetables. Make adjustments, handle changes, and ensure optimal scheduling for all departments.</p>
              <button className="action-button" onClick={handleManageClick}>
                Manage
                <span className="button-arrow">→</span>
              </button>
            </div>
          </div>
          <div className="action-card-image">
            <img src={Manage} alt="Manage Timetable" className="card-image" />
          </div>
        </div>

        <div className="action-card">
          <div className="action-card-left">
            <div className="action-card-content">
              <h2>Manage Staffs</h2>
              <p>Add, update, or remove staff members. Manage faculty details, assign courses, and track availability for better resource management.</p>
              <button className="action-button" onClick={handleStaffsClick}>
                Manage
                <span className="button-arrow">→</span>
              </button>
            </div>
          </div>
          <div className="action-card-image">
            <img src={Staffs} alt="Manage Staffs" className="card-image" />
          </div>
        </div>

        <div className="action-card">
          <div className="action-card-left">
            <div className="action-card-content">
              <h2>Create Announcement</h2>
              <p>Broadcast important updates and notifications to staff and students. Keep everyone informed about schedule changes and events.</p>
              <button className="action-button" onClick={handleAnnouncementClick}>
                Create
                <span className="button-arrow">→</span>
              </button>
            </div>
          </div>
          <div className="action-card-image">
            <img src={Announce} alt="Create Announcement" className="card-image" />
          </div>
        </div>
      </div>

      {/* Coming Soon Modal */}
      {showComingSoonModal && (
        <div className="modal-overlay" onClick={() => setShowComingSoonModal(false)}>
          <div className="coming-soon-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
            </div>
            <h3>Coming Soon!</h3>
            <p>This feature will be available in the next update.</p>
            <button className="close-modal-button" onClick={() => setShowComingSoonModal(false)}>
              Got it
            </button>
          </div>
        </div>
      )}
    </div>
    </>
  );
};

export default AdminDashboard;
