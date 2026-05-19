# Pasarela Pago Service API

Servicio orquestador de pagos y tesoreria. Expone endpoints para procesar cobros y liquidaciones.

## Base URL

http://localhost:8000

## Configuracion

Variables en .env:
- POCKETBASE_URL
- VISA_SERVICE_URL
- MASTERCARD_SERVICE_URL
- NU_SERVICE_URL
- NU_SERVICE_TOKEN

## Modelos

### PagoRequest

```json
{
  "id_idempotencia": "uuid-o-cadena",
  "empresa_id": "empresa_123",
  "franquicia": "Visa",
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

### TransaccionDetalle

```json
{
  "id": "pb_transaccion_id",
  "id_idempotencia": "idem-001",
  "empresa_id": "empresa_123",
  "monto": 100.5,
  "estado": "No Liquidado",
  "fecha": "2026-05-18T12:00:00Z"
}
```

### ReporteResponse

```json
{
  "empresa_id": "empresa_123",
  "total_deuda": 350.00,
  "cantidad_transacciones": 3,
  "transacciones": [
    {
      "id": "pb_transaccion_id",
      "id_idempotencia": "idem-001",
      "empresa_id": "empresa_123",
      "monto": 100.5,
      "estado": "No Liquidado",
      "fecha": "2026-05-18T12:00:00Z"
    }
  ]
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
    "franquicia": "Visa",
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

Liquida todas las transacciones con estado "No Liquidado" en todo el sistema.

Response:

```json
{
  "status": "ok",
  "mensaje": "Liquidacion procesada",
  "cantidad_liquidadas": 2
}
```

Ejemplo:

```bash
curl -X POST http://localhost:8000/liquidar/batch
```

## Estados de transaccion

- Procesando
- Aprobado
- Rechazado
- No Liquidado
- Liquidado

## Notas

- La franquicia se recibe en el request y debe ser Visa, Mastercard o Nu.
- Los endpoints externos se llaman via httpx.AsyncClient desde el servicio.
- Los errores de validacion o de negocio devuelven 400 cuando aplica.
