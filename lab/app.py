from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="API Lab", version="1.0.0")

# Database giả lập
# User A có token 'token-a', sở hữu order 1
# User B có token 'token-b', sở hữu order 2
db = {
    1: {"id": 1, "owner": "user_a", "data": "Secret Order A"},
    2: {"id": 2, "owner": "user_b", "data": "Secret Order B"}
}

@app.get("/api/orders/{id}")
def get_order(id: int, authorization: str = Header(None)):
    if not authorization:
        # Lỗi: Missing Auth -> Nhưng lỡ dev code quên chặn nếu không có token sẽ bị lọt
        # Để test auth_rules, ta giả lập endpoint này CÓ CHẶN auth
        raise HTTPException(status_code=401, detail="Missing Token")
    
    token = authorization.split(" ")[1] if " " in authorization else authorization
    
    if id not in db:
        raise HTTPException(status_code=404, detail="Not Found")
        
    order = db[id]
    
    # Lỗi BOLA: Dev quên kiểm tra chủ sở hữu order!
    # Nếu token hợp lệ là được xem, bất kể chủ sở hữu
    if token not in ["token-a", "token-b"]:
        raise HTTPException(status_code=401, detail="Invalid Token")
        
    return {"order": order}

@app.get("/api/public")
def get_public():
    return {"message": "Hello World"}
