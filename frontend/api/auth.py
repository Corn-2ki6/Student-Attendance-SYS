from api.client import ApiError


class AuthApi:
    def __init__(self, client):
        self.client = client

    def login(self, username, password):
        token = self.client.post_form(
            "/api/auth/login",
            {
                "username": username,
                "password": password,
            },
        )

        self.client.token = token["access_token"]

        me = self.client.get(
            "/api/auth/me"
        )

        self.client.role = me.get("role")

        return me

    def me(self):
        return self.client.get(
            "/api/auth/me"
        )

    def logout(self):
        try:
            if self.client.token:
                self.client.post_json(
                    "/api/auth/logout"
                )
        except Exception:
            pass
        finally:
            self.client.token = None
            self.client.role = None

    # ============================================================
    # REGISTER STUDENT
    # ============================================================

    def register_student(
        self,
        full_name,
        email,
        username,
        password,
    ):
        return self.client.post_json(
            "/api/auth/register",
            {
                "fullName": full_name,
                "email": email,
                "username": username,
                "password": password,
            },
        )

    # ============================================================
    # FORGOT PASSWORD
    # ============================================================

    def forgot_password(
        self,
        username,
        email,
    ):
        return self.client.post_json(
            "/api/auth/forgot-password",
            {
                "username": username,
                "email": email,
            },
        )

    # ============================================================
    # RESET PASSWORD
    # ============================================================

    def reset_password(
        self,
        username,
        reset_token,
        new_password,
    ):
        return self.client.post_json(
            "/api/auth/reset-password",
            {
                "username": username,
                "reset_token": reset_token,
                "newPassword": new_password,
            },
        )