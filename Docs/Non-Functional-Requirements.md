# Non-Functional Requirements

## I. Supplementary Specification

The following non-functional requirements describe the quality and constraints of the Student Attendance System.

---

## 1. Usability

- The system should provide a simple, clear, and easy-to-use interface for both students and lecturers.
- Users should be able to become familiar with the main functions of the system after several uses.
- A student should be able to complete a normal self-submit attendance process within **3 main steps**, excluding login and password entry when password-based attendance is required.
- The system should clearly display the current attendance status and the result of an attendance submission.
- The system should provide clear error messages when an operation cannot be completed.
- The interface should use consistent layouts, buttons, colors, icons, and navigation throughout the system.
- The interface should automatically adapt to different screen sizes (responsive design).
- The attendance check-in interface should be easy to use on mobile devices.

---

## 2. Reliability

- The system shall store attendance information accurately and consistently.
- The system shall prevent **100% of duplicate attendance records** for the same student in the same attendance session.
- At least **99% of valid attendance submissions** during testing should be recorded correctly under normal operating conditions.
- Successfully submitted attendance shall be stored and available for later viewing.
- If an error occurs during attendance submission, the system shall not create an invalid or incomplete attendance record.
- The attendance information displayed to students and lecturers should be consistent with the records stored in the system.
- The system should maintain attendance data when users log out or when an attendance session is closed.

---

## 3. Performance

- The system should respond to common operations such as login, viewing classes, viewing schedules, and viewing attendance history within **3 seconds** under normal testing conditions.
- At least **95% of valid attendance submissions** should receive a response within **3 seconds** under normal testing conditions.
- The system should successfully process at least **30 students submitting attendance within the same 10-second period** without data loss or duplicate attendance records.
- The system should maintain acceptable performance when lecturers monitor the attendance of a class with many students.
- The attendance monitoring page should display updated attendance information within **3 seconds** after a successful attendance submission.

> The above performance criteria are intended for the scope of a student project and do not represent production-level capacity requirements.

---

## 4. Supportability

- The system should be organized into separate modules to make the system easier to maintain and develop.
- Functions related to authentication, class management, attendance management, and reporting should be organized separately.
- The source code should use clear naming conventions and a consistent coding style.
- The database structure should be organized clearly to support maintenance and future expansion.
- The system should allow new attendance-related features to be added without significantly changing the existing system.
- The project documentation should be maintained together with the source code to help team members understand and maintain the system.

---

## 5. Security

- Users must log in before accessing functions that require authentication.
- The system shall identify the user's role after login and restrict access according to that role.
- **100% of tested unauthorized access attempts** shall be rejected.
- Students can only view their own attendance information and attendance history.
- Students shall not be allowed to manually modify their own attendance records.
- Lecturers can only manage attendance for classes assigned to them.
- User passwords must not be stored as plain text.
- The system should use appropriate security measures to prevent common vulnerabilities such as SQL Injection and Cross-Site Scripting (XSS).
- The system must validate the attendance password before creating an attendance record.
- **100% of tested invalid attendance passwords** shall be rejected without creating an attendance record.
- Users should only be able to access information and functions that they are authorized to use.

---

## 6. Design Constraints

- The system shall operate as a web-based application.
- The system shall support two main types of users:
  - Student
  - Lecturer
- The system shall support two attendance methods:
  - Self-submit attendance
  - Password-based attendance
- The system shall use a database to store information about students, lecturers, classes, attendance sessions, and attendance records.
- The system shall support responsive interfaces for different screen sizes.
- The system shall follow the attendance rules defined in the Functional Requirements.
- The specific programming languages, frameworks, database management systems, and server technologies will be defined after the technology stack is finalized.

---

## 7. Availability

- The system should be available during normal class hours so that students can submit attendance when an attendance session is open.
- During the testing period, the system should maintain at least **99% availability** during the defined operating period.
- The total system downtime should not exceed **15 minutes during a full day of testing**.
- The system should minimize service interruptions during active attendance sessions.
- If the system becomes temporarily unavailable, it should provide an appropriate message to users instead of displaying an unclear system error.

> The availability criteria are evaluated during the project's testing period and do not represent a 24/7 production service-level agreement.

---

## 8. Error Handling and Recovery

- The system shall provide clear error messages when an operation cannot be completed.
- If an attendance submission fails, the system shall inform the student whether the attendance was successfully recorded or not within **3 seconds** under normal operating conditions.
- The system shall not create duplicate attendance records when an error occurs during attendance submission.
- The system should prevent invalid data from being stored in the database.
- The system should handle invalid attendance passwords without creating an attendance record.
- The system should restore normal operation within **10 minutes** after a temporary service failure under normal operating conditions.

---

## 9. Acceptance Criteria

The following acceptance criteria define measurable conditions that can be verified during system testing.

### 9.1 Usability

- A student should be able to complete a normal self-submit attendance process within **3 main steps**, excluding login and password entry when password-based attendance is required.
- Error messages should be displayed within **3 seconds** after an invalid operation is detected.
- The interface should remain usable on the supported desktop and mobile screen sizes.

### 9.2 Reliability

- At least **99% of valid attendance submissions** during testing should be recorded correctly under normal operating conditions.
- The system shall create **0 duplicate attendance records** for the same student and attendance session.
- The system shall create **0 incomplete attendance records** as a result of a failed attendance submission.
- Successfully recorded attendance data shall remain available after logout and after the corresponding attendance session is closed.

### 9.3 Performance

- At least **95% of common user operations** such as login, viewing classes, viewing schedules, and viewing attendance history should complete within **3 seconds** under normal testing conditions.
- At least **95% of valid attendance submissions** should receive a response within **3 seconds** under normal testing conditions.
- The system should successfully process at least **30 students submitting attendance within the same 10-second period** without data loss or duplicate attendance records.
- The attendance monitoring page should display updated attendance information within **3 seconds** after a successful attendance submission.

### 9.4 Availability

- During the testing period, the system should maintain at least **99% availability** during the defined operating period.
- The total system downtime should not exceed **15 minutes during a full day of testing**.
- When the system is temporarily unavailable, it should display a clear error or maintenance message instead of an unhandled system error.

### 9.5 Security

- **100% of tested unauthorized access attempts** shall be rejected.
- Students shall not be able to access another student's attendance information in **any tested case**.
- Lecturers shall not be able to manage attendance for classes that are not assigned to them in **any tested case**.
- **100% of tested invalid attendance passwords** shall be rejected without creating an attendance record.
- User passwords shall never be stored as plain text.
- The system shall pass all defined security test cases for basic SQL Injection and Cross-Site Scripting (XSS) protection.

### 9.6 Attendance Session

- **100% of tested attendance sessions** shall initially have the status **Scheduled** after creation.
- **100% of tested attendance sessions** shall automatically change from **Scheduled** to **Open** when the scheduled start time is reached.
- **100% of tested manual close operations** performed by authorized lecturers shall successfully change an **Open** session to **Closed**.
- If a lecturer does not manually close the session, **100% of tested attendance sessions** shall automatically change to **Closed** when the scheduled end time is reached.
- Students shall be unable to submit attendance for a **Scheduled** or **Closed** session in **100% of tested cases**.
- When a session is closed, **100% of students who have not submitted attendance** shall be marked as **Absent**.

### 9.7 Attendance Status

- **100% of successful self-submit attendance tests** shall create a **Present** attendance record.
- **100% of tested cases** where a lecturer manually marks a student as **Late** shall result in the **Late** status.
- A student who has not submitted attendance while the session is **Open** shall remain **Pending**.
- **100% of tested Pending records** shall become **Absent** when the corresponding session is closed.
- The system shall prevent a student from submitting attendance more than once for the same attendance session in **100% of tested cases**.

### 9.8 Attendance Percentage

- The attendance percentage shall be calculated correctly in **100% of tested calculation cases**.
- The calculation shall follow:

  **Attendance Percentage = Present Records / Completed Attendance Sessions × 100**

- **Late** and **Absent** records shall not be counted as **Present** in **100% of tested cases**.
- Attendance sessions with status **Scheduled** or **Open** shall not be included in the completed attendance session total.
