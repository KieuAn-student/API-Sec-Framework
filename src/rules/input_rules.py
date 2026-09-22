class InputValidationRules:
    @staticmethod
    def check_input_validation(engine, endpoint, payload):
        findings = []
        # Danh sách 10 quy tắc fuzzing (10 input validation rules)
        fuzz_payloads = [
            ("SQL Injection 1", "' OR '1'='1"),
            ("SQL Injection 2", "1; DROP TABLE users"),
            ("XSS Attack", "<script>alert(1)</script>"),
            ("Path Traversal", "../../../../etc/passwd"),
            ("Command Injection", "& whoami"),
            ("Buffer Overflow (Long String)", "A" * 5000),
            ("Format String", "%s%s%s%s%s"),
            ("Negative Integer Bypass", "-99999"),
            ("Boolean Mismatch", "true"),
            ("Special Characters", "!@#$%^&*()_+<>?:{}|~")
        ]
        
        # Thử fuzzing vào body nếu endpoint có yêu cầu body
        if endpoint.method.upper() in ['POST', 'PUT'] and endpoint.request_body:
            for rule_name, bad_data in fuzz_payloads:
                # Ghi đè giá trị rác vào tham số đầu tiên của body
                fuzzed_payload = payload.copy() if payload else {}
                if fuzzed_payload:
                    first_key = list(fuzzed_payload.keys())[0]
                    fuzzed_payload[first_key] = bad_data
                else:
                    fuzzed_payload = {"query": bad_data} # Fallback
                
                resp = engine.send_request(endpoint.method, endpoint.path, json=fuzzed_payload)
                
                # Nếu server trả về 500 nghĩa là không xử lý được input rác -> Lỗi Input Validation
                if resp and resp.status_code == 500:
                    findings.append({
                        "vulnerability": f"Input Validation Flaw ({rule_name})",
                        "severity": "High",
                        "endpoint": endpoint.path,
                        "evidence": f"Server crashed or returned 500 when sent malicious payload: {bad_data[:20]}..."
                    })
        return findings
