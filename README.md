# College Management System with Automatic Staff Scheduling

A comprehensive web-based platform for managing college staff scheduling, leave applications, attendance tracking, and automatic class rescheduling. Built with Flask (Python) backend and responsive HTML/CSS frontend.

## Features

### Admin Portal
- **Staff Management**: Add, edit, view, and deactivate staff members
- **Timetable Management**: Create and manage class schedules with support for manual entry and CSV import
- **Leave Approvals**: Review and approve/reject leave applications
- **Automatic Rescheduling**: System automatically assigns alternative staff when someone applies for leave
- **Rescheduling Override**: Admin can manually override auto-assigned staff
- **Login Activity Monitoring**: Track all user logins and logouts with timestamps
- **Dashboard Statistics**: View total staff, active users, pending leaves, and rescheduled classes
- **Attendance & Presence Reports**: Filter and view staff leave and attendance data

### Staff Portal
- **View Timetable**: See assigned classes organized by day and time
- **Apply for Leave**: Submit leave requests with reasons
- **Leave History**: Track leave application status (pending, approved, rejected)
- **Dashboard**: Quick statistics and today's classes overview

### System Features
- **Secure Authentication**: Role-based login with password hashing (bcrypt)
- **Session Management**: Secure HTTP-only cookies with session timeout
- **SQLite Database**: Persistent storage for all data - runs locally and on Render
- **Auto-Rescheduling**: When staff apply for leave, the system:
  - Finds all classes on that day
  - Detects available alternative staff without schedule conflicts
  - Automatically assigns replacement staff
  - Allows admin to override assignments
- **Responsive Design**: Mobile-friendly interface across all devices
- **Access Control**: Role-based authorization (Admin/Staff)

## Project Structure

```
college-management-system/
├── app.py                          # Flask backend with all API routes
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── public/                        # Frontend HTML files
│   ├── index.html                # Home/landing page
│   ├── admin-login.html          # Admin login portal
│   ├── staff-login.html          # Staff login portal
│   ├── admin-dashboard.html      # Admin dashboard with all features
│   ├── staff-dashboard.html      # Staff portal
│   └── college_management.db     # SQLite database (auto-created)
├── README.md                      # This file
├── SETUP.md                       # Detailed setup instructions
└── DEPLOYMENT.md                  # Render deployment guide
```

## Quick Start (Local Development)

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- VS Code (optional, but recommended)

### Installation Steps

1. **Clone/Download Project**
   ```bash
   # If using git
   git clone <repository-url>
   cd college-management-system
   
   # Or extract the downloaded ZIP file
   ```

2. **Create Virtual Environment** (Recommended)
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   # The database will be auto-created when you start the app
   # But you can pre-create it by running:
   python -c "from app import app, db; app.app_context().push(); db.create_all()"
   ```

5. **Start the Application**
   ```bash
   python app.py
   ```
   
   The server will start at `http://localhost:5000`

6. **Access the Application**
   - Open your browser and go to `http://localhost:5000`
   - Click "Admin Login" or "Staff Login"

## Default Admin Account (Create on First Run)

The system comes with an initial registration endpoint. Create an admin account:

**Using API (Postman or curl):**
```bash
curl -X POST http://localhost:5000/api/admin/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@college.edu",
    "password": "admin123",
    "name": "Admin User"
  }'
```

Or via Python script:
```python
from app import app, db, Admin

with app.app_context():
    admin = Admin(
        email="admin@college.edu",
        name="Admin User"
    )
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    print("Admin created successfully!")
```

## Adding Initial Data

### Add Staff Members
1. Login as Admin
2. Go to "Staff Management"
3. Click "Add Staff Member"
4. Fill in the form with employee ID, name, email, department, position, phone
5. Default password is "default123" (change on first login)

### Create Timetable
1. In Admin Dashboard, go to "Timetable Management"
2. Click "Add Class Schedule"
3. Select staff member and fill in:
   - Course Code (e.g., CS101)
   - Course Name (e.g., Data Structures)
   - Day (Monday-Saturday)
   - Time Slot (e.g., 09:00-10:30)
   - Room (e.g., Room A101)
   - Batch (optional, e.g., B1)

## Database Schema

### Users
- **Admin**: Admin user accounts for system management
- **Staff**: Staff/faculty member accounts

### Scheduling
- **Timetable**: Class schedules with staff assignments
- **Leave**: Leave applications with approval status
- **ClassRescheduling**: Automatic and manual staff reassignments for leave coverage
- **Attendance**: Attendance records and login tracking
- **LoginLog**: Security audit trail of all logins/logouts

## API Endpoints Summary

### Admin Endpoints
- `POST /api/admin/register` - Register new admin
- `POST /api/admin/login` - Admin login
- `POST /api/admin/logout` - Admin logout
- `GET /api/admin/staff` - Get all staff
- `POST /api/admin/staff` - Add staff member
- `PUT /api/admin/staff/<id>` - Update staff
- `DELETE /api/admin/staff/<id>` - Deactivate staff
- `GET /api/admin/timetable` - Get all timetables
- `POST /api/admin/timetable` - Add timetable entry
- `PUT /api/admin/timetable/<id>` - Update timetable
- `DELETE /api/admin/timetable/<id>` - Delete timetable
- `GET /api/admin/leave/pending` - Get pending leave requests
- `POST /api/admin/leave/<id>/approve` - Approve leave
- `POST /api/admin/leave/<id>/reject` - Reject leave
- `GET /api/admin/stats/staff-count` - Get staff statistics
- `GET /api/admin/stats/login-activity` - Get login logs
- `GET /api/admin/leave-presence` - Get attendance report
- `GET /api/admin/rescheduling` - Get rescheduling records
- `POST /api/admin/rescheduling/<id>/override` - Override class assignment

### Staff Endpoints
- `POST /api/staff/login` - Staff login
- `POST /api/staff/logout` - Staff logout
- `GET /api/staff/timetable` - Get personal timetable
- `POST /api/staff/leave/apply` - Apply for leave
- `GET /api/admin/leave-presence` - View personal attendance

### Common Endpoints
- `GET /api/session` - Get current session info

## Security Features

- **Password Hashing**: Uses Werkzeug security (bcrypt-based)
- **Session Management**: Secure HTTP-only cookies, configurable timeout
- **CORS Protection**: Credentials required for cross-origin requests
- **Role-Based Access Control**: Separate admin and staff endpoints
- **Input Validation**: All inputs validated before processing
- **Login Audit Trail**: All login/logout events logged with IP addresses

## Deployment to Render

See `DEPLOYMENT.md` for detailed Render deployment instructions.

Quick summary:
1. Push code to GitHub
2. Create new Web Service on Render
3. Connect GitHub repository
4. Set environment variables
5. Deploy

## Troubleshooting

### Port Already in Use
```bash
# Find and kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Database Issues
Delete `college_management.db` and restart - it will auto-create with fresh schema

### CORS Errors
Ensure you're using `credentials: 'include'` in fetch requests (already done in provided code)

### Login Redirects
Check browser console (F12) for specific error messages

## Performance Tips

- Use the staff filter on Attendance page for large datasets
- Archive old timetables to keep database lean
- Monitor login activity regularly for suspicious access

## Support & Documentation

- Backend logic: See inline comments in `app.py`
- Frontend code: See inline comments in HTML files
- Database: SQLite file at `college_management.db`

## License

This system is provided as-is for educational purposes.

## Contributors

Built with Flask, SQLAlchemy, and responsive HTML/CSS for reliable college management.
