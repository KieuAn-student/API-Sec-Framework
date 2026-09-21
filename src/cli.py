import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.parser import OpenAPIParser
from src.core.generator import BaselineGenerator
from src.core.engine import HTTPEngine
from src.rules.auth_rules import AuthRules
from src.rules.bola_rules import BOLARules
from src.analyzer.analyzer import FindingManager

def main():
    print("=== REST API Security Testing Framework ===")
    spec_path = "lab/openapi.json"
    if not os.path.exists(spec_path):
        print(f"File {spec_path} không tồn tại. Vui lòng chạy API Lab trước để có file specs.")
        return

    # 1. Parse
    parser = OpenAPIParser(spec_path)
    inventory = parser.parse()
    print(f"[*] Đã load {len(inventory.endpoints)} endpoints từ '{inventory.title}'.")

    # 2. Engine
    engine = HTTPEngine("http://127.0.0.1:8000")
    manager = FindingManager()

    # 3. Test Rules
    print("[*] Bắt đầu quét lỗ hổng...")
    for ep in inventory.endpoints:
        if "/api/orders" in ep.path:
            # Sinh dữ liệu
            payload = BaselineGenerator.generate_from_schema(ep.request_body)
            
            # Test Auth
            finding_auth = AuthRules.check_missing_auth(engine, ep, payload)
            if finding_auth: manager.add_finding(finding_auth)
            
            # Test BOLA (Token B truy cập Order 1 của Token A)
            finding_bola = BOLARules.check_bola(engine, ep, payload, "token-a", "token-b", 1)
            if finding_bola: manager.add_finding(finding_bola)

    # 4. Report
    manager.export_report("report.json")
    print(f"[*] Quét hoàn tất. Tìm thấy {len(manager.findings)} lỗ hổng.")
    print("[*] Kết quả được lưu tại report.json")

if __name__ == '__main__':
    main()
