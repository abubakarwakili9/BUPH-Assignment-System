# Deployment Guide - Online Assignment Submission System

This guide will help you deploy the Online Assignment Submission System quickly and easily.

## Table of Contents
1. [Quick Local Setup (5 minutes)](#quick-local-setup)
2. [Deploy to Render.com (10 minutes) - FREE](#deploy-to-render)
3. [Deploy to PythonAnywhere (15 minutes) - FREE](#deploy-to-pythonanywhere)
4. [Deploy to School Server](#deploy-to-school-server)

---

## Quick Local Setup

Perfect for testing and development.

### Requirements
- Python 3.8 or higher
- Internet connection (for first-time setup)

### Steps

**Option 1: Using the start script (Linux/Mac)**
```bash
./start.sh
```

**Option 2: Manual setup (Windows/Linux/Mac)**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
python app.py
```

**3. Open your browser**
Go to: `http://localhost:5000`

**4. Login with default admin account**
- Username: `admin`
- Password: `admin123`

⚠️ **Important**: Change the admin password after first login!

---

## Deploy to Render (FREE & Easy)

Render provides free hosting for web applications. Perfect for production use!

### Step-by-Step Instructions

#### 1. Prepare Your Files
Ensure you have:
- ✅ `app.py`
- ✅ `requirements.txt`
- ✅ `templates/` folder
- ✅ `static/` folder
- ✅ `Procfile`

#### 2. Create a GitHub Repository (if not already)
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

#### 3. Sign Up on Render
1. Go to https://render.com
2. Click "Get Started" and sign up (use GitHub account for easy integration)

#### 4. Create a New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `buph-assignment-system` (or your choice)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

#### 5. Environment Variables (Optional but recommended)
Add these in the "Environment" section:
- `PYTHON_VERSION`: 3.11.0
- `SECRET_KEY`: Generate a random string (e.g., using https://randomkeygen.com/)

#### 6. Deploy!
Click "Create Web Service"

Render will:
- Install dependencies
- Build your application
- Deploy it automatically

⏱️ **Wait 2-3 minutes** for the first deployment

#### 7. Access Your Application
You'll get a URL like: `https://buph-assignment-system.onrender.com`

### Important Notes for Render
- **Free tier sleeps after 15 minutes of inactivity** - first request may be slow
- Database and uploads persist between restarts
- Automatic deployments on every git push
- Free SSL certificate included

---

## Deploy to PythonAnywhere (FREE)

PythonAnywhere is another excellent free hosting option.

### Step-by-Step Instructions

#### 1. Sign Up
1. Go to https://www.pythonanywhere.com
2. Create a free account ("Beginner" account is sufficient)

#### 2. Upload Your Files

**Option A: Using Git**
1. Open a Bash console
2. Clone your repository:
   ```bash
   git clone YOUR_GITHUB_REPO_URL
   cd assignment-system
   ```

**Option B: Manual Upload**
1. Go to "Files" tab
2. Upload all project files
3. Maintain the folder structure

#### 3. Install Dependencies
In a Bash console:
```bash
cd ~/assignment-system  # or your project folder
pip3.10 install --user -r requirements.txt
```

#### 4. Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Flask"
4. Select Python 3.10
5. Configure:
   - **Source code**: `/home/YOUR_USERNAME/assignment-system`
   - **Working directory**: `/home/YOUR_USERNAME/assignment-system`
   - **WSGI file**: Edit it and replace with:

```python
import sys
path = '/home/YOUR_USERNAME/assignment-system'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

#### 5. Set Up Static Files
In the "Web" tab, under "Static files":
- **URL**: `/static/`
- **Directory**: `/home/YOUR_USERNAME/assignment-system/static/`

#### 6. Reload Your Web App
Click the big green "Reload" button

#### 7. Access Your Application
Your URL: `https://YOUR_USERNAME.pythonanywhere.com`

### Important Notes for PythonAnywhere
- Free accounts have limited CPU time (100 seconds/day)
- Applications sleep after 3 months of no visits
- Database size limited to 512MB on free tier
- Need to reload after code changes

---

## Deploy to School Server

If your institution has its own server, here's how to deploy there.

### Requirements
- Ubuntu/Debian server (or similar Linux)
- Root or sudo access
- Python 3.8+
- Domain name or IP address

### Installation Steps

#### 1. Connect to Your Server
```bash
ssh username@your-server-ip
```

#### 2. Install Required Software
```bash
sudo apt update
sudo apt install python3 python3-pip nginx -y
```

#### 3. Upload Your Files
```bash
# From your local machine
scp -r assignment-system/ username@your-server-ip:/home/username/
```

Or use SFTP/FileZilla to upload files.

#### 4. Install Python Dependencies
```bash
cd /home/username/assignment-system
pip3 install -r requirements.txt
pip3 install gunicorn
```

#### 5. Test the Application
```bash
python3 app.py
```
Visit `http://your-server-ip:5000`

Press Ctrl+C to stop.

#### 6. Create a Systemd Service (for auto-start)
```bash
sudo nano /etc/systemd/system/assignment-system.service
```

Add this content:
```ini
[Unit]
Description=Assignment System
After=network.target

[Service]
User=username
WorkingDirectory=/home/username/assignment-system
Environment="PATH=/home/username/.local/bin"
ExecStart=/usr/local/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable assignment-system
sudo systemctl start assignment-system
sudo systemctl status assignment-system
```

#### 7. Configure Nginx (Reverse Proxy)
```bash
sudo nano /etc/nginx/sites-available/assignment-system
```

Add this content:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or your server IP

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /home/username/assignment-system/static;
    }

    client_max_body_size 20M;
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/assignment-system /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 8. Access Your Application
Visit: `http://your-domain.com` or `http://your-server-ip`

### Optional: Enable HTTPS with Let's Encrypt
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Post-Deployment Checklist

After deploying to any platform:

- [ ] Change the default admin password
- [ ] Change the secret key in production
- [ ] Create instructor accounts
- [ ] Create courses
- [ ] Test file uploads
- [ ] Test the full workflow (student submission → instructor grading)
- [ ] Set up regular database backups
- [ ] Monitor application logs

---

## Troubleshooting

### Application Won't Start
- Check if all dependencies are installed: `pip list`
- Check Python version: `python --version` (should be 3.8+)
- Check for error messages in logs

### Database Errors
- Ensure write permissions: `chmod 755 .` in project directory
- Delete old database: `rm assignment_system.db` and restart

### File Upload Errors
- Check uploads folder exists: `mkdir uploads`
- Check permissions: `chmod 755 uploads`

### Port Already in Use
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

---

## Support

For additional help:
1. Check the main README.md
2. Review application logs
3. Contact your system administrator

---

## Quick Reference

### Default Credentials
- Username: `admin`
- Password: `admin123`

### Important Files
- `app.py` - Main application
- `requirements.txt` - Dependencies
- `assignment_system.db` - Database (auto-created)
- `uploads/` - Submitted files (auto-created)

### Useful Commands
```bash
# Start application
python app.py

# Install dependencies
pip install -r requirements.txt

# Reset database (WARNING: Deletes all data!)
rm assignment_system.db && python -c "from app import init_db; init_db()"
```
