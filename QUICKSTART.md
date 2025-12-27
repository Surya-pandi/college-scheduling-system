# Quick Start Guide - College Management System

Get your college management system running in 5 minutes!

## Prerequisites

- Python 3.8+
- Any modern web browser

## 5-Minute Setup

### 1. Download & Extract
- Download/clone the project
- Extract to a folder
- Open in VS Code (optional but helpful)

### 2. Setup Python Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database & Create Admin
```bash
python setup_admin.py
```

You'll see:
```
✓ Admin created successfully!
Email: admin@college.edu
Password: admin123
```

### 5. Start the Server
```bash
python app.py
```

Open http://localhost:5000 in your browser.

## First Login

1. Click "Admin Login"
2. Email: `admin@college.edu`
3. Password: `admin123`
4. Change password immediately!

## Quick Next Steps

1. **Add Staff Members**
   - Staff Management → Add Staff Member
   - Fill in details and assign password

2. **Create Timetable**
   - Timetable Management → Add Class Schedule
   - Assign staff, set day/time/room

3. **Test Staff Login**
   - Use staff email and password
   - View assigned timetable
   - Apply for leave

4. **Approve Leaves**
   - Go to Leave Approvals
   - System auto-assigns replacement staff
   - Approve or override assignment

## Deployment (Optional)

Ready to go live? Follow `DEPLOYMENT.md` to deploy to Render for free.

---

**Troubleshooting?** See SETUP.md for detailed installation help.

**Questions?** Check the README.md for full documentation.
