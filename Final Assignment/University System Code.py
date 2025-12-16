def import_csv(filename):
    file=open(filename,'r')                                                      #Opens the file in readmode
    studdata={}                                                                  #Made a dictionary
    headers = file.readline().strip().split(',')                                 #Replaces the \n with an empty string so that it looks neater and replace it with a delimiter which is ,
    for line in file:
        linedata=line.strip().split(',')                                         #Same as before but for the data instead of the headers
        row={}                                                                   #Another dictionary
        for x in range(len(headers)):
            if(x in range(len(linedata))):                                       #Checks whether there is any data in a section of a header
                row[headers[x]]=linedata[x]
            else:
                row[headers[x]]="null"                                           #If there is no data then it prints null into that information box
        studdata[linedata[1]]=[row]                                              #This is to display each of the values along with its headers while keeping the 1st column as the main info
    file.close()                                                                 #This ensures that the file closes
    return studdata

MODULES_FILE = "Modules.csv"
ENROLLMENTS_FILE = "Enrollments.csv"
GRADES_FILE = "Grades.csv"
ATTENDANCE_FILE = "Attendance.csv"
STUDENT_INFO = "StudInfo.csv"

# Make a CSV File for attendance
header = ["student_id", "module_code", "attendance_percentage"]
rows = [
    [100, "M001", 100],
    [102, "M002", 97],
    [103, "M003", 95],
]

student_ids = []  # List to store student IDs
student_names = []  # List to store student names
paid_fees = []  # List to store the amount paid by each student
outstanding_fees = []  # List to store outstanding fees for each student

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

def new_stud(students,filename):
    students=[]                                                                                             #List to store the input of the user
    newid = input("Enter the Student ID: ").upper()
    with open(filename,'r') as file:
        for id in file:                                                                                     #Makes sure that the Student ID remains unique
            data = id.strip().split(',')
            if data[1] == newid:
                print("This StudentID is already registered!")
                return
    newname = input("Enter the Student's Name: ").upper()
    newprog = input("Enter the Student's Program: ").upper()
    newcont = input("Enter the Student's Contact Info: ").upper()
    students.append({'Name':newname,'StudentID':newid,'Program':newprog,'Contact Info':newcont})            #This is so that the information is put into its own header
    with open(filename,'a') as file:
        for students in students:
            file.write(
                f"{students['Name']},{students['StudentID']},{students['Program']},{students['Contact Info']}\n"
            )
    print(students)
    students.clear()
    print("Student Registered Successfully!")


def update_stud(filename):
    idnum = input("Please enter the ID of the student to edit: ").upper()           #Getting an input from the user about which students detail needs to be updated
    found = False
    updated_data = []

    with open(filename,'r') as idfile:
        for member in idfile:
            data = member.strip().split(',')
            if data[1] == idnum:                                                    # To check is the studentID exists
                found = True
                print(f"Current Details: Name:{data[0]}, Student ID: {data[1]},Program: {data[2]},Contact Info: {data[3]}")
                new_name = input("Enter the new name (Leave blank to keep the current Name): ") or data[0]
                new_id = input("Enter the new ID (Leave blank to keep the current Name): ") or data[1]
                new_prog = input("Enter the new Program (Leave blank to keep the current Name): ") or data[2]
                new_cont = input("Enter the new Contact Info (Leave blank to keep the current Name): ") or data[3]
                updated_data.append(f"{new_name},{new_id},{new_prog},{new_cont}\n")     #Adding updated details to the updated data list
            else:
                updated_data.append(member)                                             #This is to keep the data of other students unchanged
    if found:
        with open(filename,'w') as idfile:                                              #This will open the file in write mode the update the student info
            idfile.writelines(updated_data)
        print("Student Information Updated Successfully!")
    else:
        print("Student not found.")
    print(f"Updated Info: Name: {new_name}, StudentID: {new_id}, Program: {new_prog}, Contact Info: {new_cont}")
    updated_data.clear()


def display_stud(filename):
    idnum = input("Please enter the ID of the student: ").upper()

    with open(filename, 'r') as idfile:                                                 #This will open the csv file in read mode and display the info of a student
        for member in idfile:
            data = member.strip().split(',')
            if data[1] == idnum:                                                        #This checks if the StudentID is valid
                found = True
                print(f"Name: {data[0]}, Student ID: {data[1]}, Program: {data[2]}, Contact Info: {data[3]}")
    return


def manage_enrollments(students_file, modules_file, enrollment_file):
    student_id = input("Enter the Student ID: ")
    found_student = False

    with open(students_file, 'r') as students:                                          #This verifies that the studentID exists in the database
        for line in students:
            data = line.strip().split(',')
            if data[1] == student_id:
                found_student = True
                print(f"Student Found: Name: {data[0]}, Program: {data[2]}")
                break

    if not found_student:
        print("Student ID not found in student records.")
        return

        #This displays the user all the available modules
    print("\nList of Available Modules:")
    modules = {}
    with open(modules_file, 'r') as module_file:                                    #Opens the file in read mode for making changes
        for line in module_file:
            module_data = line.strip().split(',')
            modules[module_data[0]] = module_data[1]
            print(f"{module_data[0]}: {module_data[1]}")

    selected_modules = input("\nEnter the module IDs to enroll (comma-separated): ").split(',')
    selected_modules = [mod.strip() for mod in selected_modules if mod.strip() in modules]

    if not selected_modules:
        print("No valid modules selected.")
        return

    updated_data = []                                           #Ths will update the enrollment file
    enrollment_found = False

    with open(enrollment_file, 'r') as enrollments:             #Opens the csv file in read mode
        for line in enrollments:
            enrollment_data = line.strip().split(',')
            if enrollment_data[0] == student_id:                #Checks for the validity of the studentID
                enrollment_found = True
                updated_data.append(f"{student_id},{','.join(selected_modules)}\n")
            else:
                updated_data.append(line)

    if not enrollment_found:
        updated_data.append(f"{student_id},{','.join(selected_modules)}\n")

    with open(enrollment_file, 'w') as enrollments:             #If studentID is valid this will open the file in read mode and update the file
        enrollments.writelines(updated_data)

    print("Enrollments updated successfully!")


def remove_student(filename):
    student_id = input("Enter the Student ID to remove: ").strip()
    found = False
    updated_data = []
                                                                # Read the file and keep all entries except the one to be removed
    with open(filename, 'r') as file:
        for line in file:
            data = line.strip().split(',')
            if data[1] == student_id:
                found = True
                print(f"Student Removed: Name: {data[0]}, ID: {data[1]}, Program: {data[2]}, Contact: {data[3]}")
            else:
                updated_data.append(line)

    if not found:
        print("Student ID not found.")
        return
                                                                # Write back the updated data to the file
    with open(filename, 'w') as file:
        file.writelines(updated_data)


def view_student_modules(enrollment_file, modules_file):
    modules = {}
    with open(modules_file, 'r') as mod_file:                     #This will open the module file in read mode and get all the data for the students
        for line in mod_file:
            if line.strip():
                module_data = line.strip().split(',')
                if len(module_data) == 2:
                    modules[module_data[0]] = module_data[1]

    print("\nStudent Enrollments:\n")
    with open(enrollment_file, 'r') as enroll_file:                 #This will open the grades file in read mode
        headers = enroll_file.readline().strip().split(',')
        print(f"{headers[0]} | Modules")
        print("-" * 40)

        for line in enroll_file:                                    #This will check for the studentID and the module code to make sure it exist in the database
            student_data = line.strip().split(',')
            student_id = student_data[0]
            student_modules = student_data[1:]

            module_names = [modules.get(module_id, "Unknown") for module_id in student_modules if module_id]
            print(f"{student_id} | {', '.join(module_names)}")


def issue_transcript(student_file, grades_file, modules_file):
    students = {}                                                       #A Dictionary to store studentID
    with open(student_file, 'r') as stud_file:                          #This will open the file in read mode so that it can issue a trancript for a student
        headers = stud_file.readline().strip().split(',')
        for line in stud_file:
            student_data = line.strip().split(',')
            if len(student_data) >= 2:
                students[student_data[1]] = student_data[0]             #This will store the studentID and name

    print("Loaded Students:", students)

    modules = {}                                                        #This is a dictionary to store the ModuleID
    with open(modules_file, 'r') as mod_file:
        mod_file.readline()
        for line in mod_file:
            module_data = line.strip().split(',')
            if len(module_data) == 2:
                modules[module_data[0]] = module_data[1]            #This stores the moduleID and name

    print("Loaded Modules:", modules)

    student_id = input("Enter the Student ID to issue transcript: ").strip()        #Takes input from the user and removes any whitespace
    if student_id not in students:
        print(f"Student ID {student_id} not found!")
        return

    print(f"\nTranscript for {students[student_id]} (ID: {student_id}):\n")
    print("Module Name\tGrade")
    print("-" * 30)

    with open(grades_file, 'r') as grade_file:                          #Opens the file in read mode
        headers = grade_file.readline().strip().split(',')
        for line in grade_file:
            grade_data = line.strip().split(',')
            if grade_data[0] == student_id:                             #This is to check if the studentID matches with the one entered
                for i in range(1, len(grade_data)):
                    module_id = headers[i]                              #This gets the moduleID from the header
                    grade = grade_data[i]                               #This gets the grades for that module
                    module_name = modules.get(module_id, "Unknown Module")      #Get the module name and if there is no module name it changes to Unknown module
                    print(f"{module_name}\t{grade}")
                return

    print("No grades found for this student.")

# Ensure necessary text files are created
def initialize_files():
    """Create necessary text files if they do not exist."""
    required_files = ["StudInfo.csv", "Modules.csv", "lecturers.csv",]
    for file_name in required_files:
        try:
            with open(file_name, "a", encoding="utf-8") as file:
                pass  # Create the file if it doesn't exist
        except Exception as e:
            print(f"Error creating file '{file_name}': {e}")

# Admin Login System
def admin_login():
    """Authenticate the administrator."""
    print("\n--- Admin Login ---")
    for attempt in range(3):  # Allow up to 3 attempts
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            print("Login successful! Welcome, Admin!")
            return True
        else:
            print(f"Invalid credentials. {2 - attempt} attempt(s) left.")
    print("Too many failed attempts. Exiting.")
    return False

# Add a new student
def add_new_student():
    """Add a new student to the system."""
    try:
        with open("StudInfo.csv", "a", encoding="utf-8") as file:
            student_id = input("Enter Student ID: ").strip()
            student_name = input("Enter Student Name: ").strip()
            student_dept = input("Enter Student Department: ").strip()
            contact_info = input("Enter Contact Info: ").strip()
            file.write(f"{student_id},{student_name},{student_dept},{contact_info}\n")
            print("Student added successfully!")
    except Exception as e:
        print(f"Error adding student: {e}")

# Remove a student
def delete_student():
    """Remove a student from the system."""
    try:
        student_id = input("Enter Student ID to remove: ").strip()
        found = False
        with open("StudInfo.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open("StudInfo.csv", "w", encoding="utf-8") as file:
            for line in lines:
                if line.startswith(student_id + ","):
                    found = True
                else:
                    file.write(line)
        if found:
            print("Student removed successfully!")
        else:
            print("Student ID not found.")
    except Exception as e:
        print(f"Error removing student: {e}")

# Add a new course
def add_course():
    """Add a new course record."""
    try:
        with open("Modules.csv", "a", encoding="utf-8") as file:
            course_code = input("Enter Course Code: ").strip()
            course_name = input("Enter Course Name: ").strip()
            file.write(f"{course_code},{course_name}\n")
            print("Course added successfully!")
    except Exception as e:
        print(f"Error adding course: {e}")

# Add a new lecturer
def add_new_lecturer():
    """Add a new lecturer to the system."""
    try:
        with open("lecturers.csv", "a", encoding="utf-8") as file:
            lecturer_id = input("Enter Lecturer ID: ").strip()
            lecturer_name = input("Enter Lecturer Name: ").strip()
            lecturer_dept = input("Enter Lecturer Department: ").strip()
            file.write(f"{lecturer_id},{lecturer_name},{lecturer_dept}\n")
            print("Lecturer added successfully!")
    except Exception as e:
        print(f"Error adding lecturer: {e}")

# Remove a lecturer
def delete_lecturer():
    """Remove a lecturer from the system."""
    try:
        lecturer_id = input("Enter Lecturer ID to remove: ").strip()
        found = False
        with open("lecturers.csv", "r", encoding="utf-8") as file:
            lines = file.readlines()
        with open("lecturers.csv", "w", encoding="utf-8") as file:
            for line in lines:
                if line.startswith(lecturer_id + ","):
                    found = True
                else:
                    file.write(line)
        if found:
            print("Lecturer removed successfully!")
        else:
            print("Lecturer ID not found.")
    except Exception as e:
        print(f"Error removing lecturer: {e}")

# Generate reports
def generate_reports():
    """Generate reports of the current data."""
    try:
        with open("StudInfo.csv", "r", encoding="utf-8") as file:
            students = file.readlines()
        print(f"Total Students: {len(students)}")

        with open("Modules.csv", "r", encoding="utf-8") as file:
            courses = file.readlines()
        print(f"Total Courses: {len(courses)}")

        with open("lecturers.csv", "r", encoding="utf-8") as file:
            lecturers = file.readlines()
        print(f"Total Lecturers: {len(lecturers)}")
    except FileNotFoundError:
        print("Error: One or more files not found.")
    except Exception as e:
        print(f"Error: {e}")

# View all data
def view_all_data():
    """Display all data from the text files."""
    try:
        print("\n--- All Data ---")

        # Display all students
        print("\nStudents:")
        with open("StudInfo.csv", "r", encoding="utf-8") as file:
            print(file.read())

        # Display all courses
        print("\nCourses:")
        with open("Modules.csv", "r", encoding="utf-8") as file:
            print(file.read())

        # Display all lecturers
        print("\nLecturers:")
        with open("lecturers.csv", "r", encoding="utf-8") as file:
            print(file.read())
    except FileNotFoundError:
        print("Error: One or more files not found.")
    except Exception as e:
        print(f"Error: {e}")

# Admin Main Menu
def admin_menu():
    """Display and handle the admin menu."""
    while True:
        print("\n--- Admin Menu ---")
        print("1. Add Course")
        print("2. Add Student")
        print("3. Remove Student")
        print("4. Add Lecturer")
        print("5. Remove Lecturer")
        print("6. Generate Reports")
        print("7. View All Data")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            add_course()
        elif choice == "2":
            add_new_student()
        elif choice == "3":
            delete_student()
        elif choice == "4":
            add_new_lecturer()
        elif choice == "5":
            delete_lecturer()
        elif choice == "6":
            generate_reports()
        elif choice == "7":
            view_all_data()
        elif choice == "8":
            print("Exiting Admin Menu.")
            break
        else:
            print("Invalid choice! Please select a valid option.")

# Main Function
def main():
    """Main program flow."""
    # Ensure necessary text files are created
    initialize_files()

    # Login status
    logged_in = False

    # Main loop
    while True:
        print("\n--- Main Menu ---")
        print("1. Admin Login")
        print("2. Exit Program")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            logged_in = admin_login()  # Prompt for admin login
            if logged_in:
                admin_menu()  # Access the admin menu upon successful login
        elif choice == "2":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice! Please enter a valid option.")

def read_data_from_file():
    # Reads student data from a csv file if it exists
    try:
        with open("student_records.csv", "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("ID: "):
                    parts = line.strip().split(", ")
                    student_id = parts[0].split(": ")[1]
                    paid = float(parts[1].split(": RM")[1])
                    outstanding = float(parts[2].split(": RM")[1])

                    student_ids.append(student_id)
                    paid_fees.append(paid)
                    outstanding_fees.append(outstanding)
    except FileNotFoundError:
        print("No previous records found. Starting fresh.")

def accountant_menu():
    # Displays a menu and processes user input
    while True:
        print("Menu:")
        print("1. Record Tuition Fees")
        print("2. View Outstanding Fees")
        print("3. Update Payment Records")
        print("4. Issue Fee Receipts")
        print("5. View Financial Summary")
        print("6. Save Data to Text File")
        print("7. Exit")
        userinput = input("Enter your choice: ")

        # Menu option handling
        if userinput == "1":
            student_id = input("Enter Student ID: ")
            tuition_fee = float(input("Enter Total Tuition Fee Amount: "))
            tuition_paid = float(input("Enter Amount Paid: "))
            record_tuition_fees(student_id, tuition_fee, tuition_paid)
        elif userinput == "2":
            view_outstanding_fees()
        elif userinput == "3":
            student_id = input("Enter Student ID: ")
            payment_amount = float(input("Enter Payment Amount: "))
            update_payment_records(student_id, payment_amount)
        elif userinput == "4":
            student_id = input("Enter Student ID: ")
            issue_fee_receipts(student_id)
        elif userinput == "5":
            view_financial_summary()
        elif userinput == "6":
            save_data_to_file()
        elif userinput == "7":
            print("Exiting program.")
            break  # Exit the program loop
        else:
            print("Invalid input. Please try again.")

def record_tuition_fees(student_id, tuition_fee, tuition_paid=0):
    # Records tuition fees for a student
    student_ids.append(student_id)
    paid_fees.append(tuition_paid)
    outstanding_fees.append(tuition_fee - tuition_paid)  # Calculate and store outstanding fees
    print("Tuition fee of RM", tuition_fee, " recorded for Student ID: ", student_id, ". Outstanding fee: RM", tuition_fee - tuition_paid, ".")

def view_outstanding_fees():
    # Displays all students with outstanding fees
    print("Outstanding Fees:")
    outstanding = False
    for i in range(len(student_ids)):
        if outstanding_fees[i] > 0:
            outstanding = True
            print("ID: ", student_ids[i], ", Outstanding: RM", outstanding_fees[i])
    if not outstanding:
        print("All fees are cleared.")

def update_payment_records(student_id, paid_amount):
    # Updates payment records and adjusts outstanding fees
    if student_id in student_ids:
        index = student_ids.index(student_id)
        outstanding_fees[index] -= paid_amount
        paid_fees[index] += paid_amount

        if outstanding_fees[index] < 0:
            print("Student has overpaid, outstanding fees is 0 now.")
            outstanding_fees[index] = 0
        elif outstanding_fees[index] > 0:
            print("Incomplete payment. RM", outstanding_fees[index], "is left.")
        else:
            print("Payment completed, there is no outstanding balance.")

        print("Payment of RM", paid_amount, " updated for Student ID: ", student_id, ".")
    else:
        print("Student ID not found.")

def issue_fee_receipts(student_id):
    # Issues a receipt for a specific student
    if student_id in student_ids:
        index = student_ids.index(student_id)
        print("Student ID: " + str(student_ids[index]))
        print("Total Paid: RM=" + str(paid_fees[index]))
        print("Outstanding: RM" + str(outstanding_fees[index]))
    else:
        print("Student ID not found.")

def view_financial_summary():
    # Summarizes total fees collected and outstanding fees
    total_paid = sum(paid_fees)
    total_outstanding = sum(outstanding_fees)
    print("Financial Summary:")
    print("Total Fees Paid: RM", total_paid)
    print("Total Outstanding Fees: RM", total_outstanding)

def save_data_to_file():
    # Saves student data to a text file
    with open("student_records.csv", "w") as file:
        file.write("Student Fee Records\n")
        for i in range(len(student_ids)):
            file.write(f"ID: {student_ids[i]}, Paid: RM{paid_fees[i]}, Outstanding: RM{outstanding_fees[i]}\n")
        file.write("\n")

        total_paid = sum(paid_fees)
        total_outstanding = sum(outstanding_fees)
        file.write("Financial Summary:\n")
        file.write(f"Total Paid: RM{total_paid}\n")
        file.write(f"Total Outstanding: RM{total_outstanding}\n")
    print("Data saved in student_fee_records.txt.")

def create_attendance_file(file_path, header, rows):
    """Creates the attendance CSV file."""
    with open(file_path, "w") as file:
        # Write header
        file.write(",".join(header) + "\n")
        # Write rows
        for row in rows:
            file.write(",".join(map(str, row)) + "\n")

create_attendance_file(ATTENDANCE_FILE, header, rows)

# Utility functions for file handling
def read_file(file_path):
    """Reads a file and returns its content as a list of lines."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []


def write_file(file_path, lines):
    """Overwrites a file with a list of lines."""
    with open(file_path, "w") as file:
        file.write("\n".join(lines) + "\n")


def append_to_file(file_path, line):
    """Appends a single line to a file."""
    with open(file_path, "a") as file:
        file.write(line + "\n")

# Lecturer functionalities
def view_assigned_modules():
    print("\nAssigned Modules:")
    modules = read_file(MODULES_FILE)
    if not modules:
        print("No modules assigned.")
        return
    for module in modules:
        print(module)


def view_student_list():
    print("\nStudent List:")
    enrollments = read_file(STUDENT_INFO)
    if not enrollments:
        print("No students enrolled in any module.")
        return

    module_students = {}
    for enrollment in enrollments:
        # Safely split the line and handle invalid formats
        parts = enrollment.split(",")
        if len(parts) != 2:  # Skip invalid lines
            print(f"{enrollment}")
            continue

        student_id, module_code = parts
        if module_code not in module_students:
            module_students[module_code] = []
        module_students[module_code].append(student_id)

    # Display the student list grouped by module
    for module_code, students in module_students.items():
        print(f"Module: {module_code}, Students: {', '.join(students)}")


def record_attendance():
    module_code = input("Enter the module code: ").strip()
    student_id = input("Enter the student ID: ").strip()
    attendance_percentage = input("Enter attendance percentage: ").strip()

    attendance = read_file(ATTENDANCE_FILE)
    updated_attendance = []
    found = False

    for record in attendance:
        record_student_id, record_module_code, _ = record.split(",")
        if record_student_id == student_id and record_module_code == module_code:
            updated_attendance.append(f"{student_id},{module_code},{attendance_percentage}")
            found = True
        else:
            updated_attendance.append(record)

    if not found:
        updated_attendance.append(f"{student_id},{module_code},{attendance_percentage}")

    write_file(ATTENDANCE_FILE, updated_attendance)
    print("Attendance recorded successfully.")


def view_student_grades():
    module_code = input("Enter the module code: ").strip()
    grades = read_file(GRADES_FILE)

    if not grades:
        print("No grades found.")
        return

    headers = grades[0].split(",")
    module_index = headers.index(module_code) if module_code in headers else None

    if module_index is None:
        print("Module not found in grades.")
        return

    print(f"Grades for module {module_code}:")
    for line in grades[1:]:
        row = line.split(",")
        student_id = row[0]
        grade = row[module_index] if module_index < len(row) else "N/A"
        print(f"Student ID: {student_id}, Grade: {grade}")


def record_grades():
    module_code = input("Enter the module code: ").strip()
    student_id = input("Enter the student ID: ").strip()
    grade = input("Enter the grade: ").strip()

    grades = read_file(GRADES_FILE)
    if not grades:
        print("No grades file found. Creating a new one.")
        grades = ["StudentID"]

    headers = grades[0].split(",")
    if module_code not in headers:
        headers.append(module_code)
        grades[0] = ",".join(headers)

    updated_grades = []
    found = False
    for line in grades[1:]:
        row = line.split(",")
        if row[0] == student_id:
            while len(row) < len(headers):
                row.append("N/A")
            row[headers.index(module_code)] = grade
            found = True
        updated_grades.append(",".join(row))

    if not found:
        new_row = [student_id] + ["N/A"] * (len(headers) - 1)
        new_row[headers.index(module_code)] = grade
        updated_grades.append(",".join(new_row))

    updated_grades.insert(0, ",".join(headers))
    write_file(GRADES_FILE, updated_grades)
    print("Grade recorded successfully.")

# Main menu for lecturer
def lecturer_menu():
    while True:
        print("\nLecturer Menu:")
        print("1. View Assigned Modules")
        print("2. View Student List")
        print("3. Record Attendance")
        print("4. View Student Grades")
        print("5. Record Grades")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            view_assigned_modules()
        elif choice == "2":
            view_student_list()
        elif choice == "3":
            record_attendance()
        elif choice == "4":
            view_student_grades()
        elif choice == "5":
            record_grades()
        elif choice == "6":
            print("Exiting Lecturer Menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Utility functions for file handling
def read_file(file_path):
    """Reads a file and returns its content as a list of lines."""
    try:
        with open(file_path, "r") as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []


def write_file(file_path, lines):
    """Overwrites a file with a list of lines."""
    with open(file_path, "w") as file:
        file.write("\n".join(lines) + "\n")


def append_to_file(file_path, line):
    """Appends a single line to a file."""
    with open(file_path, "a") as file:
        file.write(line + "\n")


def view_available_modules():
    print("\nAvailable Modules:")
    modules = read_file(MODULES_FILE)
    if not modules:
        print("No modules available.")
        return
    for module in modules:
        print(module)


def enroll_in_module(student_id):
    module_code = input("Enter the module code to enroll: ").strip()
    enrollments = read_file(ENROLLMENTS_FILE)

    # Check if already enrolled
    if any(enrollment == f"{student_id},{module_code}" for enrollment in enrollments):
        print("You are already enrolled in this module.")
        return

    # Enroll the student
    append_to_file(ENROLLMENTS_FILE, f"{student_id},{module_code}")
    print(f"Enrolled in module {module_code} successfully.")


def view_grades(student_id):
    print("\nYour Grades:")
    grades = read_file(GRADES_FILE)

    # Check if the file is empty or invalid
    if not grades:
        print("No grades found.")
        return

    # Extract headers (modules) and find the student row
    headers = grades[0].split(",")  # First row contains headers
    found = False
    for line in grades[1:]:
        row = line.split(",")
        if row[0] == student_id:  # Check if this is the correct student
            found = True
            print(f"Student ID: {student_id}")
            for i, module in enumerate(headers[1:], start=1):  # Skip the StudentID header
                grade = row[i] if i < len(row) else "N/A"  # Handle missing grades
                print(f"Module: {module}, Grade: {grade}")
            break

    if not found:
        print("No grades found for the given Student ID.")


def access_attendance_record(student_id):
    print("\nYour Attendance Record:")
    attendance = read_file(ATTENDANCE_FILE)
    found = False
    for record in attendance:
        record_student_id, module_code, attendance_percentage = record.split(",")
        if record_student_id == student_id:
            print(f"Module: {module_code if module_code else 'N/A'}, Attendance: {attendance_percentage}%")
            found = True
    if not found:
        print("No attendance records found.")


def unenroll_from_module(student_id):
    module_code = input("Enter the module code to unenroll: ").strip()
    enrollments = read_file(ENROLLMENTS_FILE)
    updated_enrollments = [
        enrollment for enrollment in enrollments if enrollment != f"{student_id},{module_code}"
    ]

    if len(enrollments) == len(updated_enrollments):
        print("You are not enrolled in this module.")
    else:
        write_file(ENROLLMENTS_FILE, updated_enrollments)
        print(f"Unenrolled from module {module_code} successfully.")


def validate_student_id(student_id):
    """Check if the student ID exists in the STUDENT_INFO file."""
    student_info = read_file(STUDENT_INFO)
    for record in student_info:
        # Split the record by commas into columns
        columns = record.split(",")
        if len(columns) > 1 and columns[1].strip() == student_id:  # Check the second column (Student ID)
            return True
    return False


def student_menu(student_id):
    while True:
        print("\nStudent Menu:")
        print("1. View Available Modules")
        print("2. Enroll in Module")
        print("3. View Grades")
        print("4. Access Attendance Record")
        print("5. Unenroll from Module")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            view_available_modules()
        elif choice == "2":
            enroll_in_module(student_id)
        elif choice == "3":
            view_grades(student_id)
        elif choice == "4":
            access_attendance_record(student_id)
        elif choice == "5":
            unenroll_from_module(student_id)
        elif choice == "6":
            print("Exiting Student Menu. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


while True:
    main_menu = int(input("-------------------------"
                          "\n1. Admin"
                          "\n2. Lecturer"
                          "\n3. Student"
                          "\n4. Registrar"
                          "\n5. Accountant"
                          "\n6. Exit"
                          "\n-------------------------"
                          "\n>"))

    if main_menu == 1:
        if __name__ == "__main__":
            main()
    elif main_menu == 2:
        if __name__ == "__main__":
            lecturer_menu()
    elif main_menu == 3:
        if __name__ == "__main__":
            while True:
                student_id = input("Enter your Student ID: ").strip()
                if validate_student_id(student_id):
                    student_menu(student_id)
                    break
                else:
                    print("Invalid Student ID. Please try again.")
    elif main_menu == 4:
        while True:
            option = int(input(
                "-------Please Choose Any Of The Following-------"  # This gives a menu to the user along with choices
                "\n1. Register New Student"
                "\n2. Remove Student"
                "\n3. Update Student Records"
                "\n4. Manage Enrolments"
                "\n5. Issue Transcripts"
                "\n6. View Student Information"
                "\n7. Exit"
                "\n------------------------------------------------"
                "\n>"))
            if option == 1:  # If user selects the 1st option it will run the new_stud function
                register = new_stud('students', 'StudInfo.csv')
            elif option == 2:
                remove_student('StudInfo.csv')
            elif option == 3:  # If the user selects the 2nd option it will run the update_stud function
                update_stud('StudInfo.csv')
            elif option == 4:  # If the user selects the 3rd option it will give them with another menu with 2 options
                while True:
                    num = int(input("Press 1 to enroll a student into a module"
                                    "\nPress 2 to check the enrolled modules for students."
                                    "\nPress 3 to Exit"
                                    "\n>"))
                    if num == 1:  # If the user selects the 1st option it will run the manage_enrollments function
                        manage_enrollments('StudInfo.csv', 'Modules.csv', 'Enrollments.csv')
                    if num == 2:  # If the user selects the 2nd option it will run the view_student_module function
                        view_student_modules('Enrollments.csv', 'Modules.csv')
                    if num == 3:
                        break
                    else:  # If any option thing is typed it will break the loop and take the user to the main menu
                        break
            elif option == 5:  # If the user selects the 4th option it will run the issue_transcript function
                issue_transcript('StudInfo.csv', 'Grades.csv', 'Modules.csv')
            elif option == 6:  # If the user selects the 5th option it will display another menu for the user
                while True:
                    stud = int(input("------------------------------------------------"
                                     "\nPress 1 to view a single students info"
                                     "\nPress 2 to view the entire database"
                                     "\n------------------------------------------------"
                                     "\n>"))
                    if stud == 1:  # If the user selects the 1st option it will run the display_stud finction
                        display_stud('StudInfo.csv')
                    elif stud == 2:  # If the user selects the 2nd option it will run the import_csv function
                        data = import_csv('StudInfo.csv')
                        for row in data:
                            print(data[row])
                    else:  # Any other input will cause the loop to break
                        print("Invalid Option Selected")
                    break
            elif option == 7:  # If the user selects the 6th option this will end the loops
                break
            else:  # Any other input except the ones listed will cause the loop to restart again with this prompt message
                print("Invalid Option!")
    elif main_menu == 5:
        read_data_from_file()
        accountant_menu()
    elif main_menu == 6:
        print("Ending the Program!")
        break
    else:
        print("Invalid Option Selected. Try Again!")