import React, { useState } from 'react';
import './AdminNavbar.css';
import { FaUser } from 'react-icons/fa';
import Logo from "../assets/Images/Logo.png";

const AdminNavbar = ({ activePage = 'Dashboard' }) => {
  const [activeTab, setActiveTab] = useState(activePage);

  const navItems = [
    { name: 'Dashboard', path: '/admin/dashboard' },
    { name: 'Staff Directory', path: '/admin/staff' },
    { name: 'Timetables', path: '/admin/timetables' },
    { name: 'Contact', path: '/admin/contact' }
  ];

  return (
    <nav className="admin-navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <img src={Logo} alt="Skeduler Logo" className="navbar-logo" />
        </div>
        
        <div className="navbar-menu">
          {navItems.map((item) => (
            <a
              key={item.name}
              href={item.path}
              className={`nav-item ${activeTab === item.name ? 'active' : ''}`}
              onClick={(e) => {
                e.preventDefault();
                setActiveTab(item.name);
              }}
            >
              {item.name}
            </a>
          ))}
        </div>

        <div className="navbar-profile">
          <button className="profile-button" aria-label="User Profile">
            <FaUser />
          </button>
        </div>
      </div>
    </nav>
  );
};

export default AdminNavbar;
