-- Create the University Database
CREATE DATABASE university_db;

-- Connect to the database
\c university_db;

-- Create Tables with Relationships

-- 1. Students Table
CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(15),
    enrollment_date DATE,
    major_id INT,
    advisor_id INT
);

-- 2. Faculty Table
CREATE TABLE faculty (
    faculty_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(15),
    hire_date DATE,
    department_id INT
);

-- 3. Departments Table
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE,
    building VARCHAR(50),
    budget NUMERIC(10, 2)
);

-- 4. Courses Table
CREATE TABLE courses (
    course_id SERIAL PRIMARY KEY,
    course_name VARCHAR(100),
    course_code VARCHAR(10) UNIQUE,
    credits INT,
    department_id INT REFERENCES departments(department_id)
);

-- 5. Enrollments Table
CREATE TABLE enrollments (
    enrollment_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    enrollment_date DATE,
    grade CHAR(1)
);

-- 6. Classrooms Table
CREATE TABLE classrooms (
    classroom_id SERIAL PRIMARY KEY,
    building VARCHAR(50),
    room_number VARCHAR(10),
    capacity INT
);

-- 7. Course Schedule Table
CREATE TABLE course_schedule (
    schedule_id SERIAL PRIMARY KEY,
    course_id INT REFERENCES courses(course_id),
    classroom_id INT REFERENCES classrooms(classroom_id),
    faculty_id INT REFERENCES faculty(faculty_id),
    day_of_week VARCHAR(10),
    start_time TIME,
    end_time TIME
);

-- 8. Scholarships Table
CREATE TABLE scholarships (
    scholarship_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    amount NUMERIC(10, 2),
    eligibility_criteria TEXT
);

-- 9. Student Scholarships Table
CREATE TABLE student_scholarships (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    scholarship_id INT REFERENCES scholarships(scholarship_id),
    awarded_date DATE
);

-- 10. Advisors Table
CREATE TABLE advisors (
    advisor_id SERIAL PRIMARY KEY,
    faculty_id INT REFERENCES faculty(faculty_id),
    department_id INT REFERENCES departments(department_id)
);

-- 11. Attendance Table
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    course_id INT REFERENCES courses(course_id),
    date DATE,
    status BOOLEAN
);

-- 12. Library Table
CREATE TABLE library (
    library_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    building VARCHAR(50)
);

-- 13. Books Table
CREATE TABLE books (
    book_id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    author VARCHAR(100),
    isbn VARCHAR(20),
    publication_year INT,
    library_id INT REFERENCES library(library_id)
);

-- 14. Student Borrowing Table
CREATE TABLE student_borrowing (
    borrow_id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    book_id INT REFERENCES books(book_id),
    borrow_date DATE,
    return_date DATE
);

-- 15. Events Table
CREATE TABLE events (
    event_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    date DATE,
    location VARCHAR(100),
    description TEXT
);

-- 16. Student Event Participation Table
CREATE TABLE student_event_participation (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    event_id INT REFERENCES events(event_id)
);

-- 17. Internships Table
CREATE TABLE internships (
    internship_id SERIAL PRIMARY KEY,
    company_name VARCHAR(100),
    position VARCHAR(50),
    start_date DATE,
    end_date DATE
);

-- 18. Student Internships Table
CREATE TABLE student_internships (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    internship_id INT REFERENCES internships(internship_id)
);

-- 19. Housing Table
CREATE TABLE housing (
    housing_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    capacity INT,
    building VARCHAR(50)
);

-- 20. Student Housing Table
CREATE TABLE student_housing (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES students(student_id),
    housing_id INT REFERENCES housing(housing_id),
    move_in_date DATE,
    move_out_date DATE
);

-- Add some indexes for optimization
CREATE INDEX idx_student_major ON students(major_id);
CREATE INDEX idx_course_department ON courses(department_id);
CREATE INDEX idx_student_email ON students(email);
