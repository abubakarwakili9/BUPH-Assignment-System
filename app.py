from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'zip'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    conn = sqlite3.connect('assignment_system.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT,
            student_id TEXT
        );
        
        CREATE TABLE IF NOT EXISTS courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT UNIQUE NOT NULL,
            course_name TEXT NOT NULL,
            department TEXT NOT NULL,
            instructor_id INTEGER,
            FOREIGN KEY (instructor_id) REFERENCES users (id)
        );
        
        CREATE TABLE IF NOT EXISTS assignments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            course_id INTEGER NOT NULL,
            due_date TEXT NOT NULL,
            total_marks INTEGER DEFAULT 100,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (course_id) REFERENCES courses (id)
        );
        
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            assignment_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            file_path TEXT NOT NULL,
            submitted_at TEXT DEFAULT CURRENT_TIMESTAMP,
            grade INTEGER,
            feedback TEXT,
            status TEXT DEFAULT 'submitted',
            FOREIGN KEY (assignment_id) REFERENCES assignments (id),
            FOREIGN KEY (student_id) REFERENCES users (id)
        );
    ''')
    
    # Create default admin account if not exists
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        hashed_password = generate_password_hash('admin123')
        cursor.execute("""
            INSERT INTO users (username, password, full_name, email, role, department)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('admin', hashed_password, 'System Administrator', 'admin@buph.edu.ng', 'admin', 'Administration'))
    
    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' in session:
        if session['role'] == 'student':
            return redirect(url_for('student_dashboard'))
        elif session['role'] == 'instructor':
            return redirect(url_for('instructor_dashboard'))
        else:
            return redirect(url_for('admin_dashboard'))
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            session['role'] = user['role']
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        email = request.form['email']
        role = request.form['role']
        department = request.form.get('department', '')
        student_id = request.form.get('student_id', '')
        
        hashed_password = generate_password_hash(password)
        
        try:
            conn = get_db()
            conn.execute("""
                INSERT INTO users (username, password, full_name, email, role, department, student_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (username, hashed_password, full_name, email, role, department, student_id))
            conn.commit()
            conn.close()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/student/dashboard')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    conn = get_db()
    
    # Get all available assignments
    assignments = conn.execute('''
        SELECT a.*, c.course_name, c.course_code,
               s.id as submission_id, s.grade, s.feedback, s.status
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        LEFT JOIN submissions s ON a.id = s.assignment_id AND s.student_id = ?
        ORDER BY a.due_date DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return render_template('student_dashboard.html', assignments=assignments)

@app.route('/student/submit/<int:assignment_id>', methods=['GET', 'POST'])
def submit_assignment(assignment_id):
    if 'user_id' not in session or session['role'] != 'student':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{session['user_id']}_{assignment_id}_{timestamp}_{filename}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            conn = get_db()
            # Check if already submitted
            existing = conn.execute('''
                SELECT id FROM submissions 
                WHERE assignment_id = ? AND student_id = ?
            ''', (assignment_id, session['user_id'])).fetchone()
            
            if existing:
                conn.execute('''
                    UPDATE submissions 
                    SET file_path = ?, submitted_at = CURRENT_TIMESTAMP, status = 'resubmitted'
                    WHERE id = ?
                ''', (filepath, existing['id']))
            else:
                conn.execute('''
                    INSERT INTO submissions (assignment_id, student_id, file_path)
                    VALUES (?, ?, ?)
                ''', (assignment_id, session['user_id'], filepath))
            
            conn.commit()
            conn.close()
            flash('Assignment submitted successfully!', 'success')
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid file type. Allowed types: PDF, DOC, DOCX, TXT, ZIP', 'error')
    
    conn = get_db()
    assignment = conn.execute('''
        SELECT a.*, c.course_name, c.course_code
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        WHERE a.id = ?
    ''', (assignment_id,)).fetchone()
    conn.close()
    
    return render_template('submit_assignment.html', assignment=assignment)

@app.route('/instructor/dashboard')
def instructor_dashboard():
    if 'user_id' not in session or session['role'] != 'instructor':
        return redirect(url_for('login'))
    
    conn = get_db()
    
    # Get instructor's courses
    courses = conn.execute('''
        SELECT * FROM courses WHERE instructor_id = ?
    ''', (session['user_id'],)).fetchall()
    
    # Get assignments for instructor's courses
    assignments = conn.execute('''
        SELECT a.*, c.course_name, c.course_code,
               COUNT(s.id) as submission_count
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        LEFT JOIN submissions s ON a.id = s.assignment_id
        WHERE c.instructor_id = ?
        GROUP BY a.id
        ORDER BY a.created_at DESC
    ''', (session['user_id'],)).fetchall()
    
    conn.close()
    return render_template('instructor_dashboard.html', courses=courses, assignments=assignments)

@app.route('/instructor/create_assignment', methods=['GET', 'POST'])
def create_assignment():
    if 'user_id' not in session or session['role'] != 'instructor':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        course_id = request.form['course_id']
        due_date = request.form['due_date']
        total_marks = request.form.get('total_marks', 100)
        
        conn = get_db()
        conn.execute('''
            INSERT INTO assignments (title, description, course_id, due_date, total_marks)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, course_id, due_date, total_marks))
        conn.commit()
        conn.close()
        
        flash('Assignment created successfully!', 'success')
        return redirect(url_for('instructor_dashboard'))
    
    conn = get_db()
    courses = conn.execute('''
        SELECT * FROM courses WHERE instructor_id = ?
    ''', (session['user_id'],)).fetchall()
    conn.close()
    
    return render_template('create_assignment.html', courses=courses)

@app.route('/instructor/view_submissions/<int:assignment_id>')
def view_submissions(assignment_id):
    if 'user_id' not in session or session['role'] != 'instructor':
        return redirect(url_for('login'))
    
    conn = get_db()
    
    assignment = conn.execute('''
        SELECT a.*, c.course_name, c.course_code
        FROM assignments a
        JOIN courses c ON a.course_id = c.id
        WHERE a.id = ?
    ''', (assignment_id,)).fetchone()
    
    submissions = conn.execute('''
        SELECT s.*, u.full_name, u.student_id, u.email
        FROM submissions s
        JOIN users u ON s.student_id = u.id
        WHERE s.assignment_id = ?
        ORDER BY s.submitted_at DESC
    ''', (assignment_id,)).fetchall()
    
    conn.close()
    return render_template('view_submissions.html', assignment=assignment, submissions=submissions)

@app.route('/instructor/grade/<int:submission_id>', methods=['GET', 'POST'])
def grade_submission(submission_id):
    if 'user_id' not in session or session['role'] != 'instructor':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        grade = request.form['grade']
        feedback = request.form['feedback']
        
        conn = get_db()
        conn.execute('''
            UPDATE submissions 
            SET grade = ?, feedback = ?, status = 'graded'
            WHERE id = ?
        ''', (grade, feedback, submission_id))
        conn.commit()
        
        # Get assignment_id for redirect
        submission = conn.execute('SELECT assignment_id FROM submissions WHERE id = ?', 
                                 (submission_id,)).fetchone()
        conn.close()
        
        flash('Submission graded successfully!', 'success')
        return redirect(url_for('view_submissions', assignment_id=submission['assignment_id']))
    
    conn = get_db()
    submission = conn.execute('''
        SELECT s.*, u.full_name, u.student_id, a.title, a.total_marks
        FROM submissions s
        JOIN users u ON s.student_id = u.id
        JOIN assignments a ON s.assignment_id = a.id
        WHERE s.id = ?
    ''', (submission_id,)).fetchone()
    conn.close()
    
    return render_template('grade_submission.html', submission=submission)

@app.route('/download/<int:submission_id>')
def download_file(submission_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    conn = get_db()
    submission = conn.execute('SELECT file_path FROM submissions WHERE id = ?', 
                             (submission_id,)).fetchone()
    conn.close()
    
    if submission and os.path.exists(submission['file_path']):
        return send_file(submission['file_path'], as_attachment=True)
    
    flash('File not found', 'error')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    conn = get_db()
    
    stats = {
        'total_students': conn.execute("SELECT COUNT(*) as count FROM users WHERE role='student'").fetchone()['count'],
        'total_instructors': conn.execute("SELECT COUNT(*) as count FROM users WHERE role='instructor'").fetchone()['count'],
        'total_courses': conn.execute("SELECT COUNT(*) as count FROM courses").fetchone()['count'],
        'total_assignments': conn.execute("SELECT COUNT(*) as count FROM assignments").fetchone()['count'],
        'total_submissions': conn.execute("SELECT COUNT(*) as count FROM submissions").fetchone()['count']
    }
    
    users = conn.execute('SELECT * FROM users ORDER BY id DESC LIMIT 20').fetchall()
    courses = conn.execute('SELECT * FROM courses ORDER BY id DESC LIMIT 20').fetchall()
    
    conn.close()
    return render_template('admin_dashboard.html', stats=stats, users=users, courses=courses)

@app.route('/admin/create_course', methods=['GET', 'POST'])
def create_course():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        course_code = request.form['course_code']
        course_name = request.form['course_name']
        department = request.form['department']
        instructor_id = request.form.get('instructor_id')
        
        try:
            conn = get_db()
            conn.execute('''
                INSERT INTO courses (course_code, course_name, department, instructor_id)
                VALUES (?, ?, ?, ?)
            ''', (course_code, course_name, department, instructor_id))
            conn.commit()
            conn.close()
            flash('Course created successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        except sqlite3.IntegrityError:
            flash('Course code already exists', 'error')
    
    conn = get_db()
    instructors = conn.execute("SELECT * FROM users WHERE role='instructor'").fetchall()
    conn.close()
    
    return render_template('create_course.html', instructors=instructors)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
