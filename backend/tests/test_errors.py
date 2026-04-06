class TestErrorHandlerFormat:
    """DoD PASO 1: Forzar 404 y 422, ambas respuestas cumplen estructura oficial."""

    def test_404_format(self, client):
        resp = client.get("/api/v1/this-route-does-not-exist")
        assert resp.status_code == 404
        body = resp.get_json()
        assert "error" in body
        assert body["error"]["code"] == "NOT_FOUND"
        assert isinstance(body["error"]["message"], str)
        assert body["error"]["details"] == {}

    def test_422_format(self, client):
        resp = client.get("/_test/force-422")
        assert resp.status_code == 422
        body = resp.get_json()
        assert "error" in body
        assert body["error"]["code"] == "BUSINESS_RULE_ERROR"
        assert isinstance(body["error"]["message"], str)
        assert body["error"]["details"] == {}
