# Online Assignment Submission System

A complete web-based assignment management system for Binyaminu Usman Polytechnic, Hadejia.

## Features

### For Students
- 📤 Submit assignments online from anywhere
- 📊 Track assignment status and grades
- 💬 Receive feedback from instructors
- 🔄 Resubmit assignments if needed

### For Instructors
- 📝 Create and manage assignments
- 📥 View and download student submissions
- ✍️ Grade assignments and provide feedback
- 📚 Manage multiple courses

### For Administrators
- 👥 Manage users (students and instructors)
- 📚 Create and assign courses
- 📊 View system statistics
- 🔧 System oversight

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easy to deploy, no setup needed)
- **Frontend**: HTML5, CSS3, JavaScript
- **File Storage**: Local file system

## Installation & Setup

### Local Development

1. **Clone or download the project**
   ```bash
   cd assignment-system
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and go to: `http://localhost:5000`

### Default Admin Account
- **Username**: admin
- **Password**: admin123
- ⚠️ **Important**: Change this password after first login!

## Quick Start Guide

### For Students
1. Register a new account (select "Student" role)
2. Login with your credentials
3. View available assignments on your dashboard
4. Click "Submit Assignment" to upload your work
5. Check back for grades and feedback

### For Instructors
1. Register a new account (select "Instructor" role)
2. Contact admin to be assigned to courses
3. Create assignments for your courses
4. View submissions and grade student work
5. Provide detailed feedback

### For Administrators
1. Login with admin credentials
2. Create courses and assign instructors
3. Monitor system usage and statistics
4. Manage users if needed

## Deployment Options

### Option 1: Deploy on Render (Recommended - FREE)

1. **Create a Render account** at https://render.com

2. **Create a new Web Service**
   - Connect your GitHub repository (or upload files)
   - Choose "Python" as the environment
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Add environment variables** (optional)
   - `SECRET_KEY`: Your secret key for sessions

4. **Deploy!** Render will automatically deploy your app

### Option 2: Deploy on PythonAnywhere (FREE)

1. **Create account** at https://www.pythonanywhere.com

2. **Upload your files** using the Files tab

3. **Install requirements** in a Bash console:
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Configure Web App**
   - Go to Web tab
   - Add a new web app (Flask)
   - Point to your `app.py` file
   - Set working directory

5. **Reload** your web app

### Option 3: Deploy on Heroku

1. **Install Heroku CLI** and login

2. **Create a Procfile**:
   ```
   web: gunicorn app:app
   ```

3. **Deploy**:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Option 4: Deploy on Local Server (e.g., School Server)

1. **Install Python 3.8+** on the server

2. **Copy project files** to the server

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. **Run with Gunicorn**:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

5. **Use a reverse proxy** (nginx recommended) for production

## Project Structure

```
assignment-system/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── assignment_system.db        # SQLite database (auto-created)
├── uploads/                    # Student submissions (auto-created)
├── templates/                  # HTML templates
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
└── static/
    └── css/
        └── style.css           # Styling
```

## Configuration

### Change Secret Key (Production)
Edit `app.py` and change:
```python
app.secret_key = 'your-secret-key-change-this-in-production'
```

### Change Upload Limits
Edit `app.py`:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Allowed File Types
Edit `app.py`:
```python
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'zip'}
```

## Security Considerations

✅ **Implemented:**
- Password hashing using Werkzeug
- File upload validation
- Session management
- SQL injection protection (parameterized queries)

⚠️ **For Production:**
- Change default admin password immediately
- Use strong secret key
- Enable HTTPS
- Implement rate limiting
- Regular backups of database
- Secure file storage

## Troubleshooting

### Database Not Found
The database is created automatically on first run. If you have issues:
```bash
python -c "from app import init_db; init_db()"
```

### Permission Errors
Ensure the uploads directory is writable:
```bash
chmod 755 uploads/
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8000)
```

## Support & Contact

For issues or questions:
- Review the documentation
- Check the troubleshooting section
- Contact system administrator

## License

This project is developed for Binyaminu Usman Polytechnic, Hadejia.

## Acknowledgments

Developed to streamline assignment submission and management at BUPH, eliminating paper-based processes and improving efficiency for both students and instructors.
