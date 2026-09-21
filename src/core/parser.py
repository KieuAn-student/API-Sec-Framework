import yaml
import json
import jsonref
from pathlib import Path
from src.core.models import APIInventory, Endpoint, Parameter

class OpenAPIParser:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.spec = self._load_spec()
    
    def _load_spec(self) -> dict:
        with open(self.file_path, 'r', encoding='utf-8') as f:
            if self.file_path.suffix in ['.yaml', '.yml']:
                raw_dict = yaml.safe_load(f)
            else:
                raw_dict = json.load(f)
        
        # Sử dụng jsonref để tự động phân giải các $ref trong OpenAPI spec
        json_str = json.dumps(raw_dict)
        return jsonref.loads(json_str)
    
    def parse(self) -> APIInventory:
        info = self.spec.get("info", {})
        servers = self.spec.get("servers", [])
        paths = self.spec.get("paths", {})
        global_security = self.spec.get("security", [])
        
        endpoints = []
        for path, path_items in paths.items():
            # Parameters định nghĩa ở cấp độ path được dùng chung cho mọi methods
            path_level_params = path_items.get("parameters", [])
            
            for method, details in path_items.items():
                if method.lower() not in ['get', 'post', 'put', 'delete', 'patch']:
                    continue
                
                # Gom chung parameters của path và method
                raw_params = details.get("parameters", [])
                raw_params.extend(path_level_params)
                
                parameters = []
                for p in raw_params:
                    # jsonref đã resolve nên p ở đây là một dict thay vì 
                    parameters.append(Parameter(
                        name=p.get("name"),
                        in_=p.get("in"),
                        required=p.get("required", False),
                        schema=p.get("schema", {})
                    ))
                
                endpoint = Endpoint(
                    path=path,
                    method=method.upper(),
                    summary=details.get("summary", ""),
                    parameters=parameters,
                    request_body=details.get("requestBody", {}),
                    responses=details.get("responses", {}),
                    security=details.get("security", global_security)
                )
                endpoints.append(endpoint)
                
        return APIInventory(
            title=info.get("title", "Unknown API"),
            version=info.get("version", "1.0.0"),
            servers=servers,
            endpoints=endpoints
        )

if __name__ == '__main__':
    print('Parser module ready.')
