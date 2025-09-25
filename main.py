# ===============================
# Chapter 1: FastAPI Setup
# ===============================
# This chapter sets up the FastAPI application and routes for SEA-SEC.
from fastapi import FastAPI
from app.routes import router  # ✅ This line will fail if imports are broken

app = FastAPI(title="SEA-SEC Test", version="0.0.1")

# ===============================
# Chapter 2: Router Attachment
# ===============================
# Attach router from app/routes.py
app.include_router(router)

# ===============================
# Chapter 3: Health Check Endpoint
# ===============================
@app.get("/buzz")
def ping():
    return {"message": "Ding Dong!"}
