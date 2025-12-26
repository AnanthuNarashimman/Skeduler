# 📅 Skeduler

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-4+-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![OR-Tools](https://img.shields.io/badge/OR--Tools-9.8-4285F4?style=for-the-badge&logo=google&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://skeduler-git-development-ananthunarashimmans-projects.vercel.app)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**An intelligent automated timetable scheduling system powered by constraint optimization**

[Live Demo](https://skeduler-git-development-ananthunarashimmans-projects.vercel.app) • [Report Bug](../../issues) • [Request Feature](../../issues)

</div>

---

## 🌟 Features

### 🎯 Core Functionality
- **Automated Timetable Generation**: Upload Excel files and generate optimized schedules using Google OR-Tools CP-SAT solver
- **Smart Constraint Management**: Handles complex scheduling rules including labs, tutorials, integrated labs, and lectures
- **Staff Conflict Resolution**: Automatically prevents teacher double-booking across multiple classes
- **Elective Synchronization**: Groups elective subjects to ensure simultaneous scheduling
- **Merged Class Support**: Links VI_SEM A & B sections for shared subjects

### 👨‍💼 Admin Features
- **Excel File Upload**: Parse and process department timetable data
- **Interactive Preview**: View generated schedules before saving
- **Staff Directory Management**: Manage teacher information and credentials
- **Multiple Class Scheduling**: Generate timetables for all semesters simultaneously

### 👨‍🏫 Teacher Features
- **Personalized Dashboard**: Teachers can view their individual schedules
- **Secure Authentication**: Role-based login system with JWT tokens
- **Profile Management**: View and update personal information
- **Timetable Visualization**: Clean, color-coded schedule display

### 🎨 User Interface
- **Color-Coded Periods**: Visual distinction between labs (orange), integrated labs (green), tutorials (blue)
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Modern UI/UX**: Clean, professional interface with smooth animations

---

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**: Core programming language
- **Flask**: Lightweight web framework for API endpoints
- **Google OR-Tools**: Constraint programming solver for schedule optimization
- **SQLite**: Database for storing timetables and user data
- **Pandas & openpyxl**: Excel file processing
- **JWT**: Secure authentication tokens
- **bcrypt**: Password hashing

### Frontend
- **React 18**: Modern UI library with hooks
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client for API calls
- **React Router**: Client-side routing
- **CSS3**: Custom styling with gradients and animations

### Deployment
- **Vercel**: Frontend hosting and serverless functions
- **Git**: Version control

---

## 📁 Project Structure

```
Skeduler/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── engine.py              # Timetable generation algorithm
│   ├── database.py            # Database operations
│   ├── auth.py                # Authentication logic
│   ├── excel_parser.py        # Excel file parsing
│   ├── requirements.txt       # Python dependencies
│   └── uploads/               # Uploaded Excel files
│
├── skeduler/
│   ├── src/
│   │   ├── admin/             # Admin dashboard components
│   │   │   ├── AdminDashboard.jsx
│   │   │   ├── AdminNavbar.jsx
│   │   │   └── StaffDirectory.jsx
│   │   ├── Pages/
│   │   │   ├── CreateTimetable.jsx    # Timetable generation UI
│   │   │   ├── ViewTimetables.jsx     # View saved schedules
│   │   │   ├── LandingPage.jsx        # Public homepage
│   │   │   └── Teacher/               # Teacher portal
│   │   │       ├── TeacherDashboard.jsx
│   │   │       ├── TeacherLogin.jsx
│   │   │       ├── TeacherProfile.jsx
│   │   │       └── TeacherTimetableView.jsx
│   │   ├── Components/        # Reusable UI components
│   │   ├── contexts/          # React context providers
│   │   └── main.jsx           # App entry point
│   ├── public/                # Static assets
│   ├── package.json           # Node dependencies
│   └── vite.config.js         # Vite configuration
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Node.js 16 or higher
- npm or yarn

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Skeduler/backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**
   ```bash
   python app.py
   ```
   Server runs on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd ../skeduler
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```
   App runs on `http://localhost:5173`

---

## 📖 Usage

### For Administrators

1. **Login** to the admin dashboard
2. **Navigate** to "Create Timetable"
3. **Upload** your Excel file containing:
   - Class schedules
   - Subject assignments
   - Staff information
   - Lab/Tutorial details
4. **Generate** the optimized schedule
5. **Review** the generated timetables
6. **Save** to database (replaces previous schedules)

### For Teachers

1. **Login** with credentials
2. **View** your personalized timetable
3. **Check** schedule for any day/period
4. **Update** profile information

---

## 🧩 Schedule Generation Algorithm

The system uses **Google OR-Tools CP-SAT Solver** with the following constraints:

### Hard Constraints
- ✅ Normal Labs: 3-hour blocks (P2-P4 or P5-P7), once per week
- ✅ Integrated Labs: 2-hour blocks, once per week
- ✅ Tutorials: 2-hour blocks, once per week
- ✅ Lectures: 3-5 hours per week, single periods
- ✅ Staff cannot be in multiple classes simultaneously
- ✅ Classes cannot have multiple subjects in the same period
- ✅ Electives scheduled simultaneously across sections

### Soft Constraints (Optimized)
- 📈 Maximize schedule diversity (different subjects per day)
- 📉 Minimize consecutive identical subjects
- 📉 Reduce same-day repetition

### Objective Function
```
Maximize: (100 × allocation) + (50 × diversity) - (20 × penalties)
```

---

## 🎨 Color Coding

| Type | Color | Description |
|------|-------|-------------|
| 🟠 **Labs** | Orange | 3-hour laboratory sessions |
| 🟢 **Integrated Labs** | Green | 2-hour integrated practical sessions |
| 🔵 **Tutorials** | Blue | 2-hour tutorial classes |
| ⚪ **Lectures** | White | Standard theory classes |
| 🌫️ **Free** | Gray | Unscheduled periods |

---

## 🔌 API Endpoints

### Timetable Generation
```http
POST /api/upload-schedule
Content-Type: multipart/form-data

Request: Excel file upload
Response: { status: "success", schedule: {...} }
```

### Save Timetable
```http
POST /api/save-timetable
Content-Type: application/json

Request: { schedule_data, department, file_name, academic_year }
Response: { status: "success" }
```

### Authentication
```http
POST /api/teacher/login
Content-Type: application/json

Request: { email, password }
Response: { token, teacher_data }
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License.

---

## 👥 Team

Developed with ❤️ by the Skeduler Team

---

## 🔗 Links

- **Production**: [Skeduler App](https://skeduler-git-development-ananthunarashimmans-projects.vercel.app)
- **Development Branch**: Active development happens here
- **Issues**: [Report bugs or request features](../../issues)

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with 🧠 constraint optimization and ☕

</div>
