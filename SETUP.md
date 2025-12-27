# Detailed Setup Instructions

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 512MB minimum (1GB recommended)
- **Disk Space**: 500MB free space
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

## Step-by-Step Installation

### 1. Install Python

**Windows:**
- Download from https://www.python.org/downloads/
- Run installer with "Add Python to PATH" checked
- Verify: Open Command Prompt and run `python --version`

**macOS:**
```bash
# Using Homebrew
brew install python3
python3 --version
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
python3 --version
```

### 2. Setup in VS Code

1. Open VS Code
2. Install Python extension (Microsoft)
3. Install Pylance extension (Microsoft)
4. Open your project folder
5. Select Python interpreter (Ctrl+Shift+P → "Python: Select Interpreter")

### 3. Clone/Download Project

**Using Git:**
```bash
git clone <repository-url>
cd college-management-system
```

**Manual Download:**
- Download ZIP from repository
- Extract to a folder
- Open folder in VS Code

### 4. Create Virtual Environment

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` prefix in terminal when active.

### 5. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Configure Environment

The `.env` file is already configured for local development:
```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///college_management.db
```

**For production, change SECRET_KEY** to a random string.

### 7. Initialize Database

**Option A: Auto-initialize (recommended)**
Just start the app - database creates automatically.

**Option B: Manual initialization**
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### 8. Create Admin Account

**Method 1: Python Script**
Create a file called `setup_admin.py`:
```python
from app import app, db, Admin

def setup():
    with app.app_context():
        # Check if admin exists
        if Admin.query.filter_by(email="admin@college.edu").first():
            print("Admin already exists!")
            return
        
        admin = Admin(
            email="admin@college.edu",
            name="System Administrator"
        )
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
        print("✓ Admin created successfully!")
        print("Email: admin@college.edu")
        print("Password: admin123")
        print("\n⚠️  Change password after first login!")

if __name__ == "__main__":
    setup()
```

Run it:
```bash
python setup_admin.py
```

**Method 2: Using curl**
After starting the app:
```bash
curl -X POST http://localhost:5000/api/admin/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@college.edu",
    "password": "admin123",
    "name": "System Administrator"
  }'
```

### 9. Start the Application

```bash
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 10. Access the Application

Open browser and go to:
```
http://localhost:5000
```

You should see the home page with "Admin Login" and "Staff Login" buttons.

## First-Time Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Admin account created
- [ ] App running (`python app.py`)
- [ ] Can access http://localhost:5000
- [ ] Admin login works
- [ ] Database file created (college_management.db)

## Adding Test Data

### Create Test Staff Members

After login as admin:

1. Go to Staff Management
2. Add test staff:
   - Employee ID: EMP001, Name: John Doe, Email: john@college.edu, Dept: Computer Science, Pos: Assistant Professor
   - Employee ID: EMP002, Name: Jane Smith, Email: jane@college.edu, Dept: Mathematics, Pos: Professor
   - Employee ID: EMP003, Name: Bob Johnson, Email: bob@college.edu, Dept: Physics, Pos: Lecturer

### Create Sample Timetable

1. Go to Timetable Management
2. Add schedules:
   - John Doe: CS101 (Data Structures), Monday 09:00-10:30, Room A101
   - Jane Smith: MATH201 (Calculus), Tuesday 10:30-12:00, Room B201
   - John Doe: CS102 (Database), Wednesday 14:00-15:30, Room A102

### Test Leave Application

1. Login as staff (john@college.edu / default123)
2. Go to "Apply for Leave"
3. Select a Monday date, choose "Sick Leave", submit
4. Admin will see the leave request and auto-assigned rescheduling
5. Admin can approve or override the assignment

## Stopping the Application

- In terminal: Press `Ctrl+C`
- The app will shut down gracefully
- Database persists between runs

## File Explanations

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with all routes and logic |
| `requirements.txt` | Python package dependencies |
| `.env` | Environment configuration |
| `public/index.html` | Home page |
| `public/admin-login.html` | Admin login |
| `public/staff-login.html` | Staff login |
| `public/admin-dashboard.html` | Admin control panel |
| `public/staff-dashboard.html` | Staff interface |
| `college_management.db` | SQLite database (created automatically) |

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Activate virtual environment and install requirements:
```bash
# Activate venv first
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Issue: "Address already in use"
**Solution**: Port 5000 is occupied. Either:
- Stop other Flask apps
- Change port in `app.py`: `app.run(port=5001)`

### Issue: Database locked error
**Solution**: 
- Close other instances of the app
- Delete `college_management.db` and restart (fresh database)

### Issue: Login page loads but login doesn't work
**Solution**:
1. Check browser console (F12) for errors
2. Verify app is running (`python app.py` in terminal)
3. Check that POST request goes to `http://localhost:5000/api/admin/login`
4. Verify database has admin account

### Issue: Blank page or "404 Not Found"
**Solution**:
- Make sure `public/` folder exists with HTML files
- Restart Flask app
- Clear browser cache (Ctrl+Shift+Delete)

## Next Steps

1. Customize the system as needed
2. Follow DEPLOYMENT.md to deploy to Render
3. Set up regular database backups
4. Change all default passwords in production
5. Configure proper logging and monitoring

## Getting Help

1. Check console for error messages (F12 in browser)
2. Check terminal for Flask errors
3. Verify database connectivity
4. Check file permissions in project folder
5. Ensure ports are not blocked by firewall

---

You're all set! Start with the admin account and explore the features.
