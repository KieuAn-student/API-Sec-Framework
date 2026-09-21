import httpx
from typing import Dict, Any

class HTTPEngine:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.client = httpx.Client(timeout=10.0)
    
    def send_request(self, method: str, path: str, headers: dict = None, params: dict = None, json_data: dict = None) -> httpx.Response:
        url = f"{self.base_url}{path}"
        # Default headers
        req_headers = {"Content-Type": "application/json"}
        if headers:
            req_headers.update(headers)
            
        try:
            response = self.client.request(
                method=method,
                url=url,
                headers=req_headers,
                params=params,
                json=json_data
            )
            return response
        except Exception as e:
            # Fake response for timeout/error
            return httpx.Response(status_code=0, request=httpx.Request(method, url))
