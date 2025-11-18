# System Architecture - Online Assignment Submission System

## Overview

This document describes the technical architecture of the Online Assignment Submission System.

---

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         USERS                                │
│  (Students, Instructors, Administrators)                     │
└─────────────────┬───────────────────────────────────────────┘
                  │ HTTP/HTTPS
                  │
┌─────────────────▼───────────────────────────────────────────┐
│                    WEB BROWSER                               │
│  (Chrome, Firefox, Safari, Edge - All Modern Browsers)       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  │ HTTP Requests
                  │
┌─────────────────▼───────────────────────────────────────────┐
│              FLASK WEB SERVER                                │
│  - Route Handling                                            │
│  - Session Management                                        │
│  - Request Processing                                        │
│  - Response Generation                                       │
└─────────────┬───────────────┬──────────────┬────────────────┘
              │               │              │
              │               │              │
    ┌─────────▼─────┐  ┌─────▼─────┐  ┌────▼──────┐
    │   Templates   │  │  Database  │  │   Upload  │
    │   (HTML)      │  │  (SQLite)  │  │   Folder  │
    └───────────────┘  └────────────┘  └───────────┘
```

---

## Components

### 1. Frontend Layer

**Technologies:**
- HTML5
- CSS3 (Custom styling)
- JavaScript (Form validation, interactivity)

**Pages (Templates):**
```
├── base.html                 # Master template
├── index.html               # Landing page
├── login.html               # Authentication
├── register.html            # User registration
│
├── Student Portal
│   ├── student_dashboard.html
│   └── submit_assignment.html
│
├── Instructor Portal
│   ├── instructor_dashboard.html
│   ├── create_assignment.html
│   ├── view_submissions.html
│   └── grade_submission.html
│
└── Admin Portal
    ├── admin_dashboard.html
    └── create_course.html
```

**Design Features:**
- Responsive design (mobile, tablet, desktop)
- Intuitive navigation
- Color-coded status indicators
- Modern gradient aesthetics
- Accessibility compliant

---

### 2. Backend Layer (Flask Application)

**Main Application: `app.py`**

**Core Modules:**

```python
Flask Framework
├── Route Handlers (20+ routes)
│   ├── Authentication routes
│   ├── Student routes
│   ├── Instructor routes
│   └── Admin routes
│
├── Database Functions
│   ├── get_db() - Database connections
│   └── init_db() - Database initialization
│
├── Security Functions
│   ├── Password hashing
│   ├── Session management
│   └── File validation
│
└── Utility Functions
    ├── File upload handling
    ├── allowed_file()
    └── secure_filename()
```

**Key Routes:**

**Public Routes:**
- `/` - Home page
- `/login` - User authentication
- `/register` - New user registration
- `/logout` - Session termination

**Student Routes:**
- `/student/dashboard` - View assignments
- `/student/submit/<id>` - Submit assignment
- `/download/<id>` - Download submission

**Instructor Routes:**
- `/instructor/dashboard` - Instructor overview
- `/instructor/create_assignment` - Create new assignment
- `/instructor/view_submissions/<id>` - View submissions
- `/instructor/grade/<id>` - Grade submission

**Admin Routes:**
- `/admin/dashboard` - System overview
- `/admin/create_course` - Create new course

---

### 3. Database Layer

**Technology:** SQLite (Embedded database)

**Schema:**

```sql
┌─────────────────┐
│     users       │
├─────────────────┤
│ id (PK)         │
│ username        │
│ password        │ (hashed)
│ full_name       │
│ email           │
│ role            │ (student/instructor/admin)
│ department      │
│ student_id      │
└─────────────────┘
        │
        │ instructor_id (FK)
        ▼
┌─────────────────┐
│    courses      │
├─────────────────┤
│ id (PK)         │
│ course_code     │
│ course_name     │
│ department      │
│ instructor_id   │ (FK → users.id)
└─────────────────┘
        │
        │ course_id (FK)
        ▼
┌─────────────────┐
│  assignments    │
├─────────────────┤
│ id (PK)         │
│ title           │
│ description     │
│ course_id       │ (FK → courses.id)
│ due_date        │
│ total_marks     │
│ created_at      │
└─────────────────┘
        │
        │ assignment_id (FK)
        ▼
┌─────────────────┐
│  submissions    │
├─────────────────┤
│ id (PK)         │
│ assignment_id   │ (FK → assignments.id)
│ student_id      │ (FK → users.id)
│ file_path       │
│ submitted_at    │
│ grade           │
│ feedback        │
│ status          │
└─────────────────┘
```

**Relationships:**
- One instructor → Many courses
- One course → Many assignments
- One assignment → Many submissions
- One student → Many submissions

---

### 4. File Storage Layer

**Structure:**
```
uploads/
├── {user_id}_{assignment_id}_{timestamp}_{filename}.pdf
├── {user_id}_{assignment_id}_{timestamp}_{filename}.docx
└── ...
```

**Features:**
- Unique filename generation
- Timestamp-based organization
- Secure file naming (sanitization)
- Size limitation (16MB default)
- Type validation (PDF, DOC, DOCX, TXT, ZIP)

---

## Data Flow

### Student Submitting Assignment

```
1. Student logs in
   │
   ├→ Session created
   │
2. Views dashboard
   │
   ├→ Query database for assignments
   ├→ Join with submissions table
   │
3. Clicks "Submit Assignment"
   │
   ├→ Load assignment details
   │
4. Uploads file
   │
   ├→ Validate file type
   ├→ Validate file size
   ├→ Generate unique filename
   ├→ Save to uploads folder
   ├→ Create database record
   │
5. Confirmation displayed
```

### Instructor Grading Submission

```
1. Instructor logs in
   │
   ├→ Session created
   │
2. Views assignments
   │
   ├→ Query database for their courses
   │
3. Clicks "View Submissions"
   │
   ├→ Query all submissions for assignment
   ├→ Join with user data
   │
4. Downloads student work
   │
   ├→ Retrieve file path from database
   ├→ Send file to browser
   │
5. Enters grade and feedback
   │
   ├→ Update submission record
   │
6. Student sees grade on dashboard
```

---

## Security Architecture

### Authentication & Authorization

```
┌──────────────────┐
│  User Login      │
└────────┬─────────┘
         │
         ├→ Username validation
         ├→ Password verification (hashed)
         │
         ├→ If valid:
         │  ├→ Create session
         │  ├→ Store user_id
         │  ├→ Store role
         │  └→ Redirect to dashboard
         │
         └→ If invalid:
            └→ Show error message
```

**Role-Based Access Control:**

```
Student Role:
├── ✅ View assignments
├── ✅ Submit assignments
├── ✅ View own grades
└── ❌ Cannot grade
└── ❌ Cannot create assignments

Instructor Role:
├── ✅ View own courses
├── ✅ Create assignments
├── ✅ View submissions
├── ✅ Grade assignments
└── ❌ Cannot access admin panel

Admin Role:
├── ✅ Full system access
├── ✅ Create courses
├── ✅ Manage users
└── ✅ View all statistics
```

### Data Security

**Password Security:**
- Hashed using Werkzeug (PBKDF2-based)
- Salt automatically applied
- Never stored in plain text

**SQL Injection Prevention:**
- Parameterized queries throughout
- No string concatenation in SQL
- SQLite Row Factory for safe data access

**File Upload Security:**
- Type validation (whitelist approach)
- Filename sanitization (secure_filename)
- Size limits enforced
- Isolated storage directory

**Session Security:**
- Secure session cookies
- Secret key for signing
- Automatic expiration

---

## Deployment Architecture

### Development Environment
```
Local Machine
├── Python 3.8+
├── Flask Development Server
├── SQLite Database
└── Local File Storage
```

### Production Environment (Cloud)

**Option 1: Render.com**
```
Render Platform
├── Python Container
├── Gunicorn WSGI Server (4 workers)
├── Persistent Disk
│   ├── SQLite Database
│   └── Upload Folder
├── HTTPS (automatic SSL)
└── Custom Domain Support
```

**Option 2: PythonAnywhere**
```
PythonAnywhere Platform
├── Python Environment
├── WSGI Configuration
├── Static Files Serving
└── Database + Files in user space
```

**Option 3: School Server**
```
Ubuntu Server
├── Nginx (Reverse Proxy)
│   └── Port 80/443 → 5000
├── Gunicorn (Application Server)
│   └── Python Flask App
├── Systemd Service (Auto-restart)
└── File System
    ├── SQLite Database
    └── Upload Folder
```

---

## Performance Considerations

### Database Optimization
- Indexes on frequently queried fields
- Foreign key constraints for integrity
- Efficient JOIN operations
- Connection pooling (via get_db())

### File Handling
- Streaming for large files
- Secure filename generation
- Direct file serving (not through Flask)
- Size limits prevent memory issues

### Scalability Options

**Current Capacity:**
- Hundreds of concurrent users
- Thousands of submissions
- Gigabytes of file storage

**Future Scaling:**
```
Database:
└── SQLite → PostgreSQL/MySQL

File Storage:
└── Local → AWS S3/Google Cloud Storage

Web Server:
└── Single instance → Multiple instances + Load Balancer

Cache:
└── None → Redis/Memcached

Queue:
└── None → Celery for async tasks
```

---

## Error Handling

### Application Level
```python
try:
    # Database operations
except sqlite3.Error:
    # Handle database errors
    # Flash message to user
    # Log error

try:
    # File operations
except IOError:
    # Handle file errors
    # Inform user
    # Log error
```

### User Level
- Flash messages for user feedback
- Form validation (client & server side)
- Graceful error pages
- Helpful error messages

---

## API Endpoints Summary

| Endpoint | Method | Auth Required | Role | Purpose |
|----------|--------|---------------|------|---------|
| `/` | GET | No | All | Home page |
| `/login` | GET, POST | No | All | Authentication |
| `/register` | GET, POST | No | All | Registration |
| `/logout` | GET | Yes | All | Logout |
| `/student/dashboard` | GET | Yes | Student | View assignments |
| `/student/submit/<id>` | GET, POST | Yes | Student | Submit work |
| `/instructor/dashboard` | GET | Yes | Instructor | View overview |
| `/instructor/create_assignment` | GET, POST | Yes | Instructor | Create assignment |
| `/instructor/view_submissions/<id>` | GET | Yes | Instructor | View submissions |
| `/instructor/grade/<id>` | GET, POST | Yes | Instructor | Grade work |
| `/admin/dashboard` | GET | Yes | Admin | System overview |
| `/admin/create_course` | GET, POST | Yes | Admin | Create course |
| `/download/<id>` | GET | Yes | Student/Instructor | Download file |

---

## Monitoring & Logging

**Built-in Logging:**
- Flask development server logs
- Database operations logged
- File upload logs
- Error tracking

**Production Logging:**
```python
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

---

## Backup Strategy

**Recommended Backup:**
```bash
# Database backup
cp assignment_system.db assignment_system_backup_$(date +%Y%m%d).db

# Files backup
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/

# Automated daily backups (cron job)
0 2 * * * /path/to/backup_script.sh
```

---

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Backend | Python | 3.8+ | Application logic |
| Web Framework | Flask | 3.0.0 | Web server |
| Database | SQLite | 3.x | Data storage |
| WSGI Server | Gunicorn | 21.2.0 | Production server |
| Frontend | HTML5/CSS3 | - | User interface |
| Security | Werkzeug | 3.0.1 | Password hashing |

---

## System Requirements

**Minimum:**
- Python 3.8+
- 512MB RAM
- 1GB disk space
- Modern web browser

**Recommended:**
- Python 3.11+
- 1GB RAM
- 5GB disk space
- Fast internet connection

---

## Maintenance

**Regular Tasks:**
- Database backup (daily)
- Monitor disk space
- Check application logs
- Update dependencies (monthly)
- Test backup restoration (quarterly)

**Updates:**
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Test after updates
python app.py
# Visit application, test functionality
```

---

## Future Enhancements

**Possible Additions:**
- Email notifications
- Real-time notifications
- Advanced analytics dashboard
- Bulk file download
- Assignment templates
- Plagiarism detection
- Mobile app
- API for integrations
- Advanced search
- Report generation

---

**This architecture provides a solid foundation for a production-ready assignment management system.**
