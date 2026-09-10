class AttendanceApi:
    def __init__(self, client):
        self.client = client

    def history(self):
        return self.client.get("/api/attendance/me/history")

    def percentage(self):
        return self.client.get("/api/attendance/me/percentage")

    def submit(self, session_id, password=None):
        return self.client.post_json(
            f"/api/attendance/sessions/{int(session_id)}/submit",
            {"password": password or None},
        )
