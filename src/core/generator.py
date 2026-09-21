import random
import string
from typing import Dict, Any

class BaselineGenerator:
    @staticmethod
    def generate_from_schema(schema: dict) -> Any:
        if not schema:
            return {}
        
        # Lấy type của schema
        schema_type = schema.get("type", "object")
        
        if schema_type == "object":
            properties = schema.get("properties", {})
            result = {}
            for key, prop_schema in properties.items():
                result[key] = BaselineGenerator.generate_from_schema(prop_schema)
            return result
        elif schema_type == "string":
            return "test_string_" + ''.join(random.choices(string.ascii_lowercase, k=5))
        elif schema_type == "integer" or schema_type == "number":
            return random.randint(1, 100)
        elif schema_type == "boolean":
            return True
        elif schema_type == "array":
            items = schema.get("items", {})
            return [BaselineGenerator.generate_from_schema(items)]
        
        return "unknown"
