from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from presentation.routes import health, auth, stock

app = FastAPI(
    title="InvestFolio API",
    description="資産管理システムのバックエンドAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(stock.router)

@app.get("/")
async def root():
    return {"message": "InvestFolio API is running", "version": "1.0.0"}