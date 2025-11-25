import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth, apiClient } from '../../contexts/AuthContext';
import TeacherNavbar from './TeacherNavbar';
import { FaUser, FaEnvelope, FaBriefcase, FaLock, FaSignOutAlt } from 'react-icons/fa';
import './TeacherProfile.css';

function TeacherProfile() {
  const { teacher, logout } = useAuth();
  const navigate = useNavigate();
  const [showChangePassword, setShowChangePassword] = useState(false);
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [message, setMessage] = useState({ type: '', text: '' });
  const [loading, setLoading] = useState(false);

  const handlePasswordChange = async (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });

    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setMessage({ type: 'error', text: 'New passwords do not match' });
      return;
    }

    if (passwordData.newPassword.length < 6) {
      setMessage({ type: 'error', text: 'Password must be at least 6 characters long' });
      return;
    }

    setLoading(true);
    try {
      const response = await apiClient.post('/api/teacher/change-password', {
        currentPassword: passwordData.currentPassword,
        newPassword: passwordData.newPassword
      });

      if (response.data.status === 'success') {
        setMessage({ type: 'success', text: 'Password changed successfully!' });
        setPasswordData({
          currentPassword: '',
          newPassword: '',
          confirmPassword: ''
        });
        setShowChangePassword(false);
      }
    } catch (err) {
      setMessage({ 
        type: 'error', 
        text: err.response?.data?.message || 'Failed to change password' 
      });
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <>
      <TeacherNavbar />
      <div className="teacher-page">
        <div className="profile-container">
          <div className="profile-header">
            <div className="profile-avatar">
              <FaUser />
            </div>
            <h1>My Profile</h1>
            <p>Manage your account information</p>
          </div>

          <div className="profile-content">
            <div className="profile-info-card">
              <h2>Personal Information</h2>
              <div className="info-grid">
                <div className="info-item">
                  <div className="info-icon">
                    <FaUser />
                  </div>
                  <div className="info-content">
                    <label>Full Name</label>
                    <p>{teacher?.name}</p>
                  </div>
                </div>

                <div className="info-item">
                  <div className="info-icon">
                    <FaEnvelope />
                  </div>
                  <div className="info-content">
                    <label>Email Address</label>
                    <p>{teacher?.email || 'Not provided'}</p>
                  </div>
                </div>

                <div className="info-item">
                  <div className="info-icon">
                    <FaBriefcase />
                  </div>
                  <div className="info-content">
                    <label>Department</label>
                    <p>{teacher?.department}</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="profile-actions-card">
              <h2>Account Actions</h2>
              
              <div className="action-item">
                <div className="action-header">
                  <div className="action-info">
                    <FaLock className="action-icon" />
                    <div>
                      <h3>Change Password</h3>
                      <p>Update your account password</p>
                    </div>
                  </div>
                  <button 
                    className="action-btn change-password-btn"
                    onClick={() => setShowChangePassword(!showChangePassword)}
                  >
                    {showChangePassword ? 'Cancel' : 'Change Password'}
                  </button>
                </div>

                {showChangePassword && (
                  <form className="password-form" onSubmit={handlePasswordChange}>
                    {message.text && (
                      <div className={`message ${message.type}`}>
                        {message.text}
                      </div>
                    )}
                    
                    <div className="form-group">
                      <label>Current Password</label>
                      <input
                        type="password"
                        value={passwordData.currentPassword}
                        onChange={(e) => setPasswordData({ ...passwordData, currentPassword: e.target.value })}
                        required
                        placeholder="Enter current password"
                      />
                    </div>

                    <div className="form-group">
                      <label>New Password</label>
                      <input
                        type="password"
                        value={passwordData.newPassword}
                        onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                        required
                        placeholder="Enter new password"
                      />
                    </div>

                    <div className="form-group">
                      <label>Confirm New Password</label>
                      <input
                        type="password"
                        value={passwordData.confirmPassword}
                        onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                        required
                        placeholder="Confirm new password"
                      />
                    </div>

                    <button type="submit" className="submit-btn" disabled={loading}>
                      {loading ? 'Updating...' : 'Update Password'}
                    </button>
                  </form>
                )}
              </div>

              <div className="action-item">
                <div className="action-header">
                  <div className="action-info">
                    <FaSignOutAlt className="action-icon logout-icon" />
                    <div>
                      <h3>Logout</h3>
                      <p>Sign out from your account</p>
                    </div>
                  </div>
                  <button className="action-btn logout-btn" onClick={handleLogout}>
                    Logout
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export default TeacherProfile;
