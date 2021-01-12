import json

studentsData = json.load(open("sample_students.json"))
authenticationData = json.load(open("authentication_details.json"))

# The user is not authenticated by default and therefore must login
isAuthenticated = False

# By default, when the report menu is selected, the report menu should open
inReportMenu = True


# Print text with a border
def prettyPrint(text):
    print("#" * (len(text) + 4))
    print("# " + text + " #")
    print("#" * (len(text) + 4))
    print(" ")


def authenticate():
    global isAuthenticated
    _username = input("Username: ")

    usernames = [user for user in authenticationData["details"]
                 if user["username"] == _username]

    if len(usernames) == 0:
        print("That is not the correct username!")
        return authenticate()

    _password = input("Password: ")

    passwords = [user for user in authenticationData["details"]
                 if user["password"] == _password]

    if len(passwords) == 0:
        print("That is not the right password for " + _username)
        return authenticate()

    isAuthenticated = True


def addStudent():
    UUID = len(studentsData["students"])
    surname = input("Student surname: ")
    forename = input("Student forename: ")
    print("Student date of birth")
    DOB = [int(input("Day: ")), int(input("Month: ")), int(input("Year: "))]
    address = input("Student address: ")
    number = input("Student phone number: ")
    gender = input("Student gender: ")
    group = input("Student tutor group: ")
    email = forename[0] + surname[0] + "@treeroad.edu"

    studentsData["students"].append({
        "UUID": UUID,
        "surname": surname,
        "forename": forename,
        "DOB": DOB,
        "address": address,
        "number": number,
        "gender": gender,
        "group": group,
        "email": email
    })

    # Save this new dict
    with open("sample_students.json", "w") as file_:
        json.dump(studentsData, file_, indent=4)


def printStudent(student):
    print(" ")
    print("Displaying information for student with ID: " +
          str(student["UUID"]))
    print("Forename: " + student["forename"])
    print("Surname: " + student["surname"])
    dob = student["DOB"]
    print("Date of birth: {0}/{1}/{2}".format(dob[0], dob[1], dob[2]))
    print("Address: " + student["address"])
    print("Number: " + student["number"])
    print("Gender: " + student["gender"])
    print("Tutor group: " + student["group"])
    print("Email: " + student["email"])


def viewStudent():
    _studentID = int(input("Student ID: "))

    studentIds = [student for student in studentsData["students"]
                  if student["UUID"] == _studentID]

    if len(studentIds) == 0:
        print("There is no student with this ID!")
        return viewStudent()

    # print the first student with this ID
    printStudent(studentIds[0])


def filterStudents(comparator, value):
    return [student for student in studentsData["students"] if student[value].lower() == comparator]


def reportMenu():
    global inReportMenu
    print(" ")
    print("Generate reports for:")
    print("1. Student tutor group")
    print("2. Student birth month")
    print("3. Student gender")
    print("-- 4. Exit menu")
    selection = int(input("Menu selection: "))
    students = {}
    if selection == 1:
        tutorGroup = input("Tutor Group: ").lower()
        students = filterStudents(tutorGroup, "group")
    elif selection == 2:
        birthMonth = int(input("Birth Month (1-12): "))
        students = [student for student in studentsData["students"]
                    if student["DOB"][1] == birthMonth]
    elif selection == 3:
        gender = input("Gender: ").lower()
        students = filterStudents(gender, "gender")
    elif selection == 4:
        inReportMenu = False
        return

    if len(students) == 0:
        print("There are no students with this report type!")
        reportMenu()

    # Print all filtered students
    for x in students:
        print("[ID: {0}] {1} {2}".format(
            x["UUID"], x["forename"], x["surname"]))


# ---------- Menu -----------------

prettyPrint("Tree Road School Staff Menu")

while True:
    if not isAuthenticated:
        authenticate()
    else:
        print("1: Add new student")
        print("2: Select student by ID")
        print("3: Generate reports")
        print("4: Log out")
        print(" ")

        menuSelection = int(input("Selection: "))

        if menuSelection == 1:  # Add new student
            addStudent()
        elif menuSelection == 2:  # Select student
            viewStudent()
        elif menuSelection == 3:  # Enter report menu
            while inReportMenu:
                reportMenu()
        elif menuSelection == 4:  # Log out
            isAuthenticated = False

        print(" ")
