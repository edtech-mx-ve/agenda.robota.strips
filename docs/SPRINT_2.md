# Sprint 2 — Agenda Robota STRIPS · escenario 4x4

## Cambio principal

El escenario original A-B-C-D se amplía a una cuadrícula de 16 celdas:

```text
A1 -- A2 -- A3 -- A4
|     |     |     |
B1 -- B2 -- B3 -- B4
|     |     |     |
C1 -- C2 -- C3 -- C4
|     |     |     |
D1 -- D2 -- D3 -- D4
```

El robot puede moverse únicamente entre celdas ortogonalmente adyacentes:
arriba, abajo, izquierda o derecha.

## Modelo STRIPS

Ejemplo:

```text
Acción:
mover(B2,B3)

PRE:
en(robot,B2)
conectado(B2,B3)

ADD:
en(robot,B3)

DEL:
en(robot,B2)
```

La transición sigue siendo:

`S' = (S - DEL) ∪ ADD`

## Búsqueda

BFS sigue siendo apropiado porque todos los movimientos tienen costo unitario.
En una cuadrícula abierta 4x4, la distancia mínima entre A1 y D4 es de 6 acciones.

## Magnitud del dominio

- 16 estados de posición posibles para el robot.
- 24 conexiones no dirigidas.
- 48 acciones STRIPS dirigidas.
- Cada celda interior tiene hasta 4 acciones de movimiento aplicables.

## Criterios de aceptación

- `/api/scenario` entrega 16 celdas.
- La interfaz representa una cuadrícula 4x4.
- A1 → D4 produce un plan de 6 movimientos.
- Una celda interior como B2 tiene 4 movimientos potenciales.
- Inicio igual a meta devuelve un plan vacío válido.
- Entradas inválidas son rechazadas.
- Todas las pruebas automatizadas pasan.
