import React, { useState } from 'react';
import axios from 'axios';
import '../PageStyles/Create.css';
import AdminNavbar from '../admin/AdminNavbar';

function CreateTimetable() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("idle"); // 'idle', 'uploading', 'success', 'error', 'saving'
  const [schedule, setSchedule] = useState(null);
  const [errorMsg, setErrorMsg] = useState("");
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [savedMessage, setSavedMessage] = useState("");

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus("idle"); // Reset status on new file
      setSchedule(null);
      setShowConfirmation(false);
      setSavedMessage("");
    }
  };

  const handleUpload = async () => {
    if (!file) return;
    
    const formData = new FormData();
    formData.append('file', file);
    
    setStatus("uploading");
    setErrorMsg("");
    
    try {
      // Adjust the URL if your Flask port is different
      const res = await axios.post('http://localhost:5000/api/upload-schedule', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      if (res.data.status === 'success') {
        setStatus("success");
        setSchedule(res.data.schedule);
        setShowConfirmation(true);
      } else {
        setStatus("error");
        setErrorMsg(res.data.message || "Unknown error occurred");
      }
    } catch (err) {
      setStatus("error");
      setErrorMsg(err.response?.data?.message || "Server connection failed");
      console.error(err);
    }
  };

  const handleSave = async () => {
    setStatus("saving");
    setSavedMessage("");
    
    try {
      const saveData = {
        schedule_data: schedule,
        department: "CSE",
        file_name: file?.name || "timetable.xlsx",
        academic_year: new Date().getFullYear().toString()
      };
      
      const res = await axios.post('http://localhost:5000/api/save-timetable', saveData);
      
      if (res.data.status === 'success') {
        setSavedMessage("Timetable saved successfully!");
        setShowConfirmation(false);
        setTimeout(() => {
          // Reset form after successful save
          setFile(null);
          setSchedule(null);
          setStatus("idle");
          setSavedMessage("");
        }, 3000);
      } else {
        setStatus("error");
        setErrorMsg(res.data.message || "Failed to save timetable");
      }
    } catch (err) {
      setStatus("error");
      setErrorMsg(err.response?.data?.message || "Failed to save to database");
      console.error(err);
    }
  };

  const handleCancel = () => {
    setShowConfirmation(false);
    setSchedule(null);
    setFile(null);
    setStatus("idle");
  };

  return (
    <>
      <AdminNavbar activePage="Create" />
      <div className="timetable-page">
      <div className="header-section">
        <h2>Create New Timetable</h2>
        <p>Upload your department data Excel sheet to generate an optimized schedule.</p>
      </div>
      
      <div className="upload-card">
        <div className="file-input-container">
          <input 
            type="file" 
            id="excel-upload" 
            onChange={handleFileChange} 
            accept=".xlsx, .xls" 
            className="file-input"
            disabled={status === 'uploading' || status === 'saving'}
          />
          <label htmlFor="excel-upload" className="file-label">
            {file ? (
              <span className="filename">
                <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                {file.name}
              </span>
            ) : (
              <span>
                <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="17 8 12 3 7 8"></polyline>
                  <line x1="12" y1="3" x2="12" y2="15"></line>
                </svg>
                Click to Select Excel File
              </span>
            )}
          </label>
        </div>

        {file && !showConfirmation && (
          <button 
            className={`generate-btn ${status === 'uploading' ? 'disabled' : ''}`} 
            onClick={handleUpload}
            disabled={status === 'uploading'}
          >
            {status === 'uploading' ? (
              <span className="loader">
                <span className="spinner"></span> Optimizing...
              </span>
            ) : (
              <>
                <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="16 18 22 12 16 6"></polyline>
                  <polyline points="8 6 2 12 8 18"></polyline>
                </svg>
                Generate Schedule
              </>
            )}
          </button>
        )}

        {status === 'error' && (
          <div className="error-message">
            <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            <strong>Error:</strong> {errorMsg}
          </div>
        )}
        
        {savedMessage && (
          <div className="success-message">
            <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
            {savedMessage}
          </div>
        )}
      </div>

      {showConfirmation && schedule && (
        <div className="confirmation-section">
          <div className="confirmation-card">
            <svg className="warning-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
              <line x1="12" y1="9" x2="12" y2="13"></line>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            <h3>Confirm Your Action</h3>
            <p>
              <strong>Warning:</strong> Saving this timetable will <strong>delete all previously saved timetables</strong> from the database. 
              Each class will be saved as a separate timetable card. Do you want to proceed?
            </p>
            <div className="confirmation-buttons">
              <button className="save-btn" onClick={handleSave} disabled={status === 'saving'}>
                {status === 'saving' ? (
                  <span><span className="spinner"></span> Saving...</span>
                ) : (
                  <>
                    <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                      <polyline points="17 21 17 13 7 13 7 21"></polyline>
                      <polyline points="7 3 7 8 15 8"></polyline>
                    </svg>
                    Save Timetable
                  </>
                )}
              </button>
              <button className="cancel-btn" onClick={handleCancel} disabled={status === 'saving'}>
                <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {status === 'success' && schedule && (
        <div className="results-section">
          <div className="success-banner">
            <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            Schedule Generated Successfully!
          </div>
          
          <div className="timetable-grid-view">
            {Object.keys(schedule).sort().map(className => (
              <div key={className} className="class-schedule-card">
                <h3 className="class-header">Class: {className}</h3>
                <div className="grid-layout">
                  {/* Header Row */}
                  <div className="grid-cell header-cell">Day / Period</div>
                  {[1, 2, 3, 4, 5, 6, 7].map(p => (
                    <div key={p} className="grid-cell header-cell">P{p}</div>
                  ))}
                  
                  {/* Data Rows */}
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
            ))}
          </div>
        </div>
      )}
      </div>
    </>
  );
}

export default CreateTimetable;