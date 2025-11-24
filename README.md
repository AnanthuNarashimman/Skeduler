# 📅 Skeduler - Automated Timetable Generation System

<div align="center">

![Skeduler Banner](https://img.shields.io/badge/Skeduler-Timetable%20Automation-4a8bc2?style=for-the-badge)

**An intelligent timetable scheduling system for educational institutions**

[![Live Demo](https://img.shields.io/badge/Demo-Live-success?style=flat-square)](https://skeduler-git-development-ananthunarashimmans-projects.vercel.app)
[![React](https://img.shields.io/badge/React-19.2.0-61dafb?style=flat-square&logo=react)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-Python-000000?style=flat-square&logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)

</div>

---

## 🌟 Overview

**Skeduler** is a comprehensive web-based timetable management system designed to automate and simplify the complex process of scheduling classes for educational institutions. Built with modern technologies, it offers an intuitive interface for administrators to create, manage, and distribute optimized timetables efficiently.

### ✨ Key Highlights

- 🤖 **Automated Schedule Generation** - Upload Excel data and generate conflict-free timetables instantly
- 📊 **Smart Optimization Engine** - AI-powered algorithm ensures optimal resource allocation
- 🎨 **Modern UI/UX** - Clean, responsive design with smooth animations
- 💾 **Persistent Storage** - SQLite database for reliable data management
- 📥 **Export Capabilities** - Download timetables as CSV files
- 🚀 **Demo Mode** - Try the system without authentication

---

## 🎯 Features

### 🔧 Core Functionality

#### 1. **Timetable Creation**
- Upload department data via Excel files
- Automated schedule generation with conflict detection
- Real-time processing and optimization
- Save/Cancel confirmation before database storage
- Support for multiple classes and sections

#### 2. **Timetable Management**
- View all created timetables in card-based gallery
- Individual class timetable display
- Modal view for detailed schedule inspection
- Delete all timetables with confirmation dialog
- Filter and search capabilities

#### 3. **Dashboard Analytics**
- Real-time timetable count statistics
- Quick access to all features
- Clean, organized action cards
- Coming soon features preview

#### 4. **Contact System**
- Integrated contact modal in navbar
- Email client integration with pre-filled templates
- Quick support access from any page

### 🎨 Design Features

- **Responsive Layout** - Works seamlessly on desktop, tablet, and mobile
- **Smooth Animations** - GSAP-powered transitions and interactions
- **Consistent Branding** - Playfair Display + Inter font pairing
- **Blue Gradient Theme** - Professional color scheme (#6ba3d8 to #4a8bc2)
- **Dotted Background Pattern** - Subtle radial gradient texture

---

## 🛠️ Tech Stack

### Frontend
```
React 19.2.0          - UI Framework
React Router 7.9.6    - Client-side routing
Axios 1.13.2          - HTTP client
GSAP 3.13.0           - Animation library
React Icons 5.5.0     - Icon components
Vite 7.2.2            - Build tool & dev server
```

### Backend
```
Flask                 - Python web framework
SQLite3               - Database
CORS                  - Cross-origin support
Excel Parser          - Custom Excel processing
Optimization Engine   - Scheduling algorithm
```

### Database Schema
```sql
timetables table:
- id (PRIMARY KEY)
- department (TEXT)
- semester (TEXT)
- academic_year (TEXT)
- schedule_data (JSON)
- created_at (TIMESTAMP)
- updated_at (TIMESTAMP)
- is_active (BOOLEAN)

timetable_metadata table:
- id (PRIMARY KEY)
- timetable_id (FOREIGN KEY)
- total_classes (INTEGER)
- file_name (TEXT)
- created_by (TEXT)
```

---

## 📁 Project Structure

```
Skeduler/
├── backend/
│   ├── app.py                 # Flask application & API routes
│   ├── database.py            # SQLite database operations
│   ├── engine.py              # Optimization algorithm
│   ├── excel_parser.py        # Excel file processing
│   ├── test_database.py       # Database testing
│   ├── data.json              # Configuration data
│   ├── timetable.db           # SQLite database
│   └── uploads/               # Temporary file storage
│
├── skeduler/
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── admin/
│   │   │   ├── AdminDashboard.jsx      # Main dashboard
│   │   │   ├── AdminDashboard.css
│   │   │   ├── AdminNavbar.jsx         # Navigation bar
│   │   │   ├── AdminNavbar.css
│   │   │   ├── StaffDirectory.jsx
│   │   │   └── StaffDirectory.css
│   │   │
│   │   ├── Components/
│   │   │   ├── Benefits.jsx            # Landing page sections
│   │   │   ├── CTA.jsx
│   │   │   ├── Features.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── LandHero.jsx
│   │   │   ├── Navbar.jsx
│   │   │   ├── Problem.jsx
│   │   │   └── Solution.jsx
│   │   │
│   │   ├── ComponentStyles/            # Component-specific CSS
│   │   │
│   │   ├── Pages/
│   │   │   ├── CreateTimetable.jsx     # Timetable creation page
│   │   │   ├── LandingPage.jsx         # Public landing page
│   │   │   ├── ViewTimetables.jsx      # Timetable gallery
│   │   │   └── Test.jsx
│   │   │
│   │   ├── PageStyles/                 # Page-specific CSS
│   │   │   ├── Create.css
│   │   │   ├── LandingPage.css
│   │   │   ├── ViewTimetables.css
│   │   │   └── Test.css
│   │   │
│   │   ├── assets/
│   │   │   └── Images/                 # Image assets
│   │   │
│   │   ├── App.jsx                     # Main app component
│   │   ├── App.css
│   │   └── main.jsx                    # Entry point
│   │
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── vercel.json                     # Deployment config
│   └── eslint.config.js
│
├── DATABASE_SETUP.md
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.8 or higher)
- **npm** or **yarn**
- **pip** (Python package manager)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/AnanthuNarashimman/Skeduler.git
cd Skeduler
```

#### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install flask flask-cors openpyxl

# Initialize database
python database.py

# Run Flask server
python app.py
```

Backend will run on `http://localhost:5000`

#### 3. Frontend Setup
```bash
cd skeduler

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:5173`

---

## 🎮 Usage Guide

### Creating a Timetable

1. **Navigate to Create Timetable** from the dashboard
2. **Upload Excel File** containing:
   - Class information (e.g., III-A, III-B)
   - Subject details
   - Faculty assignments
   - Lab schedules
   - Period configurations
3. **Click Generate** to process the schedule
4. **Review** the generated timetable
5. **Save or Cancel** based on your requirements

### Excel File Format

Your Excel file should contain sheets with the following structure:
- Classes sheet: Class names and sections
- Subjects sheet: Subject codes and names
- Faculty sheet: Staff assignments
- Labs sheet: Laboratory periods
- Configuration: Period timings and working days

### Managing Timetables

1. Go to **View Timetables** page
2. Browse all saved timetables in card format
3. Click any card to view detailed schedule
4. Download timetables as CSV files
5. Delete all timetables when needed (with confirmation)

### Deleting Timetables

- Use the **Delete All** button (appears when timetables exist)
- Confirmation modal prevents accidental deletions
- Shows count of timetables being deleted

---

## 🔌 API Endpoints

### Timetable Operations

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/upload-schedule` | Upload Excel and generate timetable |
| `POST` | `/api/save-timetable` | Save generated timetable to database |
| `GET` | `/api/timetables` | Retrieve all timetables |
| `GET` | `/api/timetable/<id>` | Get specific timetable by ID |
| `DELETE` | `/api/timetable/<id>` | Delete single timetable |
| `DELETE` | `/api/timetables/delete-all` | Delete all timetables |
| `GET` | `/api/health` | Server health check |

### Request/Response Examples

#### Upload Schedule
```javascript
POST /api/upload-schedule
Content-Type: multipart/form-data

{
  file: <Excel File>
}

Response:
{
  "status": "success",
  "schedule_data": { ... },
  "metadata": { ... }
}
```

#### Save Timetable
```javascript
POST /api/save-timetable
Content-Type: application/json

{
  "schedule_data": { ... },
  "department": "CSE",
  "semester": "III-A",
  "academic_year": "2024-25"
}

Response:
{
  "status": "success",
  "message": "Successfully saved 2 class timetables",
  "timetable_ids": [1, 2]
}
```

---

## 🎨 Design System

### Color Palette
```css
Primary Blue:     #6ba3d8
Secondary Blue:   #4a8bc2
Text Dark:        #1a1a1a
Text Medium:      #666666
Text Light:       #475569
Background:       #ffffff
Success:          #10b981
Warning:          #f59e0b
Error:            #ef4444
```

### Typography
```css
Headings:   'Playfair Display', serif (400-900)
Body:       'Inter', sans-serif (300-900)
Code:       monospace
```

### Spacing Scale
```
4px   8px   12px   16px   20px   24px   32px   40px   60px   80px
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
python test_database.py
```

### Frontend Development
```bash
cd skeduler
npm run dev      # Development server
npm run build    # Production build
npm run preview  # Preview production build
```

---

## 📦 Deployment

### Frontend (Vercel)

The frontend is deployed on Vercel with automatic deployments from the `development` branch.

**Live URL:** [https://skeduler-git-development-ananthunarashimmans-projects.vercel.app](https://skeduler-nu.vercel.app/)

```bash
# Deploy to Vercel
cd skeduler
npm run build
vercel --prod
```

### Backend Deployment

For production, consider:
- **Heroku** - Easy Python deployment
- **Railway** - Modern hosting platform
- **PythonAnywhere** - Python-specific hosting
- **AWS EC2** - Scalable cloud infrastructure

#### Environment Variables
```env
FLASK_ENV=production
DATABASE_URL=sqlite:///timetable.db
CORS_ORIGINS=https://your-frontend-domain.com
```

---

## 🗺️ Roadmap

### ✅ Completed Features
- [x] Automated timetable generation
- [x] Excel file upload and parsing
- [x] SQLite database integration
- [x] View timetables gallery
- [x] Individual class cards
- [x] CSV export functionality
- [x] Delete all timetables
- [x] Save/Cancel confirmation
- [x] Contact modal
- [x] Demo mode (no login)
- [x] Responsive design
- [x] Admin dashboard
- [x] Coming soon modals

### 🚧 Coming Soon
- [ ] Staff management system
- [ ] Announcement creation
- [ ] User authentication
- [ ] Multi-department support
- [ ] Edit existing timetables
- [ ] Conflict resolution interface
- [ ] Email notifications
- [ ] PDF export
- [ ] Dark mode
- [ ] Mobile app

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow existing code style and conventions
- Write clear commit messages
- Test your changes thoroughly
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Ananthu Narashimman**

- GitHub: [@AnanthuNarashimman](https://github.com/AnanthuNarashimman)
- Project: [Skeduler Repository](https://github.com/AnanthuNarashimman/Skeduler)

---

## 🙏 Acknowledgments

- React team for the amazing framework
- Flask community for excellent documentation
- GSAP for powerful animation library
- Vercel for seamless deployment
- All contributors and users

---

## 📞 Support

For support, questions, or feedback:

- 📧 Use the contact modal in the application
- 🐛 Open an issue on GitHub
- 💬 Start a discussion in the repository

---

## 📊 Project Stats

![GitHub Stars](https://img.shields.io/github/stars/AnanthuNarashimman/Skeduler?style=social)
![GitHub Forks](https://img.shields.io/github/forks/AnanthuNarashimman/Skeduler?style=social)
![GitHub Issues](https://img.shields.io/github/issues/AnanthuNarashimman/Skeduler)
![GitHub Pull Requests](https://img.shields.io/github/issues-pr/AnanthuNarashimman/Skeduler)

---

<div align="center">

**Made with ❤️ for Educational Institutions**

⭐ Star this repo if you find it helpful!

[🌐 Visit Live Demo](https://skeduler-git-development-ananthunarashimmans-projects.vercel.app) • [📖 Documentation](https://github.com/AnanthuNarashimman/Skeduler/wiki) • [🐛 Report Bug](https://github.com/AnanthuNarashimman/Skeduler/issues)

</div>
