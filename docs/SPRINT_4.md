# Sprint 4 — Cierre técnico y académico

## Objetivo

Convertir el prototipo aprobado en una versión estable, documentada,
reproducible y preparada para publicación.

## Implementado

- versión estable `1.0.0`;
- README académico completo;
- documentación de arquitectura;
- matriz de validación final;
- `SECURITY.md`;
- `DEPLOYMENT.md`;
- `requirements.txt`;
- `Dockerfile` y `.dockerignore`;
- comprobación previa de despliegue;
- GitHub Actions;
- configuración de host/puerto por entorno;
- logo incluido correctamente en el paquete instalado;
- pruebas de configuración y artefactos finales.

## Criterio de cierre

El proyecto se considera cerrado cuando:

1. `python tools\deployment_check.py` devuelve OK;
2. `pytest -q` pasa completamente;
3. la app inicia;
4. A1 → D4 genera seis movimientos;
5. la simulación llega a D4;
6. PRE / ADD / DEL son visibles;
7. los controles no desplazan la página;
8. no existen secretos requeridos o embebidos.

## Backlog posterior a la entrega

No forma parte de la versión académica 1.0.0:

- obstáculos configurables;
- edición visual de mapas;
- comparación BFS / A*;
- importación/exportación PDDL;
- varios robots;
- costos diferentes por acción;
- despliegue público definitivo.


## Repositorio GitHub asignado

Repositorio oficial del proyecto:

```text
https://github.com/edtech-mx-ve/agenda.robota.strips
```

La versión local 1.0.0 está preparada para ser publicada en la rama `main`.
