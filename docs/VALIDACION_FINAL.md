# Validación final — Agenda Robota STRIPS 1.0.0

## Criterios académicos

| Criterio | Evidencia |
|---|---|
| Estado inicial | `en(robot,zona)` + conexiones |
| Objetivo | `en(robot,meta)` |
| Acciones | `mover(origen,destino)` |
| PRE | posición actual + conexión |
| ADD | nueva posición |
| DEL | posición anterior |
| Planificación | BFS |
| Simulación | paso a paso en interfaz |
| Trazabilidad | PRE / ADD / DEL + estado antes/después |

## Prueba principal

```text
Inicio: A1
Meta: D4
```

Ruta mínima determinista de la versión:

```text
A1 → A2 → A3 → A4 → B4 → C4 → D4
```

Resultado esperado:

```text
Meta alcanzada: True
Movimientos: 6
Estados expandidos: 14
```

## Casos cubiertos

- transición ADD/DEL correcta;
- rechazo de acción sin precondiciones;
- rechazo de ADD y DEL superpuestos;
- búsqueda mínima A1 → D4;
- inicio igual a meta;
- zona inválida;
- cuadrícula de 16 celdas;
- 24 aristas / 48 acciones;
- cuatro movimientos potenciales en celda interior;
- API health;
- API scenario;
- API plan;
- rechazo de campos extra;
- encabezados de seguridad;
- logo incluido;
- trazabilidad PRE / ADD / DEL;
- estado antes/después;
- controles de simulación;
- estabilidad del viewport;
- configuración de puerto;
- estructura de despliegue.

## Limitaciones

- un robot;
- escenario fijo 4×4;
- sin obstáculos dinámicos;
- sin incertidumbre;
- sin sensores;
- sin batería o recursos;
- sin tiempo continuo;
- sin control de hardware;
- sin PDDL externo;
- BFS no es adecuado para dominios de gran escala sin heurísticas.
