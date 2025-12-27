# API Testing Examples

Quick reference for testing the College Management System API endpoints using curl or Postman.

## Base URL

**Local:** `http://localhost:5000`
**Render:** `https://your-app.onrender.com`

## Authentication

### Admin Registration

```bash
curl -X POST http://localhost:5000/api/admin/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@college.edu",
    "password": "admin123",
    "name": "Administrator"
  }'
```

### Admin Login

```bash
curl -X POST http://localhost:5000/api/admin/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "admin@college.edu",
    "password": "admin123"
  }'
```

### Staff Login

```bash
curl -X POST http://localhost:5000/api/staff/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{
    "email": "john@college.edu",
    "password": "default123"
  }'
```

### Check Session

```bash
curl -X GET http://localhost:5000/api/session \
  -b cookies.txt
```

### Logout

```bash
# Admin
curl -X POST http://localhost:5000/api/admin/logout \
  -b cookies.txt

# Staff
curl -X POST http://localhost:5000/api/staff/logout \
  -b cookies.txt
```

## Staff Management

### Get All Staff

```bash
curl -X GET http://localhost:5000/api/admin/staff \
  -b cookies.txt
```

### Add Staff Member

```bash
curl -X POST http://localhost:5000/api/admin/staff \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "employee_id": "EMP001",
    "name": "John Doe",
    "email": "john@college.edu",
    "department": "Computer Science",
    "position": "Assistant Professor",
    "phone": "9876543210",
    "password": "john123"
  }'
```

### Update Staff

```bash
curl -X PUT http://localhost:5000/api/admin/staff/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "name": "John Smith",
    "email": "john.smith@college.edu",
    "department": "Engineering",
    "position": "Professor",
    "phone": "9876543211",
    "is_active": true
  }'
```

### Deactivate Staff

```bash
curl -X DELETE http://localhost:5000/api/admin/staff/1 \
  -b cookies.txt
```

## Timetable Management

### Get All Timetables

```bash
curl -X GET http://localhost:5000/api/admin/timetable \
  -b cookies.txt
```

### Add Class Schedule

```bash
curl -X POST http://localhost:5000/api/admin/timetable \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "staff_id": 1,
    "course_code": "CS101",
    "course_name": "Data Structures",
    "day": "Monday",
    "time_slot": "09:00-10:30",
    "room": "A101",
    "batch": "B1"
  }'
```

### Update Timetable Entry

```bash
curl -X PUT http://localhost:5000/api/admin/timetable/1 \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "staff_id": 1,
    "course_code": "CS101",
    "course_name": "Data Structures (Updated)",
    "day": "Tuesday",
    "time_slot": "10:30-12:00",
    "room": "A102",
    "batch": "B1"
  }'
```

### Delete Timetable Entry

```bash
curl -X DELETE http://localhost:5000/api/admin/timetable/1 \
  -b cookies.txt
```

### Get Staff Timetable (As Staff Member)

```bash
curl -X GET http://localhost:5000/api/staff/timetable \
  -b cookies.txt
```

## Leave Management

### Apply for Leave (As Staff)

```bash
curl -X POST http://localhost:5000/api/staff/leave/apply \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "leave_date": "2024-12-25",
    "leave_type": "casual",
    "reason": "Family event"
  }'
```

### Get Pending Leave Requests

```bash
curl -X GET http://localhost:5000/api/admin/leave/pending \
  -b cookies.txt
```

### Approve Leave

```bash
curl -X POST http://localhost:5000/api/admin/leave/1/approve \
  -b cookies.txt
```

### Reject Leave

```bash
curl -X POST http://localhost:5000/api/admin/leave/1/reject \
  -b cookies.txt
```

## Class Rescheduling

### Get Rescheduling Records

```bash
curl -X GET http://localhost:5000/api/admin/rescheduling \
  -b cookies.txt
```

### Override Class Assignment

```bash
curl -X POST http://localhost:5000/api/admin/rescheduling/1/override \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "assigned_staff_id": 2
  }'
```

## Reports & Statistics

### Get Staff Count

```bash
curl -X GET http://localhost:5000/api/admin/stats/staff-count \
  -b cookies.txt
```

Response:
```json
{
  "total_staff": 5,
  "active_staff": 3
}
```

### Get Login Activity

```bash
curl -X GET http://localhost:5000/api/admin/stats/login-activity \
  -b cookies.txt
```

### Get Leave & Attendance Report

```bash
# All staff
curl -X GET http://localhost:5000/api/admin/leave-presence \
  -b cookies.txt

# Specific staff
curl -X GET "http://localhost:5000/api/admin/leave-presence?staff_id=1" \
  -b cookies.txt
```

## Using Postman

1. **Create Environment Variables:**
   - Set `base_url` = `http://localhost:5000`
   - Set `token` = (auto-set after login)

2. **Use in requests:**
   ```
   {{base_url}}/api/admin/staff
   ```

3. **Add Pre-request Script** for login:
   ```javascript
   // Auto-login before each request
   const loginRequest = {
     url: pm.environment.get("base_url") + "/api/admin/login",
     method: "POST",
     header: "Content-Type: application/json",
     body: {
       mode: "raw",
       raw: JSON.stringify({
         email: "admin@college.edu",
         password: "admin123"
       })
     }
   };
   ```

## Python Script Examples

### Automated Testing

```python
import requests
import json

BASE_URL = "http://localhost:5000"
session = requests.Session()

# Login
login_response = session.post(
    f"{BASE_URL}/api/admin/login",
    json={
        "email": "admin@college.edu",
        "password": "admin123"
    }
)
print("Login Status:", login_response.status_code)

# Get staff
staff_response = session.get(f"{BASE_URL}/api/admin/staff")
print("Staff Count:", len(staff_response.json()["staff"]))

# Add staff
new_staff = session.post(
    f"{BASE_URL}/api/admin/staff",
    json={
        "employee_id": "EMP999",
        "name": "Test Staff",
        "email": "test@college.edu",
        "department": "Testing",
        "position": "Test",
        "password": "test123"
    }
)
print("Add Staff Status:", new_staff.status_code)

# Logout
session.post(f"{BASE_URL}/api/admin/logout")
```

### Bulk Staff Import

```python
import requests
import csv

BASE_URL = "http://localhost:5000"
session = requests.Session()

# Login
session.post(
    f"{BASE_URL}/api/admin/login",
    json={
        "email": "admin@college.edu",
        "password": "admin123"
    }
)

# Read from CSV and add staff
with open('staff_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        response = session.post(
            f"{BASE_URL}/api/admin/staff",
            json=row
        )
        status = "✓" if response.status_code == 201 else "✗"
        print(f"{status} {row['name']}")

session.post(f"{BASE_URL}/api/admin/logout")
```

### Bulk Timetable Import

```python
import requests
import csv

BASE_URL = "http://localhost:5000"
session = requests.Session()

# Login
session.post(
    f"{BASE_URL}/api/admin/login",
    json={"email": "admin@college.edu", "password": "admin123"}
)

# Get staff mapping
staff_response = session.get(f"{BASE_URL}/api/admin/staff")
staff_map = {s['name']: s['id'] for s in staff_response.json()['staff']}

# Read from CSV and add timetable
with open('timetable_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        response = session.post(
            f"{BASE_URL}/api/admin/timetable",
            json={
                "staff_id": staff_map[row['staff_name']],
                "course_code": row['course_code'],
                "course_name": row['course_name'],
                "day": row['day'],
                "time_slot": row['time_slot'],
                "room": row['room'],
                "batch": row.get('batch', '')
            }
        )
        status = "✓" if response.status_code == 201 else "✗"
        print(f"{status} {row['course_code']}")

session.post(f"{BASE_URL}/api/admin/logout")
```

## CSV File Format Examples

### staff_data.csv
```
employee_id,name,email,department,position,phone,password
EMP001,John Doe,john@college.edu,CS,Assistant Professor,9876543210,john123
EMP002,Jane Smith,jane@college.edu,MATH,Professor,9876543211,jane123
EMP003,Bob Johnson,bob@college.edu,PHYS,Lecturer,9876543212,bob123
```

### timetable_data.csv
```
staff_name,course_code,course_name,day,time_slot,room,batch
John Doe,CS101,Data Structures,Monday,09:00-10:30,A101,B1
Jane Smith,MATH201,Calculus,Tuesday,10:30-12:00,B201,B2
John Doe,CS102,Database,Wednesday,14:00-15:30,A102,B1
```

## Common Response Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | GET request successful |
| 201 | Created | Resource created (POST/PUT) |
| 400 | Bad Request | Invalid data format |
| 401 | Unauthorized | Not logged in |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Backend error |

## Error Response Format

```json
{
  "error": "Invalid credentials"
}
```

or 

```json
{
  "message": "Operation successful",
  "resource_id": 1
}
```

---

**Tip:** Save cookies.txt to a secure location and regenerate regularly.
