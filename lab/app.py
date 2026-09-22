from fastapi import FastAPI, Header, HTTPException
from typing import Optional
from pydantic import BaseModel

app = FastAPI(title="API Lab", version="1.0.0")

db = {
    1: {"id": 1, "owner": "user_a", "data": "Secret Order A"},
    2: {"id": 2, "owner": "user_b", "data": "Secret Order B"}
}

class SearchQuery(BaseModel):
    query: str

@app.get("/api/orders/{id}")
def get_order(id: int, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Token")
    token = authorization.split(" ")[1] if " " in authorization else authorization
    if id not in db:
        raise HTTPException(status_code=404, detail="Not Found")
    order = db[id]
    if token not in ["token-a", "token-b"]:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return {"order": order}

@app.get("/api/public")
def get_public():
    return {"message": "Hello World"}

# --- TÍNH NĂNG MỚI BỔ SUNG ---

# BFLA Endpoint: Chỉ dành cho Admin, nhưng quên kiểm tra role
@app.get("/api/admin/users")
def get_all_users(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Token")
    token = authorization.split(" ")[1] if " " in authorization else authorization
    # Lỗ hổng BFLA: Token thường (token-a, token-b) vẫn lấy được dữ liệu Admin
    if token not in ["token-a", "token-b", "token-admin"]:
        raise HTTPException(status_code=401, detail="Invalid Token")
    return {"admin_data": "Đây là danh sách người dùng bảo mật của hệ thống"}

# Input Validation Endpoint: Gửi payload rác vào để test
@app.post("/api/search")
def search_items(payload: SearchQuery):
    q = payload.query.upper()
    # Máy chủ cố tình bị crash (lỗi 500) nếu bị ném payload chứa SQLi hoặc XSS
    if "DROP TABLE" in q or "<SCRIPT>" in q or len(q) > 1000 or "%" in q:
        raise HTTPException(status_code=500, detail="Internal Server Error - Crashed by malicious input")
    return {"results": f"Found items for {payload.query}"}
