class BFLARules:
    @staticmethod
    def check_bfla(engine, endpoint, payload, normal_user_token):
        # BFLA tập trung test các tính năng của Admin
        if "admin" in endpoint.path.lower():
            headers = {"Authorization": f"Bearer {normal_user_token}"}
            resp = engine.send_request(endpoint.method, endpoint.path, headers=headers, json=payload)
            
            # Nếu User bình thường gọi API admin mà vẫn trả về 200/201 -> Lỗi BFLA
            if resp and resp.status_code in [200, 201]:
                return {
                    "vulnerability": "BFLA (Broken Function Level Authorization)",
                    "severity": "Critical",
                    "endpoint": endpoint.path,
                    "evidence": f"Normal user token successfully accessed an Admin function. Status: {resp.status_code}"
                }
        return None
