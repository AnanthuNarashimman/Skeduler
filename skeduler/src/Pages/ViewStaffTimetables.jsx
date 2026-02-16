import React, { useState, useEffect } from 'react';
import axios from 'axios';
import * as XLSX from 'xlsx';
import '../PageStyles/ViewStaffTimetables.css';
import AdminNavbar from '../admin/AdminNavbar';

function ViewStaffTimetables() {
  const [staffTimetables, setStaffTimetables] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [selectedStaff, setSelectedStaff] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const daysFull = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  const periods = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'];

  useEffect(() => {
    fetchStaffTimetables();
  }, []);

  const fetchStaffTimetables = async () => {
    setLoading(true);
    setError("");

    try {
      const res = await axios.get('http://localhost:5000/api/staff-timetables');

      if (res.data.status === 'success') {
        setStaffTimetables(res.data.staff_timetables);
      } else {
        setError(res.data.message || "Failed to fetch staff timetables");
      }
    } catch (err) {
      setError(err.response?.data?.message || "Server connection failed");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCardClick = (staff) => {
    setSelectedStaff(staff);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setTimeout(() => setSelectedStaff(null), 300);
  };

  const filteredStaff = staffTimetables.filter(staff =>
    staff.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const downloadStaffTimetable = () => {
    if (!selectedStaff) return;

    const workbook = XLSX.utils.book_new();

    // Prepare data for the sheet
    const sheetData = [
      ['Day', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7']
    ];

    days.forEach((dayShort, dayIdx) => {
      const row = [daysFull[dayIdx]];
      for (let p = 0; p < 7; p++) {
        const entry = selectedStaff.schedule[dayShort][p];
        row.push(entry || 'Free');
      }
      sheetData.push(row);
    });

    // Create worksheet
    const worksheet = XLSX.utils.aoa_to_sheet(sheetData);

    // Auto-fit column widths
    const colWidths = [];
    const numCols = sheetData[0].length;

    for (let col = 0; col < numCols; col++) {
      let maxWidth = 0;
      sheetData.forEach(row => {
        const cellValue = row[col] || '';
        const cellLength = cellValue.toString().length;
        maxWidth = Math.max(maxWidth, cellLength);
      });
      colWidths.push({ wch: Math.max(maxWidth + 2, 10) });
    }

    worksheet['!cols'] = colWidths;

    // Add worksheet to workbook
    const sheetName = selectedStaff.name.length > 31 ? selectedStaff.name.substring(0, 31) : selectedStaff.name;
    XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);

    // Write file
    XLSX.writeFile(workbook, `${selectedStaff.name.replace(/[^a-zA-Z0-9]/g, '_')}_Timetable.xlsx`);
  };

  const downloadAllStaffTimetables = () => {
    if (staffTimetables.length === 0) return;

    const workbook = XLSX.utils.book_new();

    staffTimetables.forEach(staff => {
      // Prepare data for the sheet
      const sheetData = [
        ['Day', 'Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7']
      ];

      days.forEach((dayShort, dayIdx) => {
        const row = [daysFull[dayIdx]];
        for (let p = 0; p < 7; p++) {
          const entry = staff.schedule[dayShort][p];
          row.push(entry || 'Free');
        }
        sheetData.push(row);
      });

      // Create worksheet
      const worksheet = XLSX.utils.aoa_to_sheet(sheetData);

      // Auto-fit column widths
      const colWidths = [];
      const numCols = sheetData[0].length;

      for (let col = 0; col < numCols; col++) {
        let maxWidth = 0;
        sheetData.forEach(row => {
          const cellValue = row[col] || '';
          const cellLength = cellValue.toString().length;
          maxWidth = Math.max(maxWidth, cellLength);
        });
        colWidths.push({ wch: Math.max(maxWidth + 2, 10) });
      }

      worksheet['!cols'] = colWidths;

      // Add worksheet to workbook (sheet name max 31 chars)
      let sheetName = staff.name.replace(/[^a-zA-Z0-9 ]/g, '').substring(0, 31);
      // Ensure unique sheet names
      let counter = 1;
      let originalName = sheetName;
      while (workbook.SheetNames.includes(sheetName)) {
        sheetName = `${originalName.substring(0, 28)}_${counter}`;
        counter++;
      }
      XLSX.utils.book_append_sheet(workbook, worksheet, sheetName);
    });

    // Write file
    XLSX.writeFile(workbook, 'All_Staff_Timetables.xlsx');
  };

  return (
    <>
      <AdminNavbar activePage="Staff" />
      <div className="view-staff-page">
        <div className="header-section">
          <h2>Staff Timetables</h2>
          <p>View individual staff schedules and periods per week</p>
          {staffTimetables.length > 0 && (
            <div className="header-controls">
              <div className="search-box">
                <svg className="search-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <input
                  type="text"
                  placeholder="Search staff..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="search-input"
                />
              </div>
              <button className="download-all-btn" onClick={downloadAllStaffTimetables}>
                <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                  <polyline points="7 10 12 15 17 10"></polyline>
                  <line x1="12" y1="15" x2="12" y2="3"></line>
                </svg>
                Download All as Excel
              </button>
            </div>
          )}
        </div>

        {loading && (
          <div className="loading-container">
            <div className="loading-spinner"></div>
            <p>Loading staff timetables...</p>
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

        {!loading && !error && staffTimetables.length === 0 && (
          <div className="empty-state">
            <svg className="empty-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <h3>No Staff Timetables Found</h3>
            <p>Create a timetable first to see staff schedules here</p>
          </div>
        )}

        {!loading && !error && filteredStaff.length === 0 && staffTimetables.length > 0 && (
          <div className="empty-state">
            <svg className="empty-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"></circle>
              <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
            </svg>
            <h3>No Results Found</h3>
            <p>No staff members match "{searchQuery}"</p>
          </div>
        )}

        {!loading && !error && filteredStaff.length > 0 && (
          <div className="staff-grid">
            {filteredStaff.map((staff, index) => (
              <div
                key={index}
                className="staff-card"
                onClick={() => handleCardClick(staff)}
              >
                <div className="card-header">
                  <div className="staff-avatar">
                    {staff.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()}
                  </div>
                  <div className="periods-badge">
                    {staff.periods_per_week} periods/week
                  </div>
                </div>
                <div className="card-body">
                  <h3 className="staff-name">{staff.name}</h3>
                  <div className="staff-meta">
                    <span className="meta-item">
                      <svg className="meta-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"></path>
                      </svg>
                      {staff.total_classes} class{staff.total_classes !== 1 ? 'es' : ''}
                    </span>
                    <span className="meta-item">
                      <svg className="meta-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
                        <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
                      </svg>
                      {staff.total_subjects} subject{staff.total_subjects !== 1 ? 's' : ''}
                    </span>
                  </div>
                  <div className="subjects-preview">
                    {staff.subjects.slice(0, 3).map((subject, idx) => (
                      <span key={idx} className="subject-chip">{subject}</span>
                    ))}
                    {staff.subjects.length > 3 && (
                      <span className="subject-chip more">+{staff.subjects.length - 3}</span>
                    )}
                  </div>
                </div>
                <div className="card-footer">
                  <span className="view-text">View Schedule</span>
                  <svg className="arrow-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                  </svg>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Staff Timetable Modal */}
        {showModal && selectedStaff && (
          <div className="modal-overlay" onClick={closeModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <div className="modal-header-info">
                  <div className="modal-avatar">
                    {selectedStaff.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()}
                  </div>
                  <div>
                    <h3>{selectedStaff.name}</h3>
                    <p className="modal-subtitle">
                      {selectedStaff.periods_per_week} periods per week
                      <span className="dot-separator"></span>
                      {selectedStaff.total_classes} classes
                      <span className="dot-separator"></span>
                      {selectedStaff.total_subjects} subjects
                    </p>
                  </div>
                </div>
                <button className="close-btn" onClick={closeModal}>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>

              <div className="modal-body">
                <div className="schedule-grid">
                  <div className="grid-cell header-cell">Day / Period</div>
                  {periods.map(p => (
                    <div key={p} className="grid-cell header-cell">{p}</div>
                  ))}

                  {days.map((day, dayIdx) => (
                    <React.Fragment key={day}>
                      <div className="grid-cell day-cell">{daysFull[dayIdx]}</div>
                      {Array.from({ length: 7 }).map((_, periodIdx) => {
                        const entry = selectedStaff.schedule[day][periodIdx];
                        const isLab = entry && entry.toLowerCase().includes('lab');
                        const isTutorial = entry && entry.toLowerCase().includes('tutorial');

                        return (
                          <div
                            key={periodIdx}
                            className={`grid-cell content-cell ${!entry ? 'free-cell' : ''} ${isLab ? 'lab-cell' : ''} ${isTutorial ? 'tutorial-cell' : ''}`}
                          >
                            {entry || 'Free'}
                          </div>
                        );
                      })}
                    </React.Fragment>
                  ))}
                </div>

                <div className="classes-section">
                  <h4>Classes & Subjects</h4>
                  <div className="class-list">
                    {selectedStaff.classes.map((className, idx) => (
                      <div key={idx} className="class-item">
                        <span className="class-name-badge">{className}</span>
                        <span className="class-subjects">
                          {selectedStaff.periods
                            .filter(p => p.class === className)
                            .map(p => p.subject)
                            .filter((v, i, a) => a.indexOf(v) === i)
                            .join(', ')}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="modal-footer">
                <button className="download-btn" onClick={downloadStaffTimetable}>
                  <svg className="icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                    <polyline points="7 10 12 15 17 10"></polyline>
                    <line x1="12" y1="15" x2="12" y2="3"></line>
                  </svg>
                  Download Excel
                </button>
                <button className="close-modal-btn" onClick={closeModal}>
                  Close
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  );
}

export default ViewStaffTimetables;
