from faker import Faker
import random
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import sessionmaker

# Initialize Faker and database connection
fake = Faker()
DATABASE_URL = 'postgresql://postgres:pass2006@localhost/childcare_db_fastapi'  # Replace with your credentials
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

# Define models based on your tables
children_table = Table('children', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('name', String),
                       Column('age', Integer),
                       Column('classroom', String))

staff_table = Table('staff', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String),
                    Column('role', String))

attendance_table = Table('attendance', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('date', String),
                         Column('status', String),
                         Column('child_id', Integer, ForeignKey('children.id')),
                         Column('staff_id', Integer, ForeignKey('staff.id')))

# Data generation functions
CLASSROOMS = ['Y1A', 'Y1B', 'Y2A', 'Y2B', 'Y3A', 'Y3B', 'Y4A', 'Y4B', 'Y5A', 'Y5B', 'Red', 'Green', 'Yellow', 'Blue']
STAFF_ROLES = ['Teacher', 'DOS', 'Principal', 'Vice Principal', 'Counselor', 'Librarian', 'Admin']
ATTENDANCE_STATUSES = ['present', 'absent', 'late']

def generate_children(num_children=1000000):
    return [{"name": f"{fake.first_name()} {fake.last_name()}",
             "age": random.randint(5, 15),
             "classroom": random.choice(CLASSROOMS)} for _ in range(num_children)]

def generate_staff(num_staff=500000):
    return [{"name": f"{fake.first_name()} {fake.last_name()}",
             "role": random.choice(STAFF_ROLES)} for _ in range(num_staff)]

# Insert data and return IDs
def insert_and_get_ids(table, data_list, batch_size=10000):
    inserted_ids = []
    for i in range(0, len(data_list), batch_size):
        result = session.execute(table.insert().returning(table.c.id), data_list[i:i + batch_size])
        inserted_ids.extend([row[0] for row in result])
        session.commit()  # Commit after each batch
        print(f"Inserted {len(inserted_ids)} records into {table.name}")
    return inserted_ids

# Batch insert function for attendance
def insert_attendance(attendance_list, batch_size=10000):
    for i in range(0, len(attendance_list), batch_size):
        session.execute(attendance_table.insert(), attendance_list[i:i + batch_size])
        session.commit()  # Commit after each batch
        print(f"Inserted {i + batch_size} records into attendance")

# Main function to insert all data
def insert_data():
    print("Generating and inserting Children...")
    children = generate_children()
    child_ids = insert_and_get_ids(children_table, children)

    print("Generating and inserting Staff...")
    staff = generate_staff()
    staff_ids = insert_and_get_ids(staff_table, staff)

    print("Generating and inserting Attendance Records...")
    attendance = [{"date": fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d'),
                   "status": random.choice(ATTENDANCE_STATUSES),
                   "child_id": random.choice(child_ids),
                   "staff_id": random.choice(staff_ids)} for _ in range(1000000)]
    insert_attendance(attendance)

    print("Data insertion complete!")

if __name__ == '__main__':
    insert_data()
