class AuthRules:
    @staticmethod
    def check_missing_auth(engine, endpoint, payload):
        # Không truyền token
        resp = engine.send_request(endpoint.method, endpoint.path, headers={}, json_data=payload)
        if resp.status_code in [200, 201, 204]:
            return {
                "vulnerability": "Broken Authentication (Missing Token)",
                "severity": "High",
                "endpoint": endpoint.path,
                "evidence": f"Status {resp.status_code} when requesting without token."
            }
        return None
