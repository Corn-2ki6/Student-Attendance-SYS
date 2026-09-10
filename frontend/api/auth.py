class AuthApi:
    def __init__(self, client):
        self.client = client

    def login(self, username, password):
        # Backend GitHub dùng OAuth2PasswordRequestForm => x-www-form-urlencoded.
        token = self.client.post_form(
            "/api/auth/login",
            {"username": username, "password": password},
        )
        self.client.token = token["access_token"]
        me = self.client.get("/api/auth/me")
        self.client.role = me.get("role")
        return me

    def me(self):
        return self.client.get("/api/auth/me")

    def logout(self):
        try:
            self.client.post_json("/api/auth/logout")
        finally:
            self.client.token = None
            self.client.role = None

    def forgot_password(self, username, email):
        return self.client.post_json(
            "/api/auth/forgot-password",
            {"username": username, "email": email},
        )

    def reset_password(self, username, reset_token, new_password):
        return self.client.post_json(
            "/api/auth/reset-password",
            {
                "username": username,
                "reset_token": reset_token,
                "newPassword": new_password,
            },
        )
