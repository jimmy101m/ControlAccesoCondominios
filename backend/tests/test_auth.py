import pytest


class TestLogin:
    def test_login_success(self, client, active_user):
        resp = client.post("/api/v1/auth/login", json={
            "email": active_user["email"],
            "password": active_user["password"],
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert "token" in data
        assert data["token_type"] == "Bearer"
        assert "expires_in" in data
        user = data["user"]
        assert user["email"] == active_user["email"]
        assert "id" in user
        assert "full_name" in user
        assert "role" in user
        assert "status" in user

    def test_login_wrong_password(self, client, active_user):
        resp = client.post("/api/v1/auth/login", json={
            "email": active_user["email"],
            "password": "wrongpassword",
        })
        assert resp.status_code == 401
        assert resp.get_json()["error"]["code"] == "UNAUTHORIZED"

    def test_login_unknown_email(self, client):
        resp = client.post("/api/v1/auth/login", json={
            "email": "nobody@example.com",
            "password": "somepassword",
        })
        assert resp.status_code == 401
        assert resp.get_json()["error"]["code"] == "UNAUTHORIZED"

    def test_login_inactive_user(self, client, inactive_user):
        resp = client.post("/api/v1/auth/login", json={
            "email": inactive_user["email"],
            "password": inactive_user["password"],
        })
        assert resp.status_code == 401
        assert resp.get_json()["error"]["code"] == "UNAUTHORIZED"

    def test_login_missing_fields(self, client):
        resp = client.post("/api/v1/auth/login", json={})
        assert resp.status_code == 400
        assert resp.get_json()["error"]["code"] == "VALIDATION_ERROR"


class TestMe:
    def _get_token(self, client, active_user):
        resp = client.post("/api/v1/auth/login", json={
            "email": active_user["email"],
            "password": active_user["password"],
        })
        return resp.get_json()["token"]

    def test_me_success(self, client, active_user):
        token = self._get_token(client, active_user)
        resp = client.get("/api/v1/auth/me",
                          headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        assert "user" in resp.get_json()

    def test_me_no_token(self, client):
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    def test_me_invalid_token(self, client):
        resp = client.get("/api/v1/auth/me",
                          headers={"Authorization": "Bearer invalidtoken"})
        assert resp.status_code == 401


class TestLogout:
    def _get_token(self, client, active_user):
        resp = client.post("/api/v1/auth/login", json={
            "email": active_user["email"],
            "password": active_user["password"],
        })
        return resp.get_json()["token"]

    def test_logout_success(self, client, active_user):
        token = self._get_token(client, active_user)
        resp = client.post("/api/v1/auth/logout",
                           headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["ok"] is True
        assert data["message"] == "Sesion cerrada"

    def test_me_after_logout_is_401(self, client, active_user):
        token = self._get_token(client, active_user)
        client.post("/api/v1/auth/logout",
                    headers={"Authorization": f"Bearer {token}"})
        resp = client.get("/api/v1/auth/me",
                          headers={"Authorization": f"Bearer {token}"})
        assert resp.status_code == 401
        assert resp.get_json()["error"]["code"] == "TOKEN_REVOKED"
