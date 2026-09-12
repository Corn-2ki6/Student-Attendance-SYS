class StudentApi:
    def __init__(self, client):
        self.client = client

    def profile(self):
        return self.client.get("/api/students/me")

    def classes(self):
        return self.client.get("/api/students/me/classes")

    def schedule(self):
        return self.client.get("/api/students/me/schedule")

    def change_password(self, current_password, new_password):
        return self.client.put_json(
            "/api/students/me/password",
            {
                "currentPassword": current_password,
                "newPassword": new_password,
            },
        )
