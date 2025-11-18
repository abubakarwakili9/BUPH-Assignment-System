# 🚀 Quick Start - Assignment System

## ⚡ Get Started in 5 Minutes!

### Step 1: Run the Application
```bash
# Option A: Using start script (Linux/Mac)
./start.sh

# Option B: Manual (All platforms)
pip install -r requirements.txt
python app.py
```

### Step 2: Open in Browser
Go to: **http://localhost:5000**

### Step 3: Login
- Username: **admin**
- Password: **admin123**

---

## 📁 What You Have

```
assignment-system/
├── 📄 README.md              - Complete documentation
├── 📄 DEPLOYMENT.md          - Deployment guide (Render, PythonAnywhere, etc.)
├── 📄 USER_GUIDE.md          - How to use the system
├── 📄 QUICK_START.md         - This file
│
├── 🐍 app.py                 - Main application
├── 📋 requirements.txt        - Python dependencies
├── 🚀 start.sh               - Quick start script
├── 📦 Procfile               - For Heroku/Render deployment
│
├── 📂 templates/             - All HTML pages
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student_dashboard.html
│   ├── submit_assignment.html
│   ├── instructor_dashboard.html
│   ├── create_assignment.html
│   ├── view_submissions.html
│   ├── grade_submission.html
│   ├── admin_dashboard.html
│   └── create_course.html
│
└── 📂 static/
    └── css/
        └── style.css         - All styling
```

---

## 🎯 Key Features

✅ **Students**
- Submit assignments online
- Track grades and feedback
- Resubmit if needed

✅ **Instructors**
- Create assignments
- Grade submissions
- Provide feedback

✅ **Admins**
- Manage courses
- Manage users
- View statistics

---

## 🌐 Deploy to Cloud (FREE)

### Render.com (Recommended)
1. Push code to GitHub
2. Connect to Render
3. Deploy automatically
4. Get free subdomain

**Time:** ~10 minutes
**Guide:** See DEPLOYMENT.md

### PythonAnywhere
1. Upload files
2. Install dependencies
3. Configure web app
4. Get username.pythonanywhere.com

**Time:** ~15 minutes
**Guide:** See DEPLOYMENT.md

---

## 📚 Next Steps

1. ✅ Test locally first
2. ✅ Read USER_GUIDE.md
3. ✅ Deploy to cloud (DEPLOYMENT.md)
4. ✅ Change admin password
5. ✅ Create courses and start using!

---

## 🔧 Quick Troubleshooting

**Can't install dependencies?**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Port already in use?**
Edit `app.py`, change port from 5000 to 8000

**Database issues?**
```bash
rm assignment_system.db
python -c "from app import init_db; init_db()"
```

---

## 📞 Need Help?

1. Check **README.md** for detailed docs
2. Read **USER_GUIDE.md** for usage
3. See **DEPLOYMENT.md** for deployment
4. Review code comments in `app.py`

---

## 🎉 You're Ready!

This is a complete, production-ready application.
Just deploy and start using!

**Default Login:**
- Username: `admin`
- Password: `admin123`

⚠️ **Remember to change the password after first login!**

---

*Built for Binyaminu Usman Polytechnic, Hadejia*
