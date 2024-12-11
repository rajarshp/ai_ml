import psycopg2
from faker import Faker
import random
from random import randint, choice
from datetime import datetime, timedelta

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="university_db",
    user="postgres",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

faker = Faker()

def generate_phone_number():
    """Generate a phone number with exactly 15 digits."""
    # A simple phone number format with exactly 15 digits (e.g., 123-456-789012345)
    phone_number = f"{random.randint(100, 999)}-{random.randint(000, 999)}-{random.randint(1000, 9999)}"
    return phone_number

def get_unique_email():
    email = faker.unique.email()
    cursor.execute("SELECT COUNT(1) FROM students WHERE email = %s", (email,))
    while cursor.fetchone()[0] > 0:
        email = faker.unique.email()  # Generate a new email until it's unique
    return email

# Data generation functions for each table
def generate_departments():
    departments = []
    for _ in range(10):
        name = faker.unique.company()
        building = faker.random_element(['Building A', 'Building B', 'Building C'])
        budget = round(faker.random_number(digits=7, fix_len=True), 2)
        departments.append((name, building, budget))
    cursor.executemany(
        "INSERT INTO departments (name, building, budget) VALUES (%s, %s, %s)",
        departments
    )

def generate_faculty():
    cursor.execute("SELECT department_id FROM departments")
    department_ids = [row[0] for row in cursor.fetchall()]
    faculty = []
    for _ in range(30):
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.unique.email()
        phone_number = generate_phone_number()
        hire_date = faker.date_between(start_date='-10y', end_date='today')
        department_id = choice(department_ids)
        faculty.append((first_name, last_name, email, phone_number, hire_date, department_id))
    cursor.executemany(
        "INSERT INTO faculty (first_name, last_name, email, phone_number, hire_date, department_id) VALUES (%s, %s, %s, %s, %s, %s)",
        faculty
    )

def generate_students():
    cursor.execute("SELECT faculty_id FROM faculty")
    advisor_ids = [row[0] for row in cursor.fetchall()]
    students = []
    for _ in range(100):
        first_name = faker.first_name()
        last_name = faker.last_name()
        email = faker.unique.email()
        phone_number = generate_phone_number()
        enrollment_date = faker.date_between(start_date='-5y', end_date='today')
        major_id = randint(1, 10)
        advisor_id = choice(advisor_ids)
        students.append((first_name, last_name, email, phone_number, enrollment_date, major_id, advisor_id))
    cursor.executemany(
        "INSERT INTO students (first_name, last_name, email, phone_number, enrollment_date, major_id, advisor_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        students
    )

def generate_courses():
    cursor.execute("SELECT department_id FROM departments")
    department_ids = [row[0] for row in cursor.fetchall()]
    courses = []
    for _ in range(50):
        course_name = faker.catch_phrase()
        course_code = faker.unique.lexify(text='?????-###')
        credits = randint(1, 5)
        department_id = choice(department_ids)
        courses.append((course_name, course_code, credits, department_id))
    cursor.executemany(
        "INSERT INTO courses (course_name, course_code, credits, department_id) VALUES (%s, %s, %s, %s)",
        courses
    )

def generate_enrollments():
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT course_id FROM courses")
    course_ids = [row[0] for row in cursor.fetchall()]
    enrollments = []
    for _ in range(200):
        student_id = choice(student_ids)
        course_id = choice(course_ids)
        enrollment_date = faker.date_between(start_date='-3y', end_date='today')
        grade = faker.random_element(['A', 'B', 'C', 'D', 'F'])
        enrollments.append((student_id, course_id, enrollment_date, grade))
    cursor.executemany(
        "INSERT INTO enrollments (student_id, course_id, enrollment_date, grade) VALUES (%s, %s, %s, %s)",
        enrollments
    )

def generate_classrooms():
    classrooms = []
    for _ in range(20):
        building = faker.random_element(['Building A', 'Building B', 'Building C'])
        room_number = faker.lexify(text="???-###")
        capacity = randint(20, 200)
        classrooms.append((building, room_number, capacity))
    cursor.executemany(
        "INSERT INTO classrooms (building, room_number, capacity) VALUES (%s, %s, %s)",
        classrooms
    )

def generate_course_schedule():
    cursor.execute("SELECT course_id FROM courses")
    course_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT classroom_id FROM classrooms")
    classroom_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT faculty_id FROM faculty")
    faculty_ids = [row[0] for row in cursor.fetchall()]
    schedules = []
    for _ in range(100):
        course_id = choice(course_ids)
        classroom_id = choice(classroom_ids)
        faculty_id = choice(faculty_ids)
        day_of_week = faker.random_element(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        start_time = faker.time_object()
        end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=2)).time()
        schedules.append((course_id, classroom_id, faculty_id, day_of_week, start_time, end_time))
    cursor.executemany(
        "INSERT INTO course_schedule (course_id, classroom_id, faculty_id, day_of_week, start_time, end_time) VALUES (%s, %s, %s, %s, %s, %s)",
        schedules
    )

def generate_scholarships():
    scholarships = []
    for _ in range(20):
        name = faker.catch_phrase()
        amount = round(faker.random_number(digits=6, fix_len=True), 2)
        eligibility_criteria = faker.text(max_nb_chars=200)
        scholarships.append((name, amount, eligibility_criteria))
    cursor.executemany(
        "INSERT INTO scholarships (name, amount, eligibility_criteria) VALUES (%s, %s, %s)",
        scholarships
    )

def generate_student_scholarships():
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT scholarship_id FROM scholarships")
    scholarship_ids = [row[0] for row in cursor.fetchall()]
    student_scholarships = []
    for _ in range(50):
        student_id = choice(student_ids)
        scholarship_id = choice(scholarship_ids)
        awarded_date = faker.date_between(start_date='-2y', end_date='today')
        student_scholarships.append((student_id, scholarship_id, awarded_date))
    cursor.executemany(
        "INSERT INTO student_scholarships (student_id, scholarship_id, awarded_date) VALUES (%s, %s, %s)",
        student_scholarships
    )

def generate_advisors():
    cursor.execute("SELECT faculty_id FROM faculty")
    faculty_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT department_id FROM departments")
    department_ids = [row[0] for row in cursor.fetchall()]
    advisors = []
    for _ in range(20):
        faculty_id = choice(faculty_ids)
        department_id = choice(department_ids)
        advisors.append((faculty_id, department_id))
    cursor.executemany(
        "INSERT INTO advisors (faculty_id, department_id) VALUES (%s, %s)",
        advisors
    )

def generate_attendance():
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT course_id FROM courses")
    course_ids = [row[0] for row in cursor.fetchall()]
    attendance = []
    for _ in range(200):
        student_id = choice(student_ids)
        course_id = choice(course_ids)
        date = faker.date_this_year()
        status = choice([True, False])
        attendance.append((student_id, course_id, date, status))
    cursor.executemany(
        "INSERT INTO attendance (student_id, course_id, date, status) VALUES (%s, %s, %s, %s)",
        attendance
    )

def generate_library():
    libraries = []
    for _ in range(5):
        name = faker.company()
        building = faker.random_element(['Building A', 'Building B', 'Building C'])
        libraries.append((name, building))
    cursor.executemany(
        "INSERT INTO library (name, building) VALUES (%s, %s)",
        libraries
    )

def generate_books():
    cursor.execute("SELECT library_id FROM library")
    library_ids = [row[0] for row in cursor.fetchall()]
    books = []
    for _ in range(100):
        title = faker.sentence(nb_words=4)
        author = faker.name()
        isbn = faker.unique.isbn13()
        publication_year = randint(1990, 2024)
        library_id = choice(library_ids)
        books.append((title, author, isbn, publication_year, library_id))
    cursor.executemany(
        "INSERT INTO books (title, author, isbn, publication_year, library_id) VALUES (%s, %s, %s, %s, %s)",
        books
    )

def generate_student_borrowing():
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT book_id FROM books")
    book_ids = [row[0] for row in cursor.fetchall()]
    borrowings = []
    for _ in range(100):
        student_id = choice(student_ids)
        book_id = choice(book_ids)
        borrow_date = faker.date_this_year()
        return_date = borrow_date + timedelta(days=randint(7, 30))
        borrowings.append((student_id, book_id, borrow_date, return_date))
    cursor.executemany(
        "INSERT INTO student_borrowing (student_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)",
        borrowings
    )

def generate_events():
    events = []
    for _ in range(20):
        name = faker.sentence(nb_words=4)
        event_date = faker.date_this_year()
        location = faker.address()
        description = faker.text(max_nb_chars=200)
        events.append((name, event_date, location, description))
    cursor.executemany(
        "INSERT INTO events (name, date, location, description) VALUES (%s, %s, %s, %s)",
        events
    )

def generate_student_event_participation():
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT event_id FROM events")
    event_ids = [row[0] for row in cursor.fetchall()]
    student_event_participation = []
    for _ in range(50):
        student_id = choice(student_ids)
        event_id = choice(event_ids)
        student_event_participation.append((student_id, event_id))
    cursor.executemany(
        "INSERT INTO student_event_participation (student_id, event_id) VALUES (%s, %s)",
        student_event_participation
    )

def generate_internships():
    internships = []
    for _ in range(10):
        company_name = faker.company()
        position = faker.job()
        start_date = faker.date_between(start_date='-3y', end_date='today')
        end_date = start_date + timedelta(days=randint(90, 180))
        internships.append((company_name, position, start_date, end_date))
    cursor.executemany(
        "INSERT INTO internships (company_name, position, start_date, end_date) VALUES (%s, %s, %s, %s)",
        internships
    )

def generate_student_internships():
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT internship_id FROM internships")
    internship_ids = [row[0] for row in cursor.fetchall()]
    student_internships = []
    for _ in range(30):
        student_id = choice(student_ids)
        internship_id = choice(internship_ids)
        student_internships.append((student_id, internship_id))
    cursor.executemany(
        "INSERT INTO student_internships (student_id, internship_id) VALUES (%s, %s)",
        student_internships
    )

def generate_housing():
    housing = []
    for _ in range(5):
        name = faker.word()
        capacity = randint(50, 200)
        building = faker.random_element(['Building A', 'Building B', 'Building C'])
        housing.append((name, capacity, building))
    cursor.executemany(
        "INSERT INTO housing (name, capacity, building) VALUES (%s, %s, %s)",
        housing
    )

def generate_student_housing():
    cursor.execute("SELECT student_id FROM students")
    student_ids = [row[0] for row in cursor.fetchall()]
    cursor.execute("SELECT housing_id FROM housing")
    housing_ids = [row[0] for row in cursor.fetchall()]
    student_housing = []
    for _ in range(40):
        student_id = choice(student_ids)
        housing_id = choice(housing_ids)
        move_in_date = faker.date_this_year()
        move_out_date = move_in_date + timedelta(days=randint(180, 365))
        student_housing.append((student_id, housing_id, move_in_date, move_out_date))
    cursor.executemany(
        "INSERT INTO student_housing (student_id, housing_id, move_in_date, move_out_date) VALUES (%s, %s, %s, %s)",
        student_housing
    )

    # Call functions to insert data for all tables
generate_departments()
generate_faculty()
generate_students()
generate_courses()
generate_enrollments()
generate_classrooms()
generate_course_schedule()
generate_scholarships()
generate_student_scholarships()
generate_advisors()
generate_attendance()
generate_library()
generate_books()
generate_student_borrowing()
generate_events()
generate_student_event_participation()
generate_internships()
generate_student_internships()
generate_housing()
generate_student_housing()

conn.commit()
print("Data population complete!")

# Close the connection
cursor.close()
conn.close()
