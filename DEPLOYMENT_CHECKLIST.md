# 🚀 Deployment Checklist

Complete this checklist to successfully deploy your Online Assignment Submission System.

---

## ✅ Pre-Deployment (Local Testing)

### Phase 1: Initial Setup (5 minutes)
- [ ] Download all project files
- [ ] Ensure Python 3.8+ is installed: `python3 --version`
- [ ] Navigate to project directory: `cd assignment-system`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run application: `python app.py`
- [ ] Open browser: http://localhost:5000
- [ ] Test login with admin/admin123
- [ ] Change admin password

### Phase 2: Create Sample Data (Optional, 2 minutes)
- [ ] Run: `python create_sample_data.py`
- [ ] Login with sample instructor account
- [ ] Login with sample student account
- [ ] Test assignment submission workflow
- [ ] Test grading workflow

### Phase 3: Verify Functionality (10 minutes)
- [ ] Register new student account
- [ ] Register new instructor account
- [ ] Login as admin and create a course
- [ ] Assign instructor to course
- [ ] Login as instructor and create assignment
- [ ] Login as student and submit assignment
- [ ] Login as instructor and grade submission
- [ ] Verify student can see grade
- [ ] Test file download
- [ ] Test all dashboards

---

## 🌐 Deployment Options

Choose ONE deployment method below:

### Option A: Deploy to Render.com (Recommended)

#### Prerequisites
- [ ] GitHub account created
- [ ] Render.com account created
- [ ] Git installed on your computer

#### Steps
- [ ] Initialize git repository: `git init`
- [ ] Create .gitignore (already provided)
- [ ] Add files: `git add .`
- [ ] Commit: `git commit -m "Initial commit"`
- [ ] Create GitHub repository
- [ ] Push to GitHub: `git push origin main`
- [ ] Login to Render.com
- [ ] Click "New +" → "Web Service"
- [ ] Connect GitHub repository
- [ ] Configure:
  - [ ] Environment: Python 3
  - [ ] Build Command: `pip install -r requirements.txt`
  - [ ] Start Command: `gunicorn app:app`
  - [ ] Instance Type: Free
- [ ] Add environment variable: `SECRET_KEY` (generate random string)
- [ ] Click "Create Web Service"
- [ ] Wait for deployment (2-3 minutes)
- [ ] Test deployed URL
- [ ] Login and change admin password
- [ ] Create your first course

#### Post-Deployment
- [ ] Bookmark your application URL
- [ ] Share URL with users
- [ ] Set up regular monitoring

---

### Option B: Deploy to PythonAnywhere

#### Prerequisites
- [ ] PythonAnywhere account created (free tier)

#### Steps
- [ ] Login to PythonAnywhere
- [ ] Upload all project files via Files tab
- [ ] Open Bash console
- [ ] Navigate to project: `cd assignment-system`
- [ ] Install dependencies: `pip3.10 install --user -r requirements.txt`
- [ ] Go to Web tab
- [ ] Add new web app
- [ ] Select Flask, Python 3.10
- [ ] Configure paths:
  - [ ] Source code: `/home/USERNAME/assignment-system`
  - [ ] Working directory: `/home/USERNAME/assignment-system`
- [ ] Edit WSGI file:
```python
import sys
path = '/home/USERNAME/assignment-system'
if path not in sys.path:
    sys.path.append(path)
from app import app as application
```
- [ ] Configure static files:
  - [ ] URL: `/static/`
  - [ ] Directory: `/home/USERNAME/assignment-system/static/`
- [ ] Click "Reload" button
- [ ] Test your URL: `https://USERNAME.pythonanywhere.com`
- [ ] Login and change admin password

#### Post-Deployment
- [ ] Bookmark your application URL
- [ ] Set reminder to reload every 3 months
- [ ] Monitor CPU usage

---

### Option C: Deploy to School Server

#### Prerequisites
- [ ] Server access (SSH)
- [ ] Root or sudo privileges
- [ ] Ubuntu/Debian Linux server

#### Steps
- [ ] Connect to server: `ssh user@server-ip`
- [ ] Update system: `sudo apt update && sudo apt upgrade`
- [ ] Install Python: `sudo apt install python3 python3-pip nginx -y`
- [ ] Upload project files (via SCP or SFTP)
- [ ] Navigate to project directory
- [ ] Install dependencies: `pip3 install -r requirements.txt`
- [ ] Install gunicorn: `pip3 install gunicorn`
- [ ] Test application: `python3 app.py`
- [ ] Create systemd service (see DEPLOYMENT.md)
- [ ] Configure Nginx (see DEPLOYMENT.md)
- [ ] Start service: `sudo systemctl start assignment-system`
- [ ] Enable auto-start: `sudo systemctl enable assignment-system`
- [ ] Configure firewall if needed
- [ ] Test application via domain/IP

#### Optional: HTTPS
- [ ] Install certbot: `sudo apt install certbot python3-certbot-nginx`
- [ ] Get certificate: `sudo certbot --nginx -d yourdomain.com`
- [ ] Test auto-renewal: `sudo certbot renew --dry-run`

#### Post-Deployment
- [ ] Set up automated backups
- [ ] Configure monitoring
- [ ] Document server details

---

## 🔒 Security Checklist

### Immediately After Deployment
- [ ] Change default admin password (admin123)
- [ ] Update SECRET_KEY in app.py (use random string)
- [ ] Test all user roles work correctly
- [ ] Verify file uploads are secure
- [ ] Check that unauthorized access is blocked

### Production Security
- [ ] Enable HTTPS (SSL certificate)
- [ ] Set up firewall rules
- [ ] Configure rate limiting (if available)
- [ ] Restrict database file permissions
- [ ] Set up regular backups
- [ ] Keep dependencies updated
- [ ] Monitor error logs
- [ ] Set up user activity logging

---

## 📊 Post-Deployment Setup

### Create Your System Structure
- [ ] Login as admin
- [ ] Create all departments
- [ ] Create all courses with codes
- [ ] Assign instructors to courses

### User Management
- [ ] Invite instructors to register
- [ ] Provide instructor credentials
- [ ] Invite students to register
- [ ] Verify student registrations
- [ ] Create user guidelines document

### Training
- [ ] Share USER_GUIDE.md with all users
- [ ] Conduct instructor training session
- [ ] Conduct student orientation
- [ ] Create FAQs based on questions
- [ ] Set up support channel

---

## 🔄 Regular Maintenance

### Daily
- [ ] Check application is accessible
- [ ] Monitor for errors

### Weekly
- [ ] Check disk space usage
- [ ] Review user registrations
- [ ] Monitor submission volume

### Monthly
- [ ] Backup database
- [ ] Backup upload files
- [ ] Test backup restoration
- [ ] Update dependencies if needed
- [ ] Review and respond to user feedback

### Quarterly
- [ ] Full system audit
- [ ] Performance review
- [ ] Security assessment
- [ ] User satisfaction survey

---

## 📝 Documentation Checklist

- [ ] README.md - Read and understand
- [ ] DEPLOYMENT.md - Follow for your platform
- [ ] USER_GUIDE.md - Share with users
- [ ] ARCHITECTURE.md - Understand system design
- [ ] QUICK_START.md - For rapid testing

---

## 🧪 Testing Checklist

### Student Functionality
- [ ] Student can register
- [ ] Student can login
- [ ] Student can view assignments
- [ ] Student can submit files (PDF, DOCX, ZIP)
- [ ] Student can see submission status
- [ ] Student can view grades
- [ ] Student can see feedback
- [ ] Student can resubmit
- [ ] Student can logout

### Instructor Functionality
- [ ] Instructor can register
- [ ] Instructor can login
- [ ] Instructor can view assigned courses
- [ ] Instructor can create assignments
- [ ] Instructor can view submissions
- [ ] Instructor can download student files
- [ ] Instructor can grade submissions
- [ ] Instructor can provide feedback
- [ ] Instructor can edit grades
- [ ] Instructor can logout

### Admin Functionality
- [ ] Admin can login
- [ ] Admin can view statistics
- [ ] Admin can create courses
- [ ] Admin can assign instructors
- [ ] Admin can view all users
- [ ] Admin can view all courses
- [ ] Admin can logout

### System Functionality
- [ ] File uploads work (all types)
- [ ] File downloads work
- [ ] Database stores data correctly
- [ ] Sessions persist correctly
- [ ] Password reset works (if implemented)
- [ ] Responsive design works on mobile
- [ ] All pages load without errors

---

## 🎯 Success Criteria

Your deployment is successful when:

✅ Application is accessible via URL
✅ All three user roles can login
✅ Assignments can be created and submitted
✅ Files upload and download successfully
✅ Grading system works end-to-end
✅ All users can perform their required tasks
✅ No major bugs or errors
✅ Users understand how to use the system
✅ Backups are configured
✅ Documentation is accessible to users

---

## 🆘 Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Can't access application | Check if server is running, check firewall |
| Login fails | Verify credentials, check database |
| File upload fails | Check uploads folder permissions, check file size |
| Database errors | Check database file exists and is writable |
| 500 errors | Check application logs, check Python version |
| Slow performance | Check server resources, optimize queries |
| Users can't register | Check database connection, check form validation |

See DEPLOYMENT.md for detailed troubleshooting.

---

## 📞 Support Resources

- [ ] Documentation folder with all guides
- [ ] Application logs for debugging
- [ ] GitHub repository (if created)
- [ ] Support contact established

---

## ✨ Optional Enhancements (Future)

Consider these improvements later:
- [ ] Email notifications
- [ ] SMS reminders for due dates
- [ ] Analytics dashboard
- [ ] Bulk operations
- [ ] API for mobile app
- [ ] Advanced search
- [ ] Report generation
- [ ] Integration with LMS

---

## 🎉 Final Steps

- [ ] Mark all checklist items complete
- [ ] Document any customizations made
- [ ] Celebrate successful deployment!
- [ ] Share feedback and improvements
- [ ] Plan user adoption strategy

---

## 📋 Deployment Summary

**Date Deployed:** _________________

**Platform Used:** _________________

**Application URL:** _________________

**Admin Credentials Changed:** Yes / No

**Backup Schedule Set:** Yes / No

**Users Trained:** Yes / No

**Status:** ☐ Testing  ☐ Production  ☐ Maintenance

**Notes:**
_________________________________________________
_________________________________________________
_________________________________________________

---

**🎓 Congratulations on deploying your Online Assignment Submission System!**

*For Binyaminu Usman Polytechnic, Hadejia*
