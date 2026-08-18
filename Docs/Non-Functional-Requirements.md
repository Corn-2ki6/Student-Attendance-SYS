# Non-Functional Requirements

## I. Supplementary Specification

The following non-functional requirements describe the quality and constraints of the Student Attendance System.

---

## 1. Usability

- The system should provide a simple, clear, and easy-to-use interface for both students and lecturers.
- Users should be able to become familiar with the main functions of the system after several uses.
- The student attendance process should require only a few simple steps.
- The system should clearly display the current attendance status and the result of an attendance submission.
- The system should provide clear error messages when an operation cannot be completed.
- The interface should use consistent layouts, buttons, colors, icons, and navigation throughout the system.
- The interface should automatically adapt to different screen sizes (responsive design).
- The attendance check-in interface should be easy to use on mobile devices.

---

## 2. Reliability

- The system shall store attendance information accurately and consistently.
- The system shall prevent duplicate attendance records for the same student in the same attendance session.
- Successfully submitted attendance shall be stored and available for later viewing.
- If an error occurs during attendance submission, the system shall not create an invalid or incomplete attendance record.
- The attendance information displayed to students and lecturers should be consistent with the records stored in the system.
- The system should maintain attendance data when users log out or when an attendance session is closed.

---

## 3. Performance

- The system should respond quickly to common operations such as login, viewing classes, viewing schedules, and viewing attendance history.
- The system should process attendance submissions within an acceptable response time under normal operating conditions.
- The system should be able to handle multiple students submitting attendance at approximately the same time.
- The system should maintain acceptable performance when lecturers monitor the attendance of a class with many students.
- The attendance submission process should respond quickly enough for students to complete attendance within the allowed attendance period.

> Specific performance values such as the maximum number of concurrent users or exact response time can be added later if they are defined by the project requirements.

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
- Students can only view their own attendance information and attendance history.
- Students shall not be allowed to manually modify their own attendance records.
- Lecturers can only manage attendance for classes assigned to them.
- User passwords must not be stored as plain text.
- The system should use appropriate security measures to prevent common vulnerabilities such as SQL Injection and Cross-Site Scripting (XSS).
- The system must validate the attendance password before creating an attendance record.
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
- The system should minimize service interruptions during active attendance sessions.
- If the system becomes temporarily unavailable, it should provide an appropriate message to users instead of displaying an unclear system error.

---

## 8. Error Handling and Recovery

- The system shall provide clear error messages when an operation cannot be completed.
- The system shall not create duplicate attendance records when an error occurs during attendance submission.
- If an attendance submission fails, the student should be informed whether the attendance was successfully recorded or not.
- The system should prevent invalid data from being stored in the database.
- The system should handle invalid attendance passwords without creating an attendance record.
