# Use Case Specification

## 1. Use Case Diagram

### 1.1. List of Actors

| No. | Actor | Description |
| :---: | :--- | :--- |
| **1** | **Student** | Student attending classes and performing attendance check-ins. |
| **2** | **Lecturer** | Instructor managing classes and attendance sessions. |

### 1.2. List of Use Cases

| No. | Use Case | Description | Category / Note |
| :---: | :--- | :--- | :--- |
| **1** | Login | Log in to the system | General |
| **2** | Log out | Log out of the system | General |
| **3** | Forgot Password | Recover account password | General |
| **4** | View Profile | View personal information | General |
| **5** | View Classes | View enrolled/taught class list | General |
| **6** | View Schedule | View class timetable | Student |
| **7** | Submit Attendance | Perform attendance check-in | Student |
| **8** | Enter Attendance Password | Enter password for attendance check-in | Student |
| **9** | View Attendance History | View detailed attendance history | Student |
| **10** | View Attendance Percentage | View overall attendance rate/percentage | Student |
| **11** | View Student List | View class roster / student list | Lecturer |
| **12** | Create Attendance Session | Create a new attendance session | Lecturer |
| **13** | Configure Attendance | Configure attendance session settings | Lecturer |
| **14** | Monitor Attendance | Monitor live attendance in real-time | Lecturer |
| **15** | Update Attendance | Manually update attendance records | Lecturer |
| **16** | Close Attendance | Close an active attendance session | Lecturer |
| **17** | View Attendance Report | View and export attendance summary reports | Lecturer |

---

## 2. Use-case Login

### 2.1. Brief Description
This use case describes how a user (Student/Lecturer) logs into the Student Attendance System.

### 2.2. Flow of Events

#### 2.2.1. Basic Flow
1. The use case begins when a user wishes to log into the system.
2. The system prompts the user to enter their username (email or ID) and password.
3. The user inputs credentials and submits the login request.
4. The system validates the credentials. If valid, the system grants access and redirects the user to the Dashboard corresponding to their role.

#### 2.2.2. Alternative Flows
##### 2.2.2.1. Invalid Login Credentials
If the user inputs an incorrect username or password, the system displays an error message. The user may retry or select the "Forgot Password" option.

### 2.3. Special Requirements
None.

### 2.4. Preconditions
The user is currently unauthenticated (not logged in).

### 2.5. Postconditions
If successful, the user is authenticated and logged into the system. Otherwise, the system state remains unchanged.

### 2.6. Extension Points
None.

---

## 3. Use-case Log out

### 3.1. Brief Description
This use case allows an authenticated user to log out of the system.

### 3.2. Flow of Events

#### 3.2.1. Basic Flow
1. The user selects the Log Out function.
2. The system invalidates the active user session.
3. The system redirects the user to the Login page.

#### 3.2.2. Alternative Flows
None.

### 3.3. Special Requirements
None.

### 3.4. Preconditions
The user is currently logged into the system.

### 3.5. Postconditions
The user is returned to an unauthenticated (guest) state.

### 3.6. Extension Points
None.

---

## 4. Use-case Forgot Password

### 4.1. Brief Description
This use case allows users to recover or reset their password when forgotten.

### 4.2. Flow of Events

#### 4.2.1. Basic Flow
1. The user selects the Forgot Password option.
2. The system prompts for the email address linked to the account.
3. The user inputs their email address and confirms.
4. The system validates the email address, generates a password reset link, and sends it to the specified email.
5. The system displays a notification confirming that the email has been sent successfully.

#### 4.2.2. Alternative Flows
##### 4.2.2.1. Email Address Not Found
If the entered email does not exist in the system database, the system displays an error message. The user can enter a different email address.

### 4.3. Special Requirements
The password reset link remains valid for a restricted time window only (e.g., 15 minutes).

### 4.4. Preconditions
The user is not logged in.

### 4.5. Postconditions
If successful, a password recovery email is dispatched. The user authentication status remains unchanged.

### 4.6. Extension Points
None.

---

## 5. Use-case View Profile

### 5.1. Brief Description
This use case enables users to view their personal profile details.

### 5.2. Flow of Events

#### 5.2.1. Basic Flow
1. The user selects the View Profile function.
2. The system retrieves profile information from the database.
3. The system displays profile details, including: Full Name, Student/Staff ID, Email, Department/Major, etc.

#### 5.2.2. Alternative Flows
None.

### 5.3. Special Requirements
None.

### 5.4. Preconditions
The user is logged in.

### 5.5. Postconditions
The system state remains unchanged.

### 5.6. Extension Points
None.

---

## 6. Use-case View Classes

### 6.1. Brief Description
This use case allows users to view the list of classes in which they are enrolled or assigned to teach.

### 6.2. Flow of Events

#### 6.2.1. Basic Flow
1. The user selects the View Classes function.
2. The system retrieves the list of associated classes for the logged-in user.
3. The system displays class information including: Class Code, Course Name, Instructor/Lecturer, and Semester.

#### 6.2.2. Alternative Flows
None.

### 6.3. Special Requirements
None.

### 6.4. Preconditions
The user is logged in.

### 6.5. Postconditions
The system state remains unchanged.

### 6.6. Extension Points
None.

---

## 7. Use-case View Schedule

### 7.1. Brief Description
This use case allows students to view their course timetable on a weekly or monthly basis.

### 7.2. Flow of Events

#### 7.2.1. Basic Flow
1. The student selects the View Schedule function.
2. The system fetches schedule data matching the student's active semester and timeframe.
3. The system displays the timetable in a structured grid/table format, including: Course Name, Time Slot, and Classroom.

#### 7.2.2. Alternative Flows
None.

### 7.3. Special Requirements
None.

### 7.4. Preconditions
The student is logged in.

### 7.5. Postconditions
The system state remains unchanged.

### 7.6. Extension Points
None.

---

## 8. Use-case Check Attendance

### 8.1. Brief Description
This use case allows Students to complete check-in to confirm their presence in an active class session.

### 8.2. Flow of Events

#### 8.2.1. Basic Flow
1. The student selects the attendance check-in option for an active class.
2. The system verifies whether an attendance session is currently open.
3. The system displays the check-in interface. If the session requires a password, the system prompts the student for input.
4. The student enters the password (if applicable) and submits the check-in request.
5. The system validates the password (if applicable). If valid, the system records "Present" status and the submission timestamp.
6. The system notifies the student of successful attendance check-in.

#### 8.2.2. Alternative Flows
##### 8.2.2.1. Attendance Session Not Open or Closed
If the attendance session has not started or has already expired/closed, the system displays an error message. The use case terminates.

##### 8.2.2.2. Incorrect Attendance Password
If a password is required and the student enters an incorrect password, the system displays an error notification and prompts re-entry.

### 8.3. Special Requirements
None.

### 8.4. Preconditions
The student is logged in.

### 8.5. Postconditions
The student's attendance record is updated in the database.

### 8.6. Extension Points
Use-case **Enter Attendance Password**: (Integrated directly into the Basic Flow).

---

## 9. Use-case Enter Attendance Password

### 9.1. Brief Description
This use case specifies the detailed step where a student inputs an attendance password when session security is enabled.

### 9.2. Flow of Events

#### 9.2.1. Basic Flow
1. At Step 3 of the **Check Attendance** use case, the system detects that the attendance session requires a password.
2. The system renders a password input field.
3. The student inputs the password and clicks Confirm.
4. The system validates the password and continues processing the check-in request.

#### 9.2.2. Alternative Flows
##### 9.2.2.1. Incorrect Password
The system displays an error message indicating password mismatch. The student must re-enter the password.

### 9.3. Special Requirements
None.

### 9.4. Preconditions
The student is actively performing the **Check Attendance** flow.

### 9.5. Postconditions
Returns to finalize **Check Attendance** upon successful password verification.

### 9.6. Extension Points
None.

---

## 10. Use-case View Attendance History

### 10.1. Brief Description
This use case allows students to review detailed historical attendance records for each enrolled course.

### 10.2. Flow of Events

#### 10.2.1. Basic Flow
1. The student selects the View Attendance History option for a specific course.
2. The system retrieves historical session records.
3. The system displays a list of completed class sessions alongside status indicators: Present, Absent, or Late.

#### 10.2.2. Alternative Flows
None.

### 10.3. Special Requirements
None.

### 10.4. Preconditions
The student is logged in.

### 10.5. Postconditions
The system state remains unchanged.

### 10.6. Extension Points
None.

---

## 11. Use-case View Attendance Percentage

### 11.1. Brief Description
This use case calculates and displays the student's attendance percentage relative to the total number of conducted sessions.

### 11.2. Flow of Events

#### 11.2.1. Basic Flow
1. The student selects the Attendance Statistics view.
2. The system computes: `(Attended Sessions / Total Conducted Sessions) * 100`.
3. The system presents the attendance rate via chart visualizations or numerical indicators.

#### 11.2.2. Alternative Flows
None.

### 11.3. Special Requirements
If the attendance percentage drops below a defined threshold (e.g., under 80%), the system highlights the metric in red as a warning indicator.

### 11.4. Preconditions
The student is logged in.

### 11.5. Postconditions
The system state remains unchanged.

### 11.6. Extension Points
None.

---

## 12. Use-case View Student List

### 12.1. Brief Description
This use case allows lecturers to view the complete roster of students registered in a specific class.

### 12.2. Flow of Events

#### 12.2.1. Basic Flow
1. The lecturer navigates to a class view and selects View Student List.
2. The system retrieves class enrollment records.
3. The system displays the student roster including: Student ID, Full Name, and Enrollment Status (e.g., Active, Withdrawn).

#### 12.2.2. Alternative Flows
None.

### 12.3. Special Requirements
None.

### 12.4. Preconditions
The lecturer is logged in.

### 12.5. Postconditions
The system state remains unchanged.

### 12.6. Extension Points
None.

---

## 13. Use-case Create Attendance Session

### 13.1. Brief Description
This use case allows Lecturers to create and activate an attendance session for a class.

### 13.2. Flow of Events

#### 13.2.1. Basic Flow
1. The lecturer selects Create Attendance Session for a target class.
2. The system prompts for session parameters (start time, end time, password requirement).
3. The lecturer submits the session configuration.
4. The system opens the attendance session and returns a confirmation message.

#### 13.2.2. Alternative Flows
##### 13.2.2.1. Invalid Configuration
If the specified end time is earlier than or equal to the start time, the system displays a configuration error message.

### 13.3. Special Requirements
None.

### 13.4. Preconditions
The lecturer is logged in.

### 13.5. Postconditions
A new attendance session is created and activated in the system database.

### 13.6. Extension Points
None.

---

## 14. Use-case Configure Attendance

### 14.1. Brief Description
This use case allows lecturers to modify parameter settings for an open or scheduled attendance session.

### 14.2. Flow of Events

#### 14.2.1. Basic Flow
1. The lecturer selects an active or upcoming session and chooses Configure.
2. The system displays current session settings (expiration time, security password).
3. The lecturer updates the parameters (e.g., extending duration by 5 minutes) and saves changes.
4. The system updates the session configuration and notifies success.

#### 14.2.2. Alternative Flows
None.

### 14.3. Special Requirements
None.

### 14.4. Preconditions
The lecturer is logged in and managing the class.

### 14.5. Postconditions
The attendance session configuration is updated in the database.

### 14.6. Extension Points
None.

---

## 15. Use-case Monitor Attendance

### 15.1. Brief Description
This use case allows lecturers to track real-time check-in submissions and live headcount while an attendance session is active.

### 15.2. Flow of Events

#### 15.2.1. Basic Flow
1. The lecturer opens the Live Attendance Monitor interface for an active session.
2. The system dynamically updates the list of students who have completed check-in.
3. The system displays live metrics: Checked-in Students / Total Enrolled Students.

#### 15.2.2. Alternative Flows
None.

### 15.3. Special Requirements
The system auto-refreshes or streams attendance updates in real time as new check-in records are created.

### 15.4. Preconditions
The lecturer is logged in, and an attendance session is currently open.

### 15.5. Postconditions
The system state remains unchanged.

### 15.6. Extension Points
None.

---

## 16. Use-case Update Attendance

### 16.1. Brief Description
This use case allows lecturers to manually override or edit student attendance records (e.g., changing status from Absent to Present, Late, etc.).

### 16.2. Flow of Events

#### 16.2.1. Basic Flow
1. The lecturer opens attendance records for a specific session.
2. The lecturer locates the target student and modifies their attendance status (e.g., changing Absent to Present).
3. The lecturer clicks Save.
4. The system updates the record in the database and returns a success confirmation.

#### 16.2.2. Alternative Flows
None.

### 16.3. Special Requirements
The system records audit logs capturing timestamp, modifier ID, and prior values for compliance and tracking.

### 16.4. Preconditions
The lecturer is logged in.

### 16.5. Postconditions
The student's attendance status is updated in the system.

### 16.6. Extension Points
None.

---

## 17. Use-case Close Attendance

### 17.1. Brief Description
This use case allows lecturers to manually terminate an active attendance session before its scheduled expiration time.

### 17.2. Flow of Events

#### 17.2.1. Basic Flow
1. The lecturer selects an active attendance session and clicks Close Session.
2. The system prompts for action confirmation.
3. The lecturer confirms closure.
4. The system changes session status to "Closed", preventing further student check-in submissions.

#### 17.2.2. Alternative Flows
None.

### 17.3. Special Requirements
All enrolled students who have not checked in prior to closing are automatically marked as "Absent" by the system.

### 17.4. Preconditions
The attendance session is in "Open" status.

### 17.5. Postconditions
The attendance session transitions to "Closed" status.

### 17.6. Extension Points
None.

---

## 18. Use-case View Attendance Report

### 18.1. Brief Description
This use case allows lecturers to generate and review aggregate attendance statistics and reports for an entire class.

### 18.2. Flow of Events

#### 18.2.1. Basic Flow
1. The lecturer selects View Attendance Report for a target class.
2. The system aggregates attendance statistics across all completed class sessions.
3. The system displays a summary table with student names, total absences, attended sessions, and attendance percentage (%). The lecturer can choose to Export File (Excel/PDF).

#### 18.2.2. Alternative Flows
None.

### 18.3. Special Requirements
None.

### 18.4. Preconditions
The lecturer is logged in.

### 18.5. Postconditions
The system state remains unchanged.

### 18.6. Extension Points
None.
