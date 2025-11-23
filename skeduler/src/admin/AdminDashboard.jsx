import React from 'react';
import './AdminDashboard.css';
import AdminNavbar from './AdminNavbar';

import Create from "../assets/Images/Create.png";
import Manage from "../assets/Images/Manage.png";
import Staffs from "../assets/Images/Staffs.png";
import Announce from "../assets/Images/Announcements.png";

const AdminDashboard = () => {
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
        <div className="stat-card">
          <div className="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M3 9H21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M9 21V9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="stat-content">
            <h3>Classes in Department</h3>
            <p className="stat-number">24</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M17 21V19C17 17.9391 16.5786 16.9217 15.8284 16.1716C15.0783 15.4214 14.0609 15 13 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M9 11C11.2091 11 13 9.20914 13 7C13 4.79086 11.2091 3 9 3C6.79086 3 5 4.79086 5 7C5 9.20914 6.79086 11 9 11Z" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M23 21V19C22.9993 18.1137 22.7044 17.2528 22.1614 16.5523C21.6184 15.8519 20.8581 15.3516 20 15.13" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
              <path d="M16 3.13C16.8604 3.35031 17.623 3.85071 18.1676 4.55232C18.7122 5.25392 19.0078 6.11683 19.0078 7.005C19.0078 7.89318 18.7122 8.75608 18.1676 9.45769C17.623 10.1593 16.8604 10.6597 16 10.88" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="stat-content">
            <h3>Staff in Department</h3>
            <p className="stat-number">42</p>
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
              <button className="action-button">
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
              <button className="action-button">
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
              <button className="action-button">
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
              <button className="action-button">
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
    </div>
    </>
  );
};

export default AdminDashboard;
