import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { FaUser } from 'react-icons/fa';
import './TeacherNavbar.css';
import Logo from "../../assets/Images/Logo.png";

const TeacherNavbar = () => {
  const location = useLocation();
  const navigate = useNavigate();

  return (
    <nav className="teacher-navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <img src={Logo} alt="Skeduler Logo" className="navbar-logo" />
        </div>

        <div className="navbar-menu">
          <Link
            to="/teacher/dashboard"
            className={`nav-item ${location.pathname === '/teacher/dashboard' ? 'active' : ''}`}
          >
            Dashboard
          </Link>
          <Link
            to="/teacher/timetable"
            className={`nav-item ${location.pathname === '/teacher/timetable' ? 'active' : ''}`}
          >
            My Timetable
          </Link>
        </div>

        <div className="navbar-profile">
          <button 
            className="profile-button" 
            onClick={() => navigate('/teacher/profile')}
            aria-label="Profile"
          >
            <FaUser />
          </button>
        </div>
      </div>
    </nav>
  );
};

export default TeacherNavbar;
