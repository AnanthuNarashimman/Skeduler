import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Navbar from "../Components/Navbar";
import Footer from "../Components/Footer";
import Logo from "../assets/Images/Logo.png";
import "./StaffPage.css";

const sampleStaff = {
  name: 'Dr. Maya Raman',
  subjects: ['Mathematics', 'Physics', 'Algorithms'],
  classes: ['BSc-A', 'BSc-B', 'BSc-C'],
  // 0: Mon, 1: Tue, ..., 5: Sat
  timetable: {
    0: ['Mathematics', 'Algorithms', '--- FREE ---', 'Physics', 'Mathematics', '--- FREE ---', 'Algorithms'],
    1: ['--- FREE ---', 'Mathematics', 'Algorithms', 'Physics', '--- FREE ---', 'Mathematics', 'Algorithms'],
    2: ['Physics', 'Mathematics', '--- FREE ---', 'Algorithms', 'Physics', '--- FREE ---', '--- FREE ---'],
    3: ['Algorithms', '--- FREE ---', 'Mathematics', 'Physics', 'Algorithms', 'Mathematics', '--- FREE ---'],
    4: ['Mathematics', 'Physics', 'Algorithms', '--- FREE ---', 'Mathematics', 'Algorithms', 'Physics'],
    5: ['--- FREE ---', '--- FREE ---', '--- FREE ---', '--- FREE ---', '--- FREE ---', '--- FREE ---', '--- FREE ---']
  }
};

function StaffPage() {
  const navigate = useNavigate();
  const [tab, setTab] = useState('dashboard');

  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  const todayIndex = useMemo(() => {
    const jsDay = new Date().getDay(); // 0 (Sun) - 6 (Sat)
    if (jsDay === 0) return -1;
    return jsDay - 1;
  }, []);

  const staffList = [
    { id: 1, name: 'Dr. Maya Raman', subjects: ['Mathematics', 'Physics'] },
    { id: 2, name: 'Mr. Arjun Kumar', subjects: ['Chemistry'] },
    { id: 3, name: 'Ms. Leena Das', subjects: ['Computer Science', 'Algorithms'] }
  ];

  return (
    <div className="staff-page">
      <Navbar
        logo={Logo}
        logoAlt="Logo"
        items={[]}
        baseColor="#fff"
        menuColor="#000"
        buttonBgColor="#111"
        buttonTextColor="#fff"
      />

      <main className="staff-container">
        <header className="staff-header">
          <h1>Staff Dashboard</h1>
          <div className="staff-actions">
            <button className="btn" onClick={() => navigate('/')}>Back to Landing</button>
          </div>
        </header>

        <nav className="staff-subnav">
          <div className={`nav-item ${tab === 'dashboard' ? 'active' : ''}`} onClick={() => setTab('dashboard')}>Dashboard</div>
          <div className={`nav-item ${tab === 'directory' ? 'active' : ''}`} onClick={() => setTab('directory')}>Staff Directory</div>
          <div className={`nav-item ${tab === 'timetables' ? 'active' : ''}`} onClick={() => setTab('timetables')}>Timetables</div>
          <div className={`nav-item ${tab === 'contact' ? 'active' : ''}`} onClick={() => setTab('contact')}>Contact</div>
          <div className="profile-circle" title="Profile">S</div>
        </nav>

        {tab === 'dashboard' && (
          <>
            <section className="dashboard-cards">
              <div className="card">
                <div className="card-title">Name</div>
                <div className="card-value">{sampleStaff.name}</div>
              </div>
              <div className="card">
                <div className="card-title">Subjects</div>
                <div className="card-value">{sampleStaff.subjects.length}</div>
              </div>
              <div className="card">
                <div className="card-title">Classes</div>
                <div className="card-value">{sampleStaff.classes.length}</div>
              </div>
            </section>

            <section className="timetable-section">
              <h2>Common Timetable (Weekly)</h2>
              <div className="grid-container">
                <div className="grid-header-cell">Day / Period</div>
                {[1,2,3,4,5,6,7].map(p => (
                  <div key={p} className="grid-header-cell">P{p}</div>
                ))}

                {days.map((d, di) => (
                  <React.Fragment key={d}>
                    <div className="grid-day-cell">{d}</div>
                    {(sampleStaff.timetable[di] || []).map((subj, i) => (
                      <div key={i} className={`grid-cell ${subj === '--- FREE ---' ? 'free-cell' : 'filled-cell'}`}>
                        {subj}
                      </div>
                    ))}
                  </React.Fragment>
                ))}
              </div>
            </section>

            {/* Today's timetable removed from Dashboard (moved to Timetables tab) */}
          </>
        )}

        {tab === 'directory' && (
          <section className="directory-section">
            <h2>Staff Directory</h2>
            <div className="directory-grid">
              {staffList.map(s => (
                <div key={s.id} className="staff-list-card">
                  <div className="staff-name">{s.name}</div>
                  <div className="staff-subjects">{s.subjects.join(', ')}</div>
                </div>
              ))}
            </div>
          </section>
        )}

        {tab === 'timetables' && (
          <section className="timetables-section">
            <h2>Timetables</h2>
            <p>Common timetables and downloadable schedules will appear here.</p>

            {/* Today's Timetable (moved from Dashboard) */}
            <section className="today-section">
              <h3>Today's Timetable</h3>
              {todayIndex === -1 ? (
                <div className="today-alert">No classes scheduled for Sunday.</div>
              ) : (
                <div className="today-grid">
                  <div className="today-header">Day</div>
                  <div className="today-header">Period</div>
                  <div className="today-header">Subject / Location</div>
                  {(sampleStaff.timetable[todayIndex] || []).map((subj, idx) => (
                    <React.Fragment key={idx}>
                      <div className="today-day">{days[todayIndex]}</div>
                      <div className="today-period">P{idx+1}</div>
                      <div className="today-subject">{subj}</div>
                    </React.Fragment>
                  ))}
                </div>
              )}
            </section>

            <div className="grid-placeholder">(Timetable content)</div>
          </section>
        )}

        {tab === 'contact' && (
          <section className="contact-section">
            <h2>Contact</h2>
            <div className="contact-card">
              <div><strong>Email:</strong> staff-support@skeduler.example</div>
              <div><strong>Phone:</strong> +1 (555) 123-4567</div>
              <div><strong>Office:</strong> Room 204, Department Block</div>
            </div>
          </section>
        )}

      </main>

      <Footer />
    </div>
  );
}

export default StaffPage;
