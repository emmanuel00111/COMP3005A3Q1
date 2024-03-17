#Emmanuel Adekoya 101235395
#COMP3005 Assignment3 Q1 v2.0
import psycopg2
from psycopg2 import sql

# Function to establish a connectionection to the PostgreSQL database
def connect():
    return psycopg2.connect(
        host=input("Enter host: "),
        database=input("Enter database: "),
        user=input("Enter username: "),
        password=input("Enter password: "),
        port=input("Enter Port: ")
    )

# Function to create the students table
def create_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id SERIAL PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                enrollment_date DATE
            )
        """)
        connection.commit()

# Function to insert initial data into the students table
def insert_initial_data(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
        """, ('John', 'Doe', 'john.doe@example.com', '2023-09-01'))
        cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
        """, ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'))
        cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
        """, ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02'))
        connection.commit()

# Function to get all students from the students table
def get_all_students(connection):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students")
        records = cursor.fetchall()

        # Print the records
        for record in records:
            print(record)

# Function to add a new student to the students table
def add_student(connection, first_name, last_name, email, enrollment_date):
    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
            RETURNING student_id, first_name, last_name, email, enrollment_date;
        """, (first_name, last_name, email, enrollment_date))

        # Fetch the newly inserted record
        new_student = cursor.fetchone()

        # Print the new student record
        print('\nNew Student:', new_student)

        connection.commit()

# Function to update a student's email by student_id
def update_student_email(connection, student_id, new_email):
    with connection.cursor() as cursor:
        cursor.execute("""
            UPDATE students
            SET email = %s
            WHERE student_id = %s
            RETURNING student_id, first_name, last_name, email, enrollment_date;
        """, (new_email, student_id))

        # Fetch the updated student record
        updated_student = cursor.fetchone()

        # Print the updated student record
        print('\nUpdated Student:', updated_student)

        connection.commit()

# Function to delete a student by student_id
def delete_student(connection, student_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM students WHERE student_id = %s RETURNING student_id, first_name, last_name, email, enrollment_date;", (student_id,))

        # Fetch the deleted student record
        deleted_student = cursor.fetchone()

        # Print the deleted student record
        print('\nDeleted Student:', deleted_student)

        connection.commit()

# Main function to demonstrate the application
def main():
    connection = connect()
    create_table(connection)
    insert_initial_data(connection)

    while True:
        print("\nAvailable commands:")
        print("getAllStudents() -> Get all students")
        print("addStudent() -> Add a new student")
        print("updateStudentEmail() -> Update student email")
        print("deleteStudent() -> Delete a student")
        print("exit -> Exit")

        choice = input("\nEnter your choice: ")

        if choice == 'getAllStudents()':
            print("All students:")
            print(get_all_students(connection))
        elif choice == 'addStudent()':
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
            add_student(connection, first_name, last_name, email, enrollment_date)
            print("Student added successfully.")
        elif choice == 'updateStudentEmail()':
            student_id = input("Enter student ID: ")
            new_email = input("Enter new email: ")
            update_student_email(connection, student_id, new_email)
            print("Email updated successfully.")
        elif choice == 'deleteStudent()':
            student_id = input("Enter student ID to delete: ")
            delete_student(connection, student_id)
            print("Student deleted successfully.")
        elif choice == 'exit':
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()

if __name__ == "__main__":
    main()
