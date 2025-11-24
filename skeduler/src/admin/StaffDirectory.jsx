import React, { useState } from 'react';
import './StaffDirectory.css';
import AdminNavbar from './AdminNavbar';
import { FaChevronDown, FaChevronUp, FaUser, FaEnvelope, FaPhone, FaBook, FaClock, FaEdit } from 'react-icons/fa';

const StaffDirectory = () => {
  const [expandedCard, setExpandedCard] = useState(null);
  const [editModalOpen, setEditModalOpen] = useState(false);
  const [editingStaff, setEditingStaff] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    designation: '',
    email: '',
    phone: '',
    subjects: [],
    classes: []
  });

  // Mock staff data based on data.json structure
  const mockStaffData = [
    {
      id: 1,
      name: "Mr. T. Bhaskar",
      designation: "Assistant Professor",
      email: "t.bhaskar@college.edu",
      phone: "+91 98765 43210",
      subjects: ["DMS"],
      classes: ["III_SEM_A", "III_SEM_B"],
      totalClasses: 12
    },
    {
      id: 2,
      name: "Mr. B. Rajesh",
      designation: "Assistant Professor",
      email: "b.rajesh@college.edu",
      phone: "+91 98765 43211",
      subjects: ["DSA"],
      classes: ["III_SEM_A", "III_SEM_B", "III_SEM_C"],
      totalClasses: 15
    },
    {
      id: 3,
      name: "Ms. R. Keerthana",
      designation: "Assistant Professor",
      email: "r.keerthana@college.edu",
      phone: "+91 98765 43212",
      subjects: ["JP", "GM"],
      classes: ["III_SEM_A", "VII_SEM_A", "VII_SEM_B"],
      totalClasses: 18
    },
    {
      id: 4,
      name: "Mr. O.K. Gowrishankar",
      designation: "Associate Professor",
      email: "ok.gowrishankar@college.edu",
      phone: "+91 98765 43213",
      subjects: ["OSC", "DS-I", "SSD-III", "LIB_HH"],
      classes: ["III_SEM_A", "III_SEM_B", "III_SEM_C"],
      totalClasses: 20
    },
    {
      id: 5,
      name: "Ms. U. Kasthuri",
      designation: "Assistant Professor",
      email: "u.kasthuri@college.edu",
      phone: "+91 98765 43214",
      subjects: ["COA"],
      classes: ["III_SEM_A", "III_SEM_B"],
      totalClasses: 10
    },
    {
      id: 6,
      name: "Mrs. E. Baby Anitha",
      designation: "Assistant Professor",
      email: "e.babyanitha@college.edu",
      phone: "+91 98765 43215",
      subjects: ["DSA_Lab", "DS"],
      classes: ["III_SEM_A", "VII_SEM_A"],
      totalClasses: 14
    },
    {
      id: 7,
      name: "Dr. N. Mahendran",
      designation: "Professor",
      email: "n.mahendran@college.edu",
      phone: "+91 98765 43216",
      subjects: ["JP_Lab", "BI"],
      classes: ["III_SEM_B", "VII_SEM_A"],
      totalClasses: 16
    },
    {
      id: 8,
      name: "Mrs. S. Vinothini",
      designation: "Associate Professor",
      email: "s.vinothini@college.edu",
      phone: "+91 98765 43217",
      subjects: ["OSC", "OSC_Lab", "LIB_HH"],
      classes: ["III_SEM_A", "III_SEM_B"],
      totalClasses: 18
    },
    {
      id: 9,
      name: "Dr. R. Jeetendra",
      designation: "Professor",
      email: "r.jeetendra@college.edu",
      phone: "+91 98765 43218",
      subjects: ["DBMS"],
      classes: ["V_SEM_A", "V_SEM_B"],
      totalClasses: 12
    },
    {
      id: 10,
      name: "Mrs. R. Vijayalakshme",
      designation: "Associate Professor",
      email: "r.vijayalakshme@college.edu",
      phone: "+91 98765 43219",
      subjects: ["DAA"],
      classes: ["V_SEM_A", "V_SEM_B"],
      totalClasses: 14
    },
    {
      id: 11,
      name: "Dr. S. Vadivel",
      designation: "Professor",
      email: "s.vadivel@college.edu",
      phone: "+91 98765 43220",
      subjects: ["ME"],
      classes: ["V_SEM_A", "V_SEM_B"],
      totalClasses: 12
    },
    {
      id: 12,
      name: "Mr. M. Azhagesan",
      designation: "Assistant Professor",
      email: "m.azhagesan@college.edu",
      phone: "+91 98765 43221",
      subjects: ["POM"],
      classes: ["V_SEM_A", "V_SEM_B"],
      totalClasses: 10
    },
    {
      id: 13,
      name: "Mrs. J. NirmalaGandhi",
      designation: "Associate Professor",
      email: "j.nirmalagandhi@college.edu",
      phone: "+91 98765 43222",
      subjects: ["OSC", "DBMS_Lab", "CBDA", "LIB_HH"],
      classes: ["III_SEM_C", "V_SEM_A", "VII_SEM_A"],
      totalClasses: 22
    },
    {
      id: 14,
      name: "Mr. M. Namasivayam",
      designation: "Assistant Professor",
      email: "m.namasivayam@college.edu",
      phone: "+91 98765 43223",
      subjects: ["DSA", "DSA_Lab", "GM", "GM_Lab", "PW"],
      classes: ["III_SEM_B", "VII_SEM_A", "VII_SEM_B"],
      totalClasses: 24
    },
    {
      id: 15,
      name: "Dr. S. Savitha",
      designation: "Professor",
      email: "s.savitha@college.edu",
      phone: "+91 98765 43224",
      subjects: ["SOA"],
      classes: ["VII_SEM_A"],
      totalClasses: 8
    }
  ];

  const toggleCard = (id) => {
    setExpandedCard(expandedCard === id ? null : id);
  };

  const openEditModal = (staff, e) => {
    e.stopPropagation();
    setEditingStaff(staff);
    setFormData({
      name: staff.name,
      designation: staff.designation,
      email: staff.email,
      phone: staff.phone,
      subjects: staff.subjects,
      classes: staff.classes
    });
    setEditModalOpen(true);
  };

  const closeEditModal = () => {
    setEditModalOpen(false);
    setEditingStaff(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubjectsChange = (e) => {
    const value = e.target.value;
    const subjectsArray = value.split(',').map(s => s.trim()).filter(s => s);
    setFormData(prev => ({
      ...prev,
      subjects: subjectsArray
    }));
  };

  const handleClassesChange = (e) => {
    const value = e.target.value;
    const classesArray = value.split(',').map(s => s.trim()).filter(s => s);
    setFormData(prev => ({
      ...prev,
      classes: classesArray
    }));
  };

  const handleSave = (e) => {
    e.preventDefault();
    // Here you would typically send to backend
    console.log('Saving staff data:', formData);
    closeEditModal();
  };

  return (
    <>
      <AdminNavbar activePage="Staff Directory" />
      <div className="staff-directory">
        <div className="directory-header">
          <div className="department-badge">
            <span className="dept-label">Department:</span>
            <span className="dept-name">CSE</span>
          </div>
          <h1>Staff Directory</h1>
          <p className="directory-subtitle">View and manage faculty members in your department</p>
        </div>

        <div className="staff-stats">
          <div className="stat-box">
            <h3>Total Faculty</h3>
            <p className="stat-value">{mockStaffData.length}</p>
          </div>
          <div className="stat-box">
            <h3>Total Classes</h3>
            <p className="stat-value">{mockStaffData.reduce((acc, staff) => acc + staff.totalClasses, 0)}</p>
          </div>
        </div>

        <div className="staff-list">
          {mockStaffData.map((staff) => (
            <div key={staff.id} className={`staff-card ${expandedCard === staff.id ? 'expanded' : ''}`}>
              <div className="staff-card-header" onClick={() => toggleCard(staff.id)}>
                <div className="staff-basic-info">
                  <div className="staff-avatar">
                    <FaUser />
                  </div>
                  <div className="staff-details">
                    <h3 className="staff-name">{staff.name}</h3>
                    <p className="staff-designation">{staff.designation}</p>
                  </div>
                </div>
                <div className="staff-card-actions">
                  <div className="quick-stats">
                    <span className="quick-stat">
                      <FaBook className="quick-icon" />
                      {staff.subjects.length} Subjects
                    </span>
                    <span className="quick-stat">
                      <FaClock className="quick-icon" />
                      {staff.totalClasses} Classes
                    </span>
                  </div>
                  <button 
                    className="edit-button" 
                    onClick={(e) => openEditModal(staff, e)}
                    aria-label="Edit Staff"
                  >
                    <FaEdit />
                  </button>
                  <button className="expand-button" aria-label={expandedCard === staff.id ? "Collapse" : "Expand"}>
                    {expandedCard === staff.id ? <FaChevronUp /> : <FaChevronDown />}
                  </button>
                </div>
              </div>

              {expandedCard === staff.id && (
                <div className="staff-card-content">
                  <div className="contact-section">
                    <h4>Contact Information</h4>
                    <div className="contact-info">
                      <div className="contact-item">
                        <FaEnvelope className="contact-icon" />
                        <span>{staff.email}</span>
                      </div>
                      <div className="contact-item">
                        <FaPhone className="contact-icon" />
                        <span>{staff.phone}</span>
                      </div>
                    </div>
                  </div>

                  <div className="subjects-section">
                    <h4>Subjects Handled ({staff.subjects.length})</h4>
                    <div className="subjects-list">
                      {staff.subjects.map((subject, index) => (
                        <div key={index} className="subject-tag">
                          {subject}
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="classes-section">
                    <h4>Classes Assigned</h4>
                    <div className="classes-info">
                      <div className="classes-list">
                        {staff.classes.map((className, index) => (
                          <span key={index} className="class-badge">
                            {className}
                          </span>
                        ))}
                      </div>
                      <div className="total-classes">
                        <span className="classes-count">{staff.totalClasses} total classes per week</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* Edit Modal */}
        {editModalOpen && (
          <div className="modal-overlay" onClick={closeEditModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>Edit Staff Information</h2>
                <button className="modal-close" onClick={closeEditModal}>&times;</button>
              </div>
              <form onSubmit={handleSave} className="modal-form">
                <div className="form-group">
                  <label htmlFor="name">Name</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    value={formData.name}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="designation">Designation</label>
                  <select
                    id="designation"
                    name="designation"
                    value={formData.designation}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="Assistant Professor">Assistant Professor</option>
                    <option value="Associate Professor">Associate Professor</option>
                    <option value="Professor">Professor</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="phone">Phone</label>
                  <input
                    type="tel"
                    id="phone"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="subjects">Subjects (comma-separated)</label>
                  <input
                    type="text"
                    id="subjects"
                    name="subjects"
                    value={formData.subjects.join(', ')}
                    onChange={handleSubjectsChange}
                    placeholder="e.g., DMS, DSA, JP"
                    required
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="classes">Classes (comma-separated)</label>
                  <input
                    type="text"
                    id="classes"
                    name="classes"
                    value={formData.classes.join(', ')}
                    onChange={handleClassesChange}
                    placeholder="e.g., III_SEM_A, III_SEM_B"
                    required
                  />
                </div>

                <div className="modal-actions">
                  <button type="button" className="btn-cancel" onClick={closeEditModal}>
                    Cancel
                  </button>
                  <button type="submit" className="btn-save">
                    Save Changes
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </>
  );
};

export default StaffDirectory;
