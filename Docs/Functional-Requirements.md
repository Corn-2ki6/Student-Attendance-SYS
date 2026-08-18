# Functional Requirements

## I. Student Attendance System

The Student Attendance System is a web-based system designed to help lecturers manage student attendance and allow students to submit and track their attendance.

The system has two main types of users:

- **Student**
- **Lecturer**

The system provides the following basic functions:

---

### 1. Login and Logout

- Students and lecturers can log in to the system using their account and password.
- After a successful login, the system identifies the user's role and displays the appropriate interface:
  - Students are directed to the Student interface.
  - Lecturers are directed to the Lecturer interface.
- If the account or password is incorrect, the system displays an error message and asks the user to try again.
- Users can log out of the system.

---

### 2. Student Functions

#### 2.1 View Class Information

- Students can view the classes in which they are enrolled.
- For each class, the system displays basic information, including:
  - Course name
  - Class code
  - Lecturer
  - Class schedule
  - Classroom

#### 2.2 View Class Schedule

- Students can view their class schedule.
- The schedule displays:
  - Class date
  - Course or class name
  - Start time
  - End time
  - Classroom
  - Lecturer

#### 2.3 Submit Attendance

- When a lecturer opens an attendance session, students can submit their attendance for that session.
- Students can only submit attendance when the attendance session is **Open**.
- The system supports two attendance methods:

**a. Self-submit attendance**

- If the lecturer does not require a password, students can directly select the attendance function to submit their attendance.
- If the submission is successful, the system records the student's attendance.

**b. Password-based attendance**

- If the lecturer requires a password, students must enter the attendance password provided by the lecturer.
- The system checks the entered password.
- If the password is correct, the system records the student's attendance.
- If the password is incorrect, the system displays an error message and does not record the attendance.

#### 2.4 View Attendance History

- Students can view their previous attendance records.
- For each attendance record, the system can display:
  - Date
  - Course or class
  - Attendance status
  - Check-in time
  - Attendance method

The attendance status can be:

- **Present:** The student attended the class.
- **Late:** The student attended after the defined attendance time.
- **Absent:** The student did not attend the class.
- **Pending:** The attendance has not been confirmed or recorded yet.

#### 2.5 View Attendance Percentage

- Students can view their attendance percentage for each course.
- The system calculates the attendance percentage based on the recorded attendance sessions.

#### 2.6 View Personal Information

- Students can view their personal information.
- The information may include:
  - Student ID
  - Full name
  - Date of birth
  - Gender
  - Email
  - Major

---

### 3. Lecturer Functions

#### 3.1 View Class List

- Lecturers can view the classes they are responsible for.
- For each class, the system displays:
  - Course name
  - Class code
  - Class schedule
  - Classroom
  - Number of students

#### 3.2 View Student List

- Lecturers can view the list of students enrolled in a selected class.
- The list may display:
  - Student ID
  - Student name
  - Attendance status
  - Check-in time

#### 3.3 Create Attendance Session

- Lecturers can create an attendance session for a class they are responsible for.
- When creating an attendance session, the lecturer can set:
  - Class
  - Date
  - Start time
  - End time
  - Attendance method

#### 3.4 Open and Close Attendance Session

- Lecturers can open an attendance session so that students can submit their attendance.
- When the session is open, students in that class can submit attendance.
- Lecturers can close the attendance session after the attendance period ends.
- When the attendance session is closed, students can no longer submit new attendance records.

#### 3.5 Configure Attendance Password

- Lecturers can choose whether an attendance password is required for an attendance session.
- If a password is required, the system allows the lecturer to create or generate an attendance password.
- The lecturer provides the password to students so that they can submit their attendance.

#### 3.6 Monitor Attendance

- During an open attendance session, lecturers can monitor the attendance status of students.
- The system displays the attendance status of students, including:
  - Present
  - Late
  - Absent
  - Pending
- The system can also display the number of students in each attendance status.

#### 3.7 Update Attendance Status

- Lecturers can manually update a student's attendance status when necessary.
- For example, a lecturer can change:
  - Pending to Present
  - Present to Late
  - Absent to Present

#### 3.8 View Attendance Report

- Lecturers can view attendance information for their classes.
- The attendance report may include:
  - Total number of students
  - Number of Present students
  - Number of Late students
  - Number of Absent students
  - Attendance percentage
  - Attendance history of individual students

---

### 4. Attendance Rules

The system follows the following rules:

- A student can only submit attendance when the attendance session is **Open**.
- A student can only submit attendance **once for each attendance session**.
- If an attendance session requires a password, the student must enter the correct password.
- If the password is incorrect, the system does not record the attendance.
- If an attendance session does not require a password, the student can submit attendance directly.
- When an attendance session is closed, students cannot submit new attendance records.
- A lecturer can only manage attendance for classes assigned to that lecturer.
- Students cannot manually change their own attendance status.
- Each successful attendance submission creates an attendance record containing the student, attendance session, status, check-in time, and attendance method.
