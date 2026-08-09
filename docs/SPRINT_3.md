# Sprint 3 — Agenda Robota STRIPS

## Objetivo

Transformar el planificador web 4×4 en un simulador STRIPS interactivo y
didáctico, manteniendo el motor de planificación desacoplado de la interfaz.

## Funcionalidad implementada

- Reproducción automática del plan.
- Pausa.
- Avance manual paso a paso.
- Reinicio.
- Marcador visual del robot en la celda actual.
- Ruta completa resaltada.
- Contador `Paso X de N`.
- Acción actual.
- Precondiciones PRE.
- Efectos ADD.
- Efectos DEL.
- Estado antes y estado después.
- Tratamiento correcto de `inicio == meta`.
- Respeto de `prefers-reduced-motion`.

## Flujo

```text
Usuario elige inicio/meta
        ↓
POST /api/plan
        ↓
STRIPS + BFS
        ↓
Plan + traza PRE/ADD/DEL
        ↓
Interfaz carga robot en inicio
        ↓
Reproducir / Avanzar
        ↓
Aplicar visualmente cada transición
        ↓
Meta alcanzada
```

## Contrato de cada paso

Ejemplo `mover(A1,A2)`:

```json
{
  "index": 1,
  "action": "mover(A1,A2)",
  "origin": "A1",
  "destination": "A2",
  "preconditions": [
    "conectado(A1,A2)",
    "en(robot,A1)"
  ],
  "add_effects": [
    "en(robot,A2)"
  ],
  "del_effects": [
    "en(robot,A1)"
  ],
  "state_before": [
    "en(robot,A1)"
  ],
  "state_after": [
    "en(robot,A2)"
  ]
}
```

## Criterios de aceptación

- El plan A1 → D4 conserva 6 movimientos mínimos.
- Cada paso contiene PRE, ADD y DEL.
- La interfaz muestra estados antes/después.
- Reproducir mueve el robot hasta la meta.
- Pausar detiene la reproducción.
- Avanzar ejecuta un único paso.
- Reiniciar devuelve el robot al inicio.
- Inicio igual a meta no intenta reproducir movimientos.
- Todas las pruebas automatizadas pasan.

## Limitaciones

- Entorno estático.
- Un único robot.
- Sin obstáculos dinámicos.
- Sin recursos, batería ni duración temporal.
- Sin control físico de actuadores.


## Estabilidad de viewport

Se eliminó el uso de `scrollIntoView()` en el resaltado del paso actual y se
preserva explícitamente la posición de desplazamiento al usar los controles de
simulación. Esto evita que la interfaz salte al inicio o cambie de posición
durante **Reproducir, Pausar, Avanzar y Reiniciar**.
