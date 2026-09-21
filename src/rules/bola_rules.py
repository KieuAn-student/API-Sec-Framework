class BOLARules:
    @staticmethod
    def check_bola(engine, endpoint, payload, profile_a_token, profile_b_token, object_id_a):
        # Sửa path nếu có tham số {id}
        path = endpoint.path.replace("{id}", str(object_id_a))
        
        # User B truy cập Object của User A
        headers = {"Authorization": f"Bearer {profile_b_token}"}
        resp = engine.send_request(endpoint.method, path, headers=headers, json_data=payload)
        
        if resp.status_code in [200, 201, 204]:
            return {
                "vulnerability": "BOLA / IDOR",
                "severity": "Critical",
                "endpoint": endpoint.path,
                "evidence": f"User B successfully accessed User A's object {object_id_a}. Status {resp.status_code}."
            }
        return None
