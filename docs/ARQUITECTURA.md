# Arquitectura — Agenda Robota STRIPS

## Capas

```text
Usuario
  ↓
HTML semántico + CSS responsivo + JavaScript modular
  ↓
FastAPI
  ↓
RobotPlanningService
  ↓
Planner BFS
  ↓
Dominio STRIPS
  ↓
Estado + Acción(PRE, ADD, DEL)
```

## Responsabilidades

| Capa | Responsabilidad |
|---|---|
| Interfaz | Selección inicio/meta, mapa 4×4, simulación y trazabilidad |
| API | Validación HTTP y serialización |
| Servicio | Orquestación del problema de navegación |
| Planificador | Búsqueda BFS y control de visitados |
| Dominio | Acciones STRIPS, aplicación de efectos y estados inmutables |
| Seguridad | Encabezados HTTP y validación defensiva |

## Paradigmas empleados

### Programación estructurada

Organiza el flujo de planificación, validación, iteración BFS y ejecución.

### Programación orientada a objetos

Representa responsabilidades reales mediante `Action`, `Planner`,
`RobotScenario`, `RobotPlanningService` y objetos de resultado.

### Programación funcional

Las transformaciones centrales devuelven nuevos valores. Los estados STRIPS son
`frozenset`, y la transición no modifica el estado recibido.

### Robustez y seguridad

La aplicación valida zonas, tipos, límites de búsqueda y configuración del
servidor. No procesa secretos ni ejecuta código externo.

## Transición STRIPS

```text
S' = (S - DEL) ∪ ADD
```

Ejemplo:

```text
Acción: mover(A1,A2)

PRE:
  en(robot,A1)
  conectado(A1,A2)

ADD:
  en(robot,A2)

DEL:
  en(robot,A1)
```

## Búsqueda

BFS se utiliza porque todas las acciones del escenario tienen costo unitario.
Se mantiene un conjunto de estados visitados para evitar ciclos.

## Escenario

```text
A1 -- A2 -- A3 -- A4
|     |     |     |
B1 -- B2 -- B3 -- B4
|     |     |     |
C1 -- C2 -- C3 -- C4
|     |     |     |
D1 -- D2 -- D3 -- D4
```

- 16 celdas;
- 24 conexiones no dirigidas;
- 48 acciones de movimiento dirigidas;
- movimientos ortogonales;
- un robot;
- entorno determinista y completamente conocido.
