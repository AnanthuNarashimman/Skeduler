import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { FaSignOutAlt, FaUser } from 'react-icons/fa';
import './TeacherNavbar.css';
import Logo from "../../assets/Images/Logo.png";

const TeacherNavbar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { teacher, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/teacher/login');
  };

  return (
    <nav className="teacher-navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <img src={Logo} alt="Skeduler Logo" className="navbar-logo" />
          <span className="navbar-subtitle">Teacher Portal</span>
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
          <div className="teacher-info">
            <FaUser className="teacher-icon" />
            <span className="teacher-name">{teacher?.name}</span>
          </div>
          <button className="logout-button" onClick={handleLogout}>
            <FaSignOutAlt />
            Logout
          </button>
        </div>
      </div>
    </nav>
  );
};

export default TeacherNavbar;
