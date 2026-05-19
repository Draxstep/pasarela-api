from fastapi import FastAPI

from app.api.gateway_routes import router as gateway_router
from app.api.tesoreria_routes import router as tesoreria_router

app = FastAPI(title="Pasarela Pago Service", version="0.1.0")

app.include_router(gateway_router)
app.include_router(tesoreria_router)
