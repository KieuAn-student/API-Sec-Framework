import json
import os

class FindingManager:
    def __init__(self):
        self.findings = []
        
    def add_finding(self, finding):
        if finding and finding not in self.findings:
            self.findings.append(finding)
            
    def export_report(self, path="report.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"total_findings": len(self.findings), "findings": self.findings}, f, indent=4)
