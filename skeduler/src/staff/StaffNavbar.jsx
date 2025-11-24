import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './StaffNavbar.css';
import { FaEnvelope } from 'react-icons/fa';
import Logo from "../assets/Images/Logo.png";

const StaffNavbar = ({ activePage = 'Dashboard' }) => {
  const location = useLocation();
  const [activeTab, setActiveTab] = useState(activePage);
  const [showContactModal, setShowContactModal] = useState(false);
  const [contactMessage, setContactMessage] = useState('');

  const navItems = [
    { name: 'Dashboard', path: '/staff' },
    { name: 'Timetables', path: '/staff/timetables' }
  ];

  const handleSendEmail = () => {
    const subject = encodeURIComponent('Skeduler - Staff Contact');
    const body = encodeURIComponent(contactMessage);
    window.location.href = `mailto:staff-support@skeduler.example?subject=${subject}&body=${body}`;
    setShowContactModal(false);
    setContactMessage('');
  };

  return (
    <>
      <nav className="staff-navbar">
        <div className="navbar-container">
          <div className="navbar-brand">
            <img src={Logo} alt="Skeduler Logo" className="navbar-logo" />
          </div>

          <div className="navbar-menu">
            {navItems.map((item) => (
              <Link
                key={item.name}
                to={item.path}
                className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
              >
                {item.name}
              </Link>
            ))}
          </div>

          <div className="navbar-profile">
            <button className="profile-button" aria-label="Contact Support" onClick={() => setShowContactModal(true)}>
              <FaEnvelope />
            </button>
          </div>
        </div>
      </nav>

      {showContactModal && (
        <div className="contact-modal-overlay" onClick={() => setShowContactModal(false)}>
          <div className="contact-modal" onClick={(e) => e.stopPropagation()}>
            <div className="contact-modal-header">
              <h3>Contact Support</h3>
              <button className="close-contact-btn" onClick={() => setShowContactModal(false)}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
            <div className="contact-modal-body">
              <label htmlFor="contact-message">Message</label>
              <textarea
                id="contact-message"
                className="contact-textarea"
                placeholder="Type your message here..."
                value={contactMessage}
                onChange={(e) => setContactMessage(e.target.value)}
                rows="6"
              />
            </div>
            <div className="contact-modal-footer">
              <button className="send-email-btn" onClick={handleSendEmail} disabled={!contactMessage.trim()}>
                <FaEnvelope className="btn-icon" />
                Send Email
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default StaffNavbar;
