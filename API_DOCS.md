# Pasarela Pago Service API

Servicio orquestador de pagos y tesoreria. Expone endpoints para procesar cobros y liquidaciones.

## Base URL

http://localhost:8000

## Configuracion

Variables en .env:
- POCKETBASE_URL
- VISA_SERVICE_URL
- MASTERCARD_SERVICE_URL

## Modelos

### PagoRequest

```json
{
  "id_idempotencia": "uuid-o-cadena",
  "empresa_id": "empresa_123",
  "numero_tarjeta": "4111111111111111",
  "cvc": "123",
  "fecha_expiracion": "12/28",
  "monto": 120.50
}
```

### PagoResponse

```json
{
  "status": "Aprobado",
  "transaccion_id": "pb_transaccion_id",
  "mensaje": "Pago aprobado"
}
```

### LiquidacionBatchRequest

```json
{
  "transaccion_id": ["id1", "id2", "id3"]
}
```

### ReporteResponse

```json
{
  "empresa_id": "empresa_123",
  "total_deuda": 350.00,
  "cantidad_transacciones": 3
}
```

## Endpoints

### POST /procesar-pago

Procesa un cobro. Aplica idempotencia por `id_idempotencia`.

Request: PagoRequest

Response: PagoResponse

Ejemplo:

```bash
curl -X POST http://localhost:8000/procesar-pago \
  -H "Content-Type: application/json" \
  -d '{
    "id_idempotencia": "3b0d2b61-2f41-4f1a-8f66-4a3d2c1b8d7c",
    "empresa_id": "empresa_123",
    "numero_tarjeta": "4111111111111111",
    "cvc": "123",
    "fecha_expiracion": "12/28",
    "monto": 120.50
  }'
```

### GET /reportes/{empresa_id}

Genera reporte de deuda para una empresa. Por ahora se asume que el `empresa_id` proviene del path.

Response: ReporteResponse

Ejemplo:

```bash
curl http://localhost:8000/reportes/empresa_123
```

### POST /liquidar/batch

Liquida una lista de transacciones y cambia su estado a "Liquidado".

Request: LiquidacionBatchRequest

Response:

```json
{
  "status": "ok",
  "mensaje": "Liquidacion procesada"
}
```

Ejemplo:

```bash
curl -X POST http://localhost:8000/liquidar/batch \
  -H "Content-Type: application/json" \
  -d '{"transaccion_id": ["id1", "id2"]}'
```

## Estados de transaccion

- Procesando
- Aprobado
- Rechazado
- No Liquidado
- Liquidado

## Notas

- La franquicia se determina por el primer digito: 4 = Visa, 5 = Mastercard.
- Los endpoints externos se llaman via httpx.AsyncClient desde el servicio.
- Los errores de validacion o de negocio devuelven 400 cuando aplica.
