import time
import uuid

import structlog
from fastapi import FastAPI, Request

from app.api.gateway_routes import router as gateway_router
from app.api.tesoreria_routes import router as tesoreria_router
from app.core.logging import configure_logging

configure_logging()
logger = structlog.get_logger(__name__)

app = FastAPI(
	title="Pasarela Pago Service",
	version="1.0.0",
	description=(
		"API de pasarela de pagos y tesoreria. Permite procesar cobros, "
		"consultar reportes de deuda y ejecutar liquidaciones masivas."
	),
	contact={"name": "Equipo Backend", "email": "backend@example.com"},
	openapi_tags=[
		{
			"name": "gateway",
			"description": "Orquestacion de cobros y validaciones de pago.",
		},
		{
			"name": "tesoreria",
			"description": "Reportes y liquidaciones de transacciones.",
		},
	],
)


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
	start_time = time.perf_counter()
	request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
	structlog.contextvars.bind_contextvars(request_id=request_id)
	response = None
	try:
		response = await call_next(request)
		return response
	finally:
		duration_ms = (time.perf_counter() - start_time) * 1000
		logger.info(
			"http_request",
			method=request.method,
			path=request.url.path,
			query_string=request.url.query,
			client_ip=request.client.host if request.client else None,
			status_code=getattr(response, "status_code", 500),
			duration_ms=round(duration_ms, 2),
		)
		structlog.contextvars.clear_contextvars()

app.include_router(gateway_router)
app.include_router(tesoreria_router)
