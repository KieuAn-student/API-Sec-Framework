from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict, Any, Optional

class Parameter(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    name: str
    in_: str = Field(alias="in")
    required: bool = False
    schema_definition: Optional[Dict[str, Any]] = Field(default=None, alias="schema")

class Endpoint(BaseModel):
    path: str
    method: str
    summary: Optional[str] = ""
    parameters: List[Parameter] = []
    request_body: Optional[Dict[str, Any]] = None
    responses: Dict[str, Any] = {}
    security: Optional[List[Dict[str, List[str]]]] = None

class APIInventory(BaseModel):
    title: str
    version: str
    servers: List[Dict[str, str]] = []
    endpoints: List[Endpoint] = []
