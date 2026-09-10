import requests


class ApiError(Exception):
    pass


class ApiClient:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")
        self.token = None
        self.role = None

    def _headers(self):
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(self, method, path, **kwargs):
        try:
            response = requests.request(
                method,
                self.base_url + path,
                headers=self._headers(),
                timeout=10,
                **kwargs,
            )
        except requests.RequestException as exc:
            raise ApiError(
                "Không kết nối được backend. Hãy chạy FastAPI tại http://127.0.0.1:8000 trước."
            ) from exc

        if not response.ok:
            try:
                body = response.json()
                detail = body.get("detail", body)
            except Exception:
                detail = response.text or f"HTTP {response.status_code}"
            raise ApiError(str(detail))

        if response.status_code == 204 or not response.content:
            return None
        return response.json()

    def get(self, path, params=None):
        return self.request("GET", path, params=params)

    def post_json(self, path, data=None):
        return self.request("POST", path, json=data or {})

    def put_json(self, path, data=None):
        return self.request("PUT", path, json=data or {})

    def post_form(self, path, data=None):
        return self.request("POST", path, data=data or {})
