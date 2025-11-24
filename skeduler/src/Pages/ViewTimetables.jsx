import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../PageStyles/ViewTimetables.css';
import AdminNavbar from '../admin/AdminNavbar';

function ViewTimetables() {
  const [timetables, setTimetables] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedTimetable, setSelectedTimetable] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    fetchTimetables();
  }, []);

  const fetchTimetables = async () => {
    setLoading(true);
    setError("");
    
    try {
      const res = await axios.get('http://localhost:5000/api/timetables');
      
      if (res.data.status === 'success') {
        setTimetables(res.data.timetables);
      } else {
        setError(res.data.message || "Failed to fetch timetables");
      }
    } catch (err) {
      setError(err.response?.data?.message || "Server connection failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCardClick = (timetable) => {
    setSelectedTimetable(timetable);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setTimeout(() => setSelectedTimetable(null), 300);
  };

  const downloadTimetable = () => {
    if (!selectedTimetable) return;

    const schedule = selectedTimetable.schedule_data;
    let csvContent = "Class,Day,Period 1,Period 2,Period 3,Period 4,Period 5,Period 6,Period 7\n";

    Object.keys(schedule).forEach(className => {
      const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      days.forEach((day, dayIdx) => {
        const periods = schedule[className][dayIdx.toString()] || [];
        csvContent += `${className},${day},${periods.join(',')}\n`;
      });
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `timetable_${selectedTimetable.id}_${Date.now()}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };

  const getClassList = (scheduleData) => {
    try {
      // scheduleData is already an object from the backend
      const schedule = typeof scheduleData === 'string' ? JSON.parse(scheduleData) : scheduleData;
      return Object.keys(schedule);
    } catch {
      return [];
    }
  };

  const getClassName = (scheduleData) => {
    try {
      // scheduleData is already an object from the backend
      const schedule = typeof scheduleData === 'string' ? JSON.parse(scheduleData) : scheduleData;
      const keys = Object.keys(schedule);
      return keys.length > 0 ? keys[0] : 'Unknown';
    } catch {
      return 'Unknown';
    }
  };

  const handleDeleteAll = async () => {
    setDeleting(true);
    setError("");
    
    try {
      const res = await axios.delete('http://localhost:5000/api/timetables/delete-all');
      
      if (res.data.status === 'success') {
        setTimetables([]);
        setShowDeleteConfirm(false);
      } else {
        setError(res.data.message || "Failed to delete timetables");
      }
    } catch (err) {
      setError(err.response?.data?.message || "Server connection failed");
      console.error(err);
    } finally {
      setDeleting(false);
    }
  };

  return (
    <>
      <AdminNavbar activePage="View" />
      <div className="view-timetables-page">
        <div className="header-section">
          <h2>Timetable Gallery</h2>
          <p>View and download all created timetables</p>
          {timetables.length > 0 && (
            <button 
              className="delete-all-btn"
              onClick={() => setShowDeleteConfirm(true)}
              disabled={deleting}
            >
              <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                <line x1="10" y1="11" x2="10" y2="17"></line>
                <line x1="14" y1="11" x2="14" y2="17"></line>
              </svg>
              Delete All
            </button>
          )}
        </div>

        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading timetables...</p>
          </div>
        )}

        {error && (
          <div className="error-banner">
            <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            <strong>Error:</strong> {error}
          </div>
        )}

        {!loading && !error && timetables.length === 0 && (
          <div className="empty-state">
            <svg className="empty-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
            <h3>No Timetables Found</h3>
            <p>Create your first timetable to see it here</p>
          </div>
        )}

        {!loading && !error && timetables.length > 0 && (
          <div className="timetables-grid">
            {timetables.map((timetable) => {
              const className = getClassName(timetable.schedule_data);
              return (
                <div 
                  key={timetable.id} 
                  className="timetable-card"
                  onClick={() => handleCardClick(timetable)}
                >
                  <div className="card-header">
                    <svg className="card-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                      <line x1="16" y1="2" x2="16" y2="6"></line>
                      <line x1="8" y1="2" x2="8" y2="6"></line>
                      <line x1="3" y1="10" x2="21" y2="10"></line>
                    </svg>
                    <div className="card-badge">{timetable.department}</div>
                  </div>
                  <div className="card-body">
                    <h3 className="class-name">{className}</h3>
                    <div className="card-meta">
                      <span className="meta-item">
                        <svg className="meta-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <circle cx="12" cy="12" r="10"></circle>
                          <polyline points="12 6 12 12 16 14"></polyline>
                        </svg>
                        {formatDate(timetable.created_at)}
                      </span>
                      {timetable.academic_year && (
                        <span className="meta-item">
                          <svg className="meta-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                            <line x1="16" y1="2" x2="16" y2="6"></line>
                            <line x1="8" y1="2" x2="8" y2="6"></line>
                            <line x1="3" y1="10" x2="21" y2="10"></line>
                          </svg>
                          AY {timetable.academic_year}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="card-footer">
                    <span className="view-text">Click to view</span>
                    <svg className="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <line x1="5" y1="12" x2="19" y2="12"></line>
                      <polyline points="12 5 19 12 12 19"></polyline>
                    </svg>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Modal */}
        {showModal && selectedTimetable && (
          <div className="modal-overlay" onClick={closeModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <div>
                  <h3>Timetable Details</h3>
                  <p className="modal-subtitle">
                    {selectedTimetable.department} • Created on {formatDate(selectedTimetable.created_at)}
                  </p>
                </div>
                <button className="close-btn" onClick={closeModal}>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>

              <div className="modal-body">
                {(() => {
                  const schedule = selectedTimetable.schedule_data;
                  return Object.keys(schedule).sort().map(className => (
                    <div key={className} className="modal-schedule-card">
                      <h4 className="modal-class-header">Class: {className}</h4>
                      <div className="modal-grid-layout">
                        <div className="grid-cell header-cell">Day / Period</div>
                        {[1, 2, 3, 4, 5, 6, 7].map(p => (
                          <div key={p} className="grid-cell header-cell">P{p}</div>
                        ))}
                        
                        {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((dayName, dayIdx) => (
                          <React.Fragment key={dayIdx}>
                            <div className="grid-cell day-cell">{dayName}</div>
                            {(schedule[className][dayIdx.toString()] || []).map((subject, pIdx) => (
                              <div 
                                key={pIdx} 
                                className={`grid-cell content-cell ${subject.includes('Lab') ? 'lab-cell' : ''} ${subject === "--- FREE ---" ? 'free-cell' : ''}`}
                              >
                                {subject}
                              </div>
                            ))}
                          </React.Fragment>
                        ))}
                      </div>
                    </div>
                  ));
                })()}
              </div>

              <div className="modal-footer">
                <button className="download-btn" onClick={downloadTimetable}>
                  <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                  </svg>
                  Download CSV
                </button>
                <button className="close-modal-btn" onClick={closeModal}>
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="delete-modal-overlay" onClick={() => setShowDeleteConfirm(false)}>
          <div className="delete-modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="delete-modal-header">
              <svg className="warning-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
              <h3>Delete All Timetables?</h3>
            </div>
            <div className="delete-modal-body">
              <p>Are you sure you want to delete all {timetables.length} timetable(s)?</p>
              <p className="warning-text">This action cannot be undone.</p>
            </div>
            <div className="delete-modal-footer">
              <button 
                className="cancel-delete-btn" 
                onClick={() => setShowDeleteConfirm(false)}
                disabled={deleting}
              >
                Cancel
              </button>
              <button 
                className="confirm-delete-btn" 
                onClick={handleDeleteAll}
                disabled={deleting}
              >
                {deleting ? (
                  <>
                    <div className="delete-spinner"></div>
                    Deleting...
                  </>
                ) : (
                  <>
                    <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                    Delete All
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default ViewTimetables;
