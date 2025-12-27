# Deployment to Render

This guide explains how to deploy the College Management System to Render.com (a free platform that supports Flask applications and PostgreSQL/SQLite).

## Prerequisites

- GitHub account (https://github.com)
- Render account (https://render.com) - free tier available
- Git installed locally

## Step 1: Prepare Repository

### 1.1 Create .gitignore

Create a file named `.gitignore` in your project root:
```
venv/
__pycache__/
*.pyc
.env
college_management.db
.DS_Store
instance/
*.log
```

### 1.2 Update requirements.txt

Ensure your requirements.txt is in the root directory with pinned versions:
```
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
Werkzeug==2.3.7
python-dotenv==1.0.0
Gunicorn==21.2.0
```

Gunicorn is needed for production. Test it locally:
```bash
pip install gunicorn
gunicorn app:app
```

### 1.3 Create Procfile

Create a file named `Procfile` in your project root (no extension):
```
web: gunicorn app:app
```

This tells Render how to start your app.

### 1.4 Update app.py for Production

Modify the last line of `app.py`:

```python
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    # Use environment to determine debug mode
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

Add at the top:
```python
import os
```

## Step 2: Push to GitHub

### 2.1 Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "Initial commit: College Management System"
```

### 2.2 Create GitHub Repository

1. Go to https://github.com/new
2. Create new repository (e.g., `college-management-system`)
3. Follow instructions to push your code:

```bash
git remote add origin https://github.com/YOUR_USERNAME/college-management-system.git
git branch -M main
git push -u origin main
```

## Step 3: Deploy on Render

### 3.1 Create Render Account

1. Go to https://render.com
2. Sign up (free tier available)
3. Verify email

### 3.2 Create New Web Service

1. Click "New +" button → "Web Service"
2. Connect GitHub (authorize if first time)
3. Select your repository
4. Fill in details:
   - **Name**: `college-management` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free (good for testing)

### 3.3 Set Environment Variables

Before deploying, click "Environment" and add:

```
FLASK_ENV=production
SECRET_KEY=your-random-secret-key-here
DATABASE_URL=sqlite:///college_management.db
```

Generate a secure SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 3.4 Deploy

1. Click "Create Web Service"
2. Render will build and deploy automatically
3. Check "Logs" tab for deployment progress
4. Once successful, you'll get a URL like: `https://college-management.onrender.com`

## Step 4: Initial Setup on Render

Once deployed:

### 4.1 Create Admin Account

Use curl or Postman to create admin:
```bash
curl -X POST https://your-app-url.onrender.com/api/admin/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@college.edu",
    "password": "secure-password-here",
    "name": "Administrator"
  }'
```

Or create a Python script locally that connects to Render:

```python
import requests

url = "https://your-app-url.onrender.com/api/admin/register"
data = {
    "email": "admin@college.edu",
    "password": "secure-password-here",
    "name": "Administrator"
}
response = requests.post(url, json=data)
print(response.json())
```

### 4.2 Access Application

Open your browser:
```
https://college-management.onrender.com
```

You should see the home page.

## Step 5: Post-Deployment

### 5.1 Security Checklist

- [ ] Changed SECRET_KEY to a secure random value
- [ ] Set FLASK_ENV to production
- [ ] Changed default admin password
- [ ] Tested admin and staff login
- [ ] Verified database is working
- [ ] Checked logs for errors

### 5.2 Add Staff and Timetable

1. Login as admin at your Render URL
2. Add test staff members
3. Create timetable entries
4. Test staff login

### 5.3 Monitor Application

In Render dashboard:
- Check "Logs" for errors
- Monitor "Metrics" tab
- Set up email alerts for failures

## Step 6: Updating Your Application

When you make changes:

1. Test locally first:
   ```bash
   python app.py
   ```

2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Feature: Add new functionality"
   git push origin main
   ```

3. Render automatically redeploys within minutes

## Database on Render

### Important Notes

- **SQLite on Render**: SQLite data persists between deployments BUT:
  - Free tier can restart without notice
  - Data might be lost on tier changes
  - Not ideal for production

- **Better for Production**: Use PostgreSQL (Render offers free tier)
  
### Upgrading to PostgreSQL (Optional)

1. In Render dashboard, click "New +" → "PostgreSQL"
2. Create database with:
   - Name: `college_management`
   - User: `postgres`
   - Region: Same as your web service
3. Copy the Internal Database URL
4. Update web service environment variable:
   ```
   DATABASE_URL=postgresql://...
   ```
5. Modify `app.py` to use PostgreSQL:
   ```python
   import os
   DB_URL = os.environ.get('DATABASE_URL')
   if DB_URL.startswith('postgres://'):
       DB_URL = DB_URL.replace('postgres://', 'postgresql://', 1)
   app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
   ```

## Troubleshooting Render Deployment

### Build Fails

Check "Logs" tab:
- Missing requirements? Add to requirements.txt
- Python version? Render uses Python 3 by default
- Syntax errors? The logs will show exact line numbers

### App Crashes After Deploy

1. Check logs in Render dashboard
2. Common issues:
   - Missing environment variables
   - Database connection string wrong
   - Import errors

### Database Not Found

- SQLite file is created automatically on first run
- Give it 1-2 minutes after first deploy

### Port Issues

- Render automatically assigns a PORT env variable
- The code handles this: `port=int(os.environ.get('PORT', 5000))`

## Performance Optimization

### For Free Tier

- Expected response time: 1-3 seconds (cold start)
- After traffic: Response time < 500ms
- Database: Keep queries simple and indexed

### Cost

- **Free Tier**: Limited free hours per month
- **Paid Tiers**: Start from $7/month
- Current app uses minimal resources (suitable for free tier)

## Backup Data

Since SQLite can be lost on Render free tier:

### Manual Backup

```bash
# Download from Render file system (requires SSH)
# Or use periodic exports via API
```

### Recommended: Use PostgreSQL

Render's PostgreSQL free tier is more reliable for production.

## Custom Domain (Optional)

1. In Render dashboard, go to "Settings"
2. Add custom domain
3. Update DNS records (instructions in Render)
4. HTTPS is automatic

## Monitoring & Alerts

1. Set up Email Alerts:
   - Dashboard → Settings → Notifications
2. Monitor these metrics:
   - CPU usage
   - Memory usage
   - Build failures
   - Deploy frequency

## Going Live Checklist

- [ ] Domain configured (if using custom domain)
- [ ] Admin account created
- [ ] Test data added
- [ ] Admin and staff login tested
- [ ] Leave application tested
- [ ] Rescheduling verified
- [ ] Backup strategy in place
- [ ] Monitoring alerts enabled

## Support

- Render Docs: https://docs.render.com
- Render Community: https://community.render.com
- Flask Deployment: https://flask.palletsprojects.com/deployment/

---

Your College Management System is now live on the internet!
