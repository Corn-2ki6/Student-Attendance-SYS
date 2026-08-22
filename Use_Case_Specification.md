# Use Case Specification

---

## 1. Use Case Diagram

### 1.1. Actor List

| No. | Actor | Description |
| :---: | :--- | :--- |
| **1** | Student | A user who participates in classes and performs attendance check-in. |
| **2** | Lecturer | A user who manages classes and attendance activities. |

### 1.2. Use Case List

| No. | Use Case | Description | Group |
| :---: | :--- | :--- | :--- |
| **1** | Login | Authenticate and access the system | Common |
| **2** | Log out | Sign out of the system | Common |
| **3** | Forgot Password | Recover a forgotten password | Common |
| **4** | View Profile | View personal account information | Common |
| **5** | View Dashboard | View the system dashboard | Common |
| **6** | View Classes | View the list of classes | Common |
| **7** | View Schedule | View the class schedule | Student |
| **8** | Check Attendance | Record attendance | Student |
| **9** | Enter Attendance Password | Enter the attendance password | Student |
| **10** | View Attendance History | View attendance history | Student |
| **11** | View Attendance Percentage | View the attendance percentage | Student |
| **12** | View Student List | View the list of enrolled students | Lecturer |
| **13** | Create Attendance Session | Create an attendance session | Lecturer |
| **14** | Configure Attendance | Configure attendance settings | Lecturer |
| **15** | Monitor Attendance | Monitor attendance in real time | Lecturer |
| **16** | Update Attendance | Update attendance records | Lecturer |
| **17** | Close Attendance | Close an attendance session | Lecturer |
| **18** | View Attendance Report | View attendance reports | Lecturer |

---

## 2. Use Case: Login

### 2.1. Summary
This use case describes how a user (Student/Lecturer) logs in to the Student Attendance System.

### 2.2. Flow of Events
#### 2.2.1. Main Flow
1. The use case begins when a user wants to log in to the system.
2. The system prompts the user to enter a username (email address or identification number) and password.
3. The user enters the credentials and submits the login request.
4. The system validates the credentials. If they are correct, the system authenticates the user and redirects them to the Dashboard corresponding to their role.

#### 2.2.2. Alternative Flows
##### 2.2.2.1. Invalid Login Credentials
If the user enters an incorrect username or password, the system displays an error message. The user may re-enter the credentials or select the Forgot Password option.

### 2.3. Special Requirements
None.

### 2.4. Precondition
The user is not authenticated.

### 2.5. Postcondition
If the login is successful, the user is authenticated and logged in to the system. Otherwise, the system state remains unchanged.

### 2.6. Extension Points
None.

---

## 3. Use Case: Log out

### 3.1. Summary
This use case allows a user to log out of the system.

### 3.2. Flow of Events
#### 3.2.1. Main Flow
1. The user selects the Log out function.
2. The system terminates the user's active session.
3. The system redirects the user to the Login page.

#### 3.2.2. Alternative Flows
None.

### 3.3. Special Requirements
None.

### 3.4. Precondition
The user is authenticated and has an active session.

### 3.5. Postcondition
The user is no longer authenticated and is returned to the guest state.

### 3.6. Extension Points
None.

---

## 4. Use Case: Forgot Password

### 4.1. Summary
This use case allows a user to recover a forgotten password.

### 4.2. Flow of Events
#### 4.2.1. Main Flow
1. The user selects the Forgot Password function.
2. The system prompts the user to enter the email address associated with the account.
3. The user enters the email address and confirms the request.
4. The system verifies the email address, generates a password-reset link, and sends the link to the specified email address.
5. The system notifies the user that the password-reset email has been sent successfully.

#### 4.2.2. Alternative Flows
##### 4.2.2.1. Email Address Not Found
If the email address does not exist in the system, the system displays an error message. The user may enter another email address.

### 4.3. Special Requirements
The password-reset link is valid only for a limited period (e.g., 15 minutes).

### 4.4. Precondition
The user is not authenticated.

### 4.5. Postcondition
If successful, the password-recovery email is sent. The user's authentication state remains unchanged.

### 4.6. Extension Points
None.

---

## 5. Use Case: View Profile

### 5.1. Summary
This use case allows a user to view their personal information.

### 5.2. Flow of Events
#### 5.2.1. Main Flow
1. The user selects the View Profile function.
2. The system retrieves the user's information from the database.
3. The system displays information such as full name, identification number, email address, faculty/major, and other relevant information.

#### 5.2.2. Alternative Flows
None.

### 5.3. Special Requirements
None.

### 5.4. Precondition
The user is authenticated.

### 5.5. Postcondition
The system state remains unchanged.

### 5.6. Extension Points
None.

---

## 6. Use Case: View Dashboard

### 6.1. Summary
This use case allows a user to view an overview dashboard after logging in.

### 6.2. Flow of Events
#### 6.2.1. Main Flow
1. The user successfully logs in or selects the logo/home page.
2. The system aggregates key information:
   - **For students:** Today's classes and overall attendance percentage.
   - **For lecturers:** Classes being taught and today's teaching schedule.
3. The system displays the Dashboard.

#### 6.2.2. Alternative Flows
None.

### 6.3. Special Requirements
None.

### 6.4. Precondition
The user is authenticated.

### 6.5. Postcondition
The system state remains unchanged.

### 6.6. Extension Points
None.

---

## 7. Use Case: View Classes

### 7.1. Summary
This use case allows a user to view the list of classes in which they are enrolled or which they teach.

### 7.2. Flow of Events
#### 7.2.1. Main Flow
1. The user selects the View Classes function.
2. The system retrieves the classes associated with the user.
3. The system displays a list containing the class code, course name, lecturer, and semester.

#### 7.2.2. Alternative Flows
None.

### 7.3. Special Requirements
None.

### 7.4. Precondition
The user is authenticated.

### 7.5. Postcondition
The system state remains unchanged.

### 7.6. Extension Points
None.

---

## 8. Use Case: View Schedule

### 8.1. Summary
This use case allows a student to view their course schedule by week or month.

### 8.2. Flow of Events
#### 8.2.1. Main Flow
1. The student selects the View Schedule function.
2. The system retrieves the student's class schedule based on the selected/current time period.
3. The system displays the schedule in a tabular format, including course, time, and classroom.

#### 8.2.2. Alternative Flows
None.

### 8.3. Special Requirements
None.

### 8.4. Precondition
The student is authenticated.

### 8.5. Postcondition
The system state remains unchanged.

### 8.6. Extension Points
None.

---

## 9. Use Case: Check Attendance

### 9.1. Summary
This use case allows a student to record attendance and confirm their presence in a class.

### 9.2. Flow of Events
#### 9.2.1. Main Flow
1. The student selects the attendance function for an ongoing class.
2. The system verifies whether the attendance session is currently open.
3. The system displays the attendance interface. If the attendance session requires a password, the system prompts the student to enter it.
4. The student enters the password, if required, and submits the attendance request.
5. The system validates the password, if applicable. If valid, the system records the student's attendance status as "Present" together with the attendance timestamp.
6. The system displays a success notification confirming that attendance has been recorded.

#### 9.2.2. Alternative Flows
##### 9.2.2.1. Attendance Session Not Open or Already Closed
If the attendance session has not been opened or has expired, the system displays an error message and terminates the use case.

##### 9.2.2.2. Invalid Attendance Password
If the attendance session requires a password and the student enters an incorrect password, the system displays an error message and prompts the student to enter the password again.

### 9.3. Special Requirements
None.

### 9.4. Precondition
The student is authenticated.

### 9.5. Postcondition
The student's attendance status is updated in the database.

### 9.6. Extension Points
The `Enter Attendance Password` use case is integrated directly into the Main Flow.

---

## 10. Use Case: Enter Attendance Password

### 10.1. Summary
This use case describes how a student enters the attendance password when an attendance session requires password-based verification.

### 10.2. Flow of Events
#### 10.2.1. Main Flow
1. During Step 3 of the `Check Attendance` use case, the system detects that the attendance session is password-protected.
2. The system displays a password input field.
3. The student enters the password and selects Confirm.
4. The system validates the password and proceeds with recording the student's attendance.

#### 10.2.2. Alternative Flows
##### 10.2.2.1. Invalid Password
The system displays an error indicating that the password is incorrect. The student must re-enter the password.

### 10.3. Special Requirements
None.

### 10.4. Precondition
The student is in the process of executing the `Check Attendance` use case.

### 10.5. Postcondition
If the password is valid, the system returns to the `Check Attendance` use case to complete the attendance process.

### 10.6. Extension Points
None.

---

## 11. Use Case: View Attendance History

### 11.1. Summary
This use case allows a student to review detailed attendance records for previous class sessions of a specific course.

### 11.2. Flow of Events
#### 11.2.1. Main Flow
1. The student selects the View Attendance History function for a specific course.
2. The system retrieves attendance data for previous class sessions.
3. The system displays a list of class sessions together with attendance statuses: Present, Absent, or Late.

#### 11.2.2. Alternative Flows
None.

### 11.3. Special Requirements
None.

### 11.4. Precondition
The student is authenticated.

### 11.5. Postcondition
The system state remains unchanged.

### 11.6. Extension Points
None.

---

## 12. Use Case: View Attendance Percentage

### 12.1. Summary
This use case calculates and displays the percentage of attended class sessions relative to the total number of class sessions.

### 12.2. Flow of Events
#### 12.2.1. Main Flow
1. The student selects the attendance statistics function.
2. The system calculates the attendance percentage using the following formula: `(Number of Present Sessions / Total Number of Sessions Held) * 100`.
3. The system displays the attendance percentage as a chart or numerical value.

#### 12.2.2. Alternative Flows
None.

### 12.3. Special Requirements
If the attendance percentage falls below the required threshold (e.g., below 80%), the system may highlight the value in red as a warning.

### 12.4. Precondition
The student is authenticated.

### 12.5. Postcondition
The system state remains unchanged.

### 12.6. Extension Points
None.

---

## 13. Use Case: View Student List

### 13.1. Summary
This use case allows a lecturer to view all students enrolled in a class.

### 13.2. Flow of Events
#### 13.2.1. Main Flow
1. The lecturer opens a class and selects the View Student List function.
2. The system retrieves the class enrollment data.
3. The system displays a list containing student identification numbers, full names, and enrollment status (e.g., active, withdrawn).

#### 13.2.2. Alternative Flows
None.

### 13.3. Special Requirements
None.

### 13.4. Precondition
The lecturer is authenticated.

### 13.5. Postcondition
The system state remains unchanged.

### 13.6. Extension Points
None.

---

## 14. Use Case: Create Attendance Session

### 14.1. Summary
This use case allows a lecturer to create and open an attendance session for students.

### 14.2. Flow of Events
#### 14.2.1. Main Flow
1. The lecturer selects the function to create an attendance session for a class.
2. The system prompts the lecturer to specify the session configuration, including the start time, end time, and whether an attendance password is required.
3. The lecturer enters the required information and submits the creation request.
4. The system creates and opens the attendance session and displays a success notification.

#### 14.2.2. Alternative Flows
##### 14.2.2.1. Invalid Configuration
If the end time is earlier than the start time, the system displays an error message.

### 14.3. Special Requirements
None.

### 14.4. Precondition
The lecturer is authenticated.

### 14.5. Postcondition
A new attendance session is created.

### 14.6. Extension Points
None.

---

## 15. Use Case: Configure Attendance

### 15.1. Summary
This use case allows a lecturer to modify the configuration parameters of an attendance session that is currently open or scheduled to open.

### 15.2. Flow of Events
#### 15.2.1. Main Flow
1. The lecturer selects an attendance session and chooses the Configure function.
2. The system displays the current configuration parameters, such as the session time and password.
3. The lecturer modifies the required parameters (e.g., extends the session by 5 minutes) and saves the changes.
4. The system updates the session configuration and displays a success notification.

#### 15.2.2. Alternative Flows
None.

### 15.3. Special Requirements
None.

### 15.4. Precondition
The lecturer is authenticated and has access to manage the class.

### 15.5. Postcondition
The attendance session configuration is updated.

### 15.6. Extension Points
None.

---

## 16. Use Case: Monitor Attendance

### 16.1. Summary
This use case allows a lecturer to monitor, in real time, the number and list of students who have recorded attendance while an attendance session is open.

### 16.2. Flow of Events
#### 16.2.1. Main Flow
1. The lecturer opens the Attendance Monitoring interface for an ongoing attendance session.
2. The system continuously updates the list of students who have submitted their attendance.
3. The system displays the current attendance count: Number of students who have recorded attendance / Total number of students.

#### 16.2.2. Alternative Flows
None.

### 16.3. Special Requirements
The system updates the attendance list whenever new attendance data is submitted.

### 16.4. Precondition
The lecturer is authenticated and the attendance session is open.

### 16.5. Postcondition
The system state remains unchanged.

### 16.6. Extension Points
None.

---

## 17. Use Case: Update Attendance

### 17.1. Summary
This use case allows a lecturer to manually modify a student's attendance status (e.g., from Absent to Present or Late).

### 17.2. Flow of Events
#### 17.2.1. Main Flow
1. The lecturer selects the attendance records for a class session.
2. The lecturer locates the student whose attendance record needs to be modified and changes the attendance status (e.g., from Absent to Present).
3. The lecturer selects Save.
4. The system updates the attendance status in the database and displays a success notification.

#### 17.2.2. Alternative Flows
None.

### 17.3. Special Requirements
The system may maintain an audit log recording when the lecturer modified an attendance record for auditing purposes.

### 17.4. Precondition
The lecturer is authenticated.

### 17.5. Postcondition
The student's attendance status is updated in the system.

### 17.6. Extension Points
None.

---

## 18. Use Case: Close Attendance

### 18.1. Summary
This use case allows a lecturer to manually close an attendance session before its configured end time.

### 18.2. Flow of Events
#### 18.2.1. Main Flow
1. The lecturer selects an open attendance session and selects the Close button.
2. The system prompts the lecturer to confirm the action.
3. The lecturer confirms the closure.
4. The system changes the session status to "Closed", after which students can no longer record attendance.

#### 18.2.2. Alternative Flows
None.

### 18.3. Special Requirements
All students who have not recorded attendance at the time of closure are automatically assigned the "Absent" status by the system.

### 18.4. Precondition
The attendance session is in the Open state.

### 18.5. Postcondition
The attendance session status is changed to Closed.

### 18.6. Extension Points
None.

---

## 19. Use Case: View Attendance Report

### 19.1. Summary
This use case allows a lecturer to view an overall attendance report and statistics for a class.

### 19.2. Flow of Events
#### 19.2.1. Main Flow
1. The lecturer selects the View Attendance Report function for a class.
2. The system aggregates attendance data from all class sessions.
3. The system displays a list of students together with the number of absences, number of attendances, and attendance percentage. The lecturer may export the report as an Excel or PDF file.

#### 19.2.2. Alternative Flows
None.

### 19.3. Special Requirements
None.

### 19.4. Precondition
The lecturer is authenticated.

### 19.5. Postcondition
The system state remains unchanged.

### 19.6. Extension Points
None.
