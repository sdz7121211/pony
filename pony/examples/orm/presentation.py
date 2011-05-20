from decimal import Decimal
from datetime import date

from pony.orm import *

class Department(Entity):
    number = PrimaryKey(int)
    name = Unique(unicode)
    groups = Set("Group")
    courses = Set("Course")

class Group(Entity):
    number = PrimaryKey(int)
    major = Required(unicode)
    dept = Required("Department")
    students = Set("Student")

class Course(Entity):
    name = Required(unicode)
    semester = Required(int)
    lect_hours = Required(int)
    lab_hours = Required(int)
    credits = Required(int)
    dept = Required(Department)
    students = Set("Student")
    PrimaryKey(name, semester)
    
class Student(Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(unicode)
    dob = Required(date)
    picture = Optional(buffer)
    gpa = Required(float, default=0)
    group = Required(Group)
    courses = Set(Course)

db = Database('sqlite', 'presentation.sqlite', create_db=True)
# db = Database('mysql', host="localhost", user="root", passwd="root", db="university")

db.generate_mapping(create_tables=True)

sql_debug(True)  # Output all SQL queries to stdout

def populate_database():
    if select.count(s for s in Student) > 0:
        return
    
    d1 = Department.create(number=1, name="Department of Computer Science")
    d2 = Department.create(number=2, name="Department of Mathematical Sciences")
    d3 = Department.create(number=3, name="Department of Applied Physics")

    c1 = Course.create(name="Web Design", semester=1, dept=d1,
                       lect_hours=30, lab_hours=30, credits=3)
    c2 = Course.create(name="Data Structures and Algorithms", semester=3, dept=d1,
                       lect_hours=40, lab_hours=20, credits=4)

    c3 = Course.create(name="Linear Algebra", semester=1, dept=d2,
                       lect_hours=30, lab_hours=30, credits=4)
    c4 = Course.create(name="Statistical Methods", semester=2, dept=d2,
                       lect_hours=50, lab_hours=25, credits=5)

    c5 = Course.create(name="Thermodynamics", semester=2, dept=d3,
                       lect_hours=25, lab_hours=40, credits=4)
    c6 = Course.create(name="Quantum Mechanics", semester=3, dept=d3,
                       lect_hours=40, lab_hours=30, credits=5)

    g101 = Group.create(number=101, major='B.E. in Computer Engineering', dept=d1)
    g102 = Group.create(number=102, major='B.S./M.S. in Computer Science', dept=d1)
    g103 = Group.create(number=103, major='B.S. in Applied Mathematics and Statistics', dept=d2)
    g104 = Group.create(number=104, major='B.S./M.S. in Pure Mathematics', dept=d2)
    g105 = Group.create(number=105, major='B.E in Electronics', dept=d3)
    g106 = Group.create(number=106, major='B.S./M.S. in Nuclear Engineering', dept=d3)

    s1 = Student.create(name='John Smith', dob=date(1991, 3, 20), gpa=3, group=g101,
                        courses=[c1, c2, c4, c6])
    s1 = Student.create(name='Matthew Reed', dob=date(1990, 11, 26), gpa=3.5, group=g101,
                        courses=[c1, c3, c4, c5])
    s1 = Student.create(name='Chuan Qin', dob=date(1989, 2, 5), gpa=4, group=g101,
                        courses=[c3, c5, c6])
    s1 = Student.create(name='Rebecca Lawson', dob=date(1990, 4, 18), gpa=3.3, group=g102,
                        courses=[c1, c4, c5, c6])
    s1 = Student.create(name='Maria Ionescu', dob=date(1991, 4, 23), gpa=3.9, group=g102,
                        courses=[c1, c2, c4, c6])
    s1 = Student.create(name='Oliver Blakey', dob=date(1990, 9, 8), gpa=3.1, group=g102,
                        courses=[c1, c2, c5])
    s1 = Student.create(name='Jing Xia', dob=date(1988, 12, 30), gpa=3.2, group=g102,
                        courses=[c1, c3, c5, c6])
    commit()

def print_students(students):
    for s in students:
        print s.name
    print

def test_queries():
    students = select(s for s in Student).all()
    print_students(students)


    students = select(s for s in Student
                        if s.gpa > 3.4
                        and s.dob.year == 1990).all()
    print_students(students)


    students = select(s for s in Student if len(s.courses) < 4).all()
    print_students(students)


    students = select(s for s in Student if s.name.startswith("M")).all()
    print_students(students)


    students = select(s for s in Student if "Smith" in s.name).all()
    print_students(students)


    students = select(s for s in Student 
                        if "Web Design" in s.courses.name).all()
    print_students(students)


    avg = select.avg(s.gpa for s in Student)
    print 'Average GPA is', avg
    print
    

    students = select(s for s in Student 
                        if sum(c.credits for c in s.courses) < 15).all()
    print_students(students)


    sstudents = select(s for s in Student 
                         if s.group.major == "B.E. in Computer Engineering").all()
    print_students(students)


    students = select(s for s in Student 
                      if s.group.dept.name == "Department of Computer Science").all()
    print_students(students)


    students = select(s for s in Student).orderby(Student.name).all()
    print_students(students)


    students = select(s for s in Student).orderby(Student.name)[2:4]
    print_students(students)


    students = select(s for s in Student).orderby(Student.name.desc).all()
    print_students(students)


    students = select(s for s in Student).orderby(Student.group, Student.name.desc).all()
    print_students(students)


    students = select(s for s in Student 
             if s.group.dept.name == "Department of Computer Science"
                and s.gpa > 3.5
                and len(s.courses) > 3).all()
    print_students(students)


if __name__ == '__main__':
    populate_database()
    test_queries()