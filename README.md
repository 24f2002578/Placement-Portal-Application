# Be-Rozgar — Placement Portal Application

A full-stack **Placement Management System** built with **Flask** that connects **Students**, **Companies**, and an **Admin** on a single platform to streamline the campus placement process — from registration and profile creation to drive management, application tracking, and final selection.

---

## Tech Stack

| Layer        | Technology                            |
| ------------ | ------------------------------------- |
| **Backend**  | Python 3, Flask                       |
| **Database** | SQLite with Flask-SQLAlchemy (ORM)    |
| **Frontend** | HTML5, CSS3, Jinja2 Templating Engine |
| **Auth**     | Session-based Authentication          |

---

## Key Features

### Authentication & Authorization
- Role-based access control with three distinct roles: **Admin**, **Student**, and **Company**.
- Session-based login/logout with form validation and flash messaging.
- Admin approval workflow — companies must be approved before they can access the portal.

### Student Module
- Complete profile management — personal details, education, skills, resume upload, LinkedIn & GitHub links.
- Browse and apply to approved & open placement drives.
- Track application status (Applied → Selected / Rejected).
- Role-aware search to discover companies and open drives.

### Company Module
- Company profile creation with HR contact, website, and description.
- Create, edit, and manage placement drives (job role, description, salary, deadline, eligibility, etc.).
- View applications received per drive and **Select / Reject** candidates.
- Drives require admin approval before going live.

### Admin Module
- Centralized dashboard with counts of registered students, companies, drives, and applications.
- Approve or reject new company registrations and placement drives.
- Blacklist / un-blacklist users to restrict portal access.
- Full search across students, companies, and drives.

### Search
- Context-aware search — results are filtered based on the logged-in user's role:
  - **Admin** → searches students, companies, and drives.
  - **Student** → searches companies and approved open drives.
  - **Company** → searches only students who have applied to their drives.

---

## Project Structure

```
Be-Rozgar/
│
├── main.py                     # Application entry point, DB init, role seeding
├── requirements.txt            # Python dependencies
│
├── controller/
│   ├── config.py               # App configuration (secret key, DB URI, upload path)
│   ├── database.py             # SQLAlchemy DB instance
│   ├── models.py               # ORM models — User, Role, StudentProfile, CompanyProfile,
│   │                           #   PlacementDrive, Application, Blacklist
│   ├── auth_routes.py          # Login, Logout, Register routes
│   └── routes.py               # All CRUD & business logic routes
│
├── templates/                  # Jinja2 HTML templates
│   ├── base.html               # Base layout
│   ├── navbar.html             # Navigation bar
│   ├── home.html               # Landing / dashboard page
│   ├── login.html              # Login form
│   ├── register.html           # Registration form
│   ├── admin_dashboard.html    # Admin panel
│   ├── student_dashboard.html  # Student panel
│   ├── company_dashboard.html  # Company panel
│   ├── approve.html            # Admin approval page (users + drives)
│   ├── drive.html              # Create new placement drive
│   ├── search.html             # Search results page
│   └── ...                     # Edit, view, and detail templates
│
└── static/
    └── student_resume/         # Uploaded resume files
```

---

## Database Schema (ER Overview)

```
User ──── 1:1 ──── StudentProfile
  │                     │
  │                     └──── * Application * ────┐
  │                                               │
  ├── 1:1 ──── CompanyProfile                     │
  │                 │                              │
  │                 └──── * PlacementDrive * ──────┘
  │
  ├── M:N ──── Role  (via UserRole junction table)
  │
  └── 1:1 ──── Blacklist
```

**6 Models:** `User`, `Role` (+ `UserRole`), `StudentProfile`, `CompanyProfile`, `PlacementDrive`, `Application`, `Blacklist`

---

## Setup & Run

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/Be-Rozgar.git
cd Be-Rozgar

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python main.py
```

The app will be available at **http://127.0.0.1:5000**

> **Default Admin Credentials**
> - Email: `24f2002578@ds.study.iitm.ac.in`
> - Password: `Admin123`

---

## Highlights

- Full CRUD operations for Students, Companies, and Placement Drives
- Resume file upload support
- Admin approval pipeline for companies and drives
- User blacklisting mechanism
- Context-aware search filtered by user role
- Flash message feedback for every user action
- Clean MVC architecture with separated concerns

---
