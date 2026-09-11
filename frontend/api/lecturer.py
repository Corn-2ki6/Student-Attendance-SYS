class LecturerApi:
    def __init__(self, client):
        self.client = client

    # =========================
    # LECTURER
    # =========================

    def profile(self):
        return self.client.get("/api/lecturers/me")

    # =========================
    # CLASSES
    # =========================

    def classes(self):
        return self.client.get("/api/lecturers/me/classes")

    def class_students(self, class_id):
        return self.client.get(
            f"/api/lecturers/classes/{int(class_id)}/students"
        )

    # =========================
    # ATTENDANCE SESSIONS
    # =========================

    def sessions(
        self,
        class_id=None,
        session_date=None,
        status=None,
    ):
        params = {}

        if class_id is not None:
            params["class_id"] = class_id

        if session_date:
            params["session_date"] = session_date

        if status:
            params["status"] = status

        return self.client.get(
            "/api/lecturers/me/sessions",
            params=params,
        )

    def create_session(
        self,
        class_id,
        session_date,
        start_time,
        end_time,
        attendance_method,
        attendance_password=None,
    ):
        data = {
            "classID": int(class_id),
            "sessionDate": session_date,
            "startTime": start_time,
            "endTime": end_time,
            "attendanceMethod": attendance_method,
            "attendancePassword": attendance_password or None,
        }

        return self.client.post_json(
            "/api/attendance/sessions",
            data,
        )

    def open_session(self, session_id):
        return self.client.post_json(
            f"/api/attendance/sessions/{int(session_id)}/open"
        )

    def records(self, session_id):
        return self.client.get(
            f"/api/attendance/sessions/{int(session_id)}/records"
        )

    def update_attendance(
        self,
        attendance_id,
        status,
        remark=None,
    ):
        data = {
            "status": status,
            "remark": remark or None,
        }

        return self.client.put_json(
            f"/api/attendance/records/{int(attendance_id)}",
            data,
        )

    def close_session(self, session_id):
        return self.client.post_json(
            f"/api/attendance/sessions/{int(session_id)}/close"
        )

    def report(self, session_id):
        return self.client.get(
            f"/api/attendance/sessions/{int(session_id)}/report"
        )

    # =========================
    # CHANGE PASSWORD
    # =========================

    def change_password(
        self,
        current_password,
        new_password,
    ):
        return self.client.put_json(
            "/api/lecturers/me/password",
            {
                "currentPassword": current_password,
                "newPassword": new_password,
            },
        )