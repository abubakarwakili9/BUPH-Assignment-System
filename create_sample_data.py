"""
Sample Data Generator for Online Assignment Submission System
This script creates sample users, courses, and assignments for testing.
"""

import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def create_sample_data():
    """Create sample data for testing the application"""
    
    conn = sqlite3.connect('assignment_system.db')
    cursor = conn.cursor()
    
    print("Creating sample data...")
    
    # Sample Students
    students = [
        ('john_doe', 'password123', 'John Doe', 'john.doe@student.buph.edu.ng', 'Computer Science', 'CS/2021/001'),
        ('jane_smith', 'password123', 'Jane Smith', 'jane.smith@student.buph.edu.ng', 'Computer Science', 'CS/2021/002'),
        ('ahmed_ibrahim', 'password123', 'Ahmed Ibrahim', 'ahmed.ibrahim@student.buph.edu.ng', 'Computer Science', 'CS/2021/003'),
        ('fatima_mohammed', 'password123', 'Fatima Mohammed', 'fatima.mohammed@student.buph.edu.ng', 'Engineering', 'ENG/2021/001'),
        ('usman_ali', 'password123', 'Usman Ali', 'usman.ali@student.buph.edu.ng', 'Engineering', 'ENG/2021/002'),
    ]
    
    print("Creating 5 sample students...")
    for username, password, full_name, email, department, student_id in students:
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute("""
                INSERT INTO users (username, password, full_name, email, role, department, student_id)
                VALUES (?, ?, ?, ?, 'student', ?, ?)
            """, (username, hashed_password, full_name, email, department, student_id))
            print(f"  ✓ Created student: {full_name}")
        except sqlite3.IntegrityError:
            print(f"  ⚠ Student {username} already exists")
    
    # Sample Instructors
    instructors = [
        ('dr_bello', 'password123', 'Dr. Bello Musa', 'bello.musa@buph.edu.ng', 'Computer Science'),
        ('prof_aisha', 'password123', 'Prof. Aisha Sani', 'aisha.sani@buph.edu.ng', 'Engineering'),
        ('mr_ibrahim', 'password123', 'Mr. Ibrahim Yusuf', 'ibrahim.yusuf@buph.edu.ng', 'Mathematics'),
    ]
    
    print("\nCreating 3 sample instructors...")
    for username, password, full_name, email, department in instructors:
        hashed_password = generate_password_hash(password)
        try:
            cursor.execute("""
                INSERT INTO users (username, password, full_name, email, role, department)
                VALUES (?, ?, ?, ?, 'instructor', ?)
            """, (username, hashed_password, full_name, email, department))
            print(f"  ✓ Created instructor: {full_name}")
        except sqlite3.IntegrityError:
            print(f"  ⚠ Instructor {username} already exists")
    
    # Get instructor IDs
    cursor.execute("SELECT id, full_name FROM users WHERE username IN ('dr_bello', 'prof_aisha', 'mr_ibrahim')")
    instructors_data = cursor.fetchall()
    
    if not instructors_data:
        print("\n⚠ No instructors found. Please run script again.")
        conn.close()
        return
    
    # Sample Courses
    courses = [
        ('CS101', 'Introduction to Computer Science', 'Computer Science', instructors_data[0][0] if len(instructors_data) > 0 else None),
        ('CS201', 'Data Structures and Algorithms', 'Computer Science', instructors_data[0][0] if len(instructors_data) > 0 else None),
        ('ENG101', 'Engineering Mathematics', 'Engineering', instructors_data[1][0] if len(instructors_data) > 1 else None),
        ('CS301', 'Database Management Systems', 'Computer Science', instructors_data[0][0] if len(instructors_data) > 0 else None),
        ('ENG201', 'Thermodynamics', 'Engineering', instructors_data[1][0] if len(instructors_data) > 1 else None),
    ]
    
    print("\nCreating 5 sample courses...")
    course_ids = []
    for course_code, course_name, department, instructor_id in courses:
        try:
            cursor.execute("""
                INSERT INTO courses (course_code, course_name, department, instructor_id)
                VALUES (?, ?, ?, ?)
            """, (course_code, course_name, department, instructor_id))
            course_ids.append(cursor.lastrowid)
            print(f"  ✓ Created course: {course_code} - {course_name}")
        except sqlite3.IntegrityError:
            print(f"  ⚠ Course {course_code} already exists")
            cursor.execute("SELECT id FROM courses WHERE course_code = ?", (course_code,))
            result = cursor.fetchone()
            if result:
                course_ids.append(result[0])
    
    # Sample Assignments
    today = datetime.now()
    assignments = [
        ('Introduction to Programming Assignment', 
         'Write a Python program that calculates the factorial of a number. Include proper documentation and test cases.',
         course_ids[0] if len(course_ids) > 0 else 1,
         (today + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M'),
         100),
        
        ('Data Structures Project', 
         'Implement a Binary Search Tree in Python with insert, delete, and search operations. Provide complexity analysis.',
         course_ids[1] if len(course_ids) > 1 else 2,
         (today + timedelta(days=14)).strftime('%Y-%m-%dT%H:%M'),
         100),
        
        ('Engineering Calculus Problem Set', 
         'Solve problems 1-20 from Chapter 5. Show all working and final answers.',
         course_ids[2] if len(course_ids) > 2 else 3,
         (today + timedelta(days=5)).strftime('%Y-%m-%dT%H:%M'),
         50),
        
        ('Database Design Assignment', 
         'Design a database schema for a library management system. Include ER diagram and normalized tables.',
         course_ids[3] if len(course_ids) > 3 else 4,
         (today + timedelta(days=10)).strftime('%Y-%m-%dT%H:%M'),
         100),
        
        ('Thermodynamics Lab Report', 
         'Submit a detailed lab report on the heat transfer experiment conducted in class. Include calculations and analysis.',
         course_ids[4] if len(course_ids) > 4 else 5,
         (today + timedelta(days=3)).strftime('%Y-%m-%dT%H:%M'),
         75),
    ]
    
    print("\nCreating 5 sample assignments...")
    for title, description, course_id, due_date, total_marks in assignments:
        try:
            cursor.execute("""
                INSERT INTO assignments (title, description, course_id, due_date, total_marks)
                VALUES (?, ?, ?, ?, ?)
            """, (title, description, course_id, due_date, total_marks))
            print(f"  ✓ Created assignment: {title}")
        except Exception as e:
            print(f"  ⚠ Error creating assignment: {e}")
    
    conn.commit()
    conn.close()
    
    print("\n" + "="*60)
    print("✅ Sample data created successfully!")
    print("="*60)
    print("\nSample Login Credentials:")
    print("\nAdmin:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nInstructors:")
    print("  Username: dr_bello / Password: password123")
    print("  Username: prof_aisha / Password: password123")
    print("  Username: mr_ibrahim / Password: password123")
    print("\nStudents:")
    print("  Username: john_doe / Password: password123")
    print("  Username: jane_smith / Password: password123")
    print("  Username: ahmed_ibrahim / Password: password123")
    print("  Username: fatima_mohammed / Password: password123")
    print("  Username: usman_ali / Password: password123")
    print("\n⚠ Remember to change these passwords in production!")
    print("="*60)

if __name__ == '__main__':
    try:
        create_sample_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. The database exists (run: python app.py once)")
        print("2. You're in the correct directory")
        print("3. Python dependencies are installed")
