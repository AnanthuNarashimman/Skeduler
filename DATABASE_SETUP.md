# Skeduler - Database Setup

## Overview
This project now includes a SQLite database integration to store generated timetables persistently.

## Database Schema

### Tables

#### 1. `timetables`
Main table storing timetable data:
- `id` - Primary key (auto-increment)
- `department` - Department name (e.g., CSE)
- `semester` - Semester information
- `academic_year` - Academic year
- `schedule_data` - JSON string of the complete schedule
- `created_at` - Timestamp of creation
- `updated_at` - Timestamp of last update
- `is_active` - Status flag (1=active, 0=deleted)

#### 2. `timetable_metadata`
Additional metadata for timetables:
- `id` - Primary key
- `timetable_id` - Foreign key to timetables table
- `total_classes` - Number of classes in the timetable
- `total_subjects` - Number of subjects
- `file_name` - Original uploaded file name
- `created_by` - User who created the timetable

## API Endpoints

### 1. Upload and Generate Schedule
**POST** `/api/upload-schedule`
- Upload Excel file and generate timetable
- Returns generated schedule

### 2. Save Timetable
**POST** `/api/save-timetable`
```json
{
  "schedule_data": { ... },
  "department": "CSE",
  "semester": "Sem 1",
  "academic_year": "2024-2025",
  "file_name": "schedule.xlsx"
}
```

### 3. Get All Timetables
**GET** `/api/timetables?department=CSE&limit=50`
- Retrieve all saved timetables
- Optional filters: department, limit

### 4. Get Single Timetable
**GET** `/api/timetable/<id>`
- Retrieve specific timetable by ID

### 5. Delete Timetable
**DELETE** `/api/timetable/<id>`
- Soft delete (marks as inactive)

## User Flow

1. **Admin Dashboard** → Click "Create Timetable" button
2. **Create Timetable Page** → Upload Excel file
3. **Generate** → System processes and displays schedule
4. **Review** → User reviews the generated timetable
5. **Confirmation Dialog** → User chooses to Save or Cancel
6. **Save** → Timetable is saved to database
7. **Success** → User sees confirmation message

## Frontend Features

### Enhanced UI
- Gradient backgrounds and modern styling
- Animated transitions and hover effects
- Confirmation dialog for save action
- Loading spinners during operations
- Success/Error messages with visual feedback

### Navigation
- AdminDashboard integrates with routing
- "Create" button navigates to CreateTimetable page
- AdminNavbar for consistent navigation

## Setup Instructions

### 1. Backend Setup
```bash
cd backend
python database.py  # Initialize database
python app.py       # Start Flask server
```

### 2. Frontend Setup
```bash
cd skeduler
npm install
npm run dev         # Start development server
```

### 3. Test Database
```bash
cd backend
python test_database.py
```

## Database Location
- File: `backend/timetable.db`
- Type: SQLite3
- Initialized automatically on first run

## Future Enhancements
- User authentication
- Edit existing timetables
- Export to PDF
- Manage multiple semesters
- View timetable history
- Conflict detection and resolution
