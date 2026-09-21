import json
from lab.app import app

openapi_schema = app.openapi()
with open("lab/openapi.json", "w", encoding="utf-8") as f:
    json.dump(openapi_schema, f, indent=4)
print("Dumped openapi.json")
