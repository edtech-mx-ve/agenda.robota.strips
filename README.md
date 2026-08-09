# Agenda Robota STRIPS

**Versión estable:** 1.0.0  
**Estado:** estable, validada y desplegada públicamente en Render  
**Aplicación principal:** `agenda_robota_strips.main:app`  
**Interfaz local:** `http://127.0.0.1:8000/`  
**API interactiva:** `http://127.0.0.1:8000/docs`  
**Aplicación pública:** https://agenda-robota-strips.onrender.com/  
**Repositorio:** https://github.com/edtech-mx-ve/agenda.robota.strips  
**Secretos requeridos:** ninguno

## Implementación de un sistema STRIPS básico para planificar y simular el movimiento de un robot usando Python

**INSTITUTO INTERNACIONAL DE AGUASCALIENTES**  
**Maestría en Inteligencia Artificial para la Transformación Digital**  
**Asignatura:** Razonamiento Inteligente  

| Campo | Información |
|---|---|
| **Alumno** | Antonio Nicolás Toro González |
| **Tutora** | Dra. Claudia Andrea Vidales Basurto |

---

## Descripción

Agenda Robota STRIPS es una aplicación web académica desarrollada en Python para
modelar, planificar y simular el desplazamiento de un robot mediante el formalismo
STRIPS.

El robot opera en una cuadrícula 4×4 de 16 celdas. El usuario selecciona una
posición inicial y una meta. El sistema construye el problema simbólico, verifica
las acciones aplicables y utiliza búsqueda en anchura (BFS) para obtener una
secuencia mínima de movimientos cuando todos los pasos tienen costo unitario.

Cada acción mantiene trazabilidad explícita de:

1. precondiciones `PRE`;
2. efectos positivos `ADD`;
3. efectos negativos `DEL`;
4. estado antes de la acción;
5. estado después de la acción.

Agenda Robota STRIPS no utiliza aprendizaje automático, modelos generativos ni
servicios externos. La planificación es determinista y se apoya en reglas STRIPS
definidas explícitamente.

## Propósito

La aplicación permite:

- representar un estado inicial;
- definir una meta;
- modelar movimientos mediante acciones STRIPS;
- verificar precondiciones;
- aplicar efectos `ADD` y `DEL`;
- buscar automáticamente un plan;
- visualizar la ruta encontrada;
- simular cada acción;
- explicar la transición de estados;
- demostrar los conceptos de planificación automática de la unidad académica.

## Funciones principales

- Escenario 4×4 con 16 celdas.
- 24 conexiones no dirigidas.
- 48 acciones de movimiento dirigidas.
- Selección de inicio y meta.
- Planificación automática con BFS.
- Prevención de ciclos mediante estados visitados.
- Límite defensivo de estados expandidos.
- Estados inmutables con `frozenset`.
- Simulación visual del robot.
- Controles **Reproducir**, **Pausar**, **Avanzar** y **Reiniciar**.
- Posición estable de la página durante la simulación.
- Resaltado de la ruta.
- Contador de pasos.
- Visualización de `PRE`, `ADD` y `DEL`.
- Estado antes y después de cada acción.
- API REST con FastAPI.
- Swagger/OpenAPI.
- Interfaz responsive.
- Encabezados HTTP de seguridad.
- Pruebas automatizadas.
- Validación previa al despliegue.
- Configuración mediante variables de entorno.
- Contenedor Docker.
- Integración continua con GitHub Actions.

## Alcance del planificador

### Estado

Un estado se representa como un conjunto inmutable de hechos.

Ejemplo:

```text
en(robot,A1)
conectado(A1,A2)
conectado(A2,A1)
...
```

### Objetivo

Ejemplo:

```text
en(robot,D4)
```

### Acción

Ejemplo:

```text
mover(A1,A2)

PRE:
  en(robot,A1)
  conectado(A1,A2)

ADD:
  en(robot,A2)

DEL:
  en(robot,A1)
```

### Regla de transición

```text
S' = (S - DEL) ∪ ADD
```

## Escenario 4×4

```text
A1 -- A2 -- A3 -- A4
|     |     |     |
B1 -- B2 -- B3 -- B4
|     |     |     |
C1 -- C2 -- C3 -- C4
|     |     |     |
D1 -- D2 -- D3 -- D4
```

El robot se mueve exclusivamente entre celdas ortogonalmente adyacentes.

## Arquitectura

```text
Usuario
  ↓
Interfaz HTML/CSS/JavaScript
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
  ↓
Plan + traza de estados
  ↓
Simulación visual
```

## Pipeline de planificación

```text
Inicio/meta
→ validación
→ construcción del estado inicial
→ construcción del objetivo
→ generación de acciones
→ evaluación de precondiciones
→ BFS
→ control de estados visitados
→ detección de meta
→ reconstrucción del plan
→ simulación
→ PRE / ADD / DEL
→ estado antes/después
→ reporte visual
```

## Búsqueda BFS

La búsqueda en anchura se utiliza porque el escenario asigna el mismo costo a
cada movimiento.

Para `A1 → D4`, la versión estable encuentra seis movimientos:

```text
A1 → A2 → A3 → A4 → B4 → C4 → D4
```

Resultado esperado:

```text
Meta alcanzada: True
Movimientos: 6
Estados expandidos: 14
```

Puede existir más de una ruta mínima. El orden determinista de las acciones de
esta implementación define cuál se devuelve primero.

## Arquitectura multiparadigma

### Programación estructurada

Organiza la secuencia del algoritmo, selecciones, iteraciones, manejo de errores,
logging y ejecución.

### Programación orientada a objetos

Se utiliza solamente donde existe responsabilidad de dominio o servicio:

- `Action`;
- `Planner`;
- `PlanningResult`;
- `RobotScenario`;
- `RobotPlanningService`;
- `RobotPlan`;
- `MovementStep`.

### Programación funcional

Las transformaciones centrales reciben y devuelven valores explícitos. Los
estados son inmutables y la aplicación de una acción genera un nuevo estado.

### Robustez y seguridad

El proyecto valida entradas, configuración del servidor, límites de búsqueda y
estructura de despliegue. No almacena secretos ni datos personales.

## Estructura del repositorio

```text
agenda-robota-strips/
├── .github/
│   └── workflows/
│       └── quality.yml
├── docs/
│   ├── ARQUITECTURA.md
│   ├── SPRINT_2.md
│   ├── SPRINT_3.md
│   ├── SPRINT_4.md
│   └── VALIDACION_FINAL.md
├── src/
│   └── agenda_robota_strips/
│       ├── web/
│       │   ├── index.html
│       │   └── static/
│       │       ├── agenda-robota-logo.png
│       │       ├── app.js
│       │       └── styles.css
│       ├── __init__.py
│       ├── api.py
│       ├── demo.py
│       ├── domain.py
│       ├── main.py
│       ├── planner.py
│       ├── scenario.py
│       ├── schemas.py
│       ├── security.py
│       └── service.py
├── tests/
├── tools/
│   └── deployment_check.py
├── .dockerignore
├── .gitignore
├── DEPLOYMENT.md
├── Dockerfile
├── pyproject.toml
├── requirements.txt
├── SECURITY.md
└── README.md
```

## Interfaz web

La interfaz incluye:

- logo oficial de Agenda Robota STRIPS;
- título y presentación;
- selección de celda inicial;
- selección de celda objetivo;
- mapa responsive 4×4;
- robot visible;
- ruta planificada;
- métricas del plan;
- controles de simulación;
- panel de trazabilidad;
- explicación de `PRE`, `ADD` y `DEL`;
- estado antes y después;
- regla de transición STRIPS;
- sección de ayuda breve y metódica sobre planificación automática y uso de la app.

Los controles de simulación mantienen estable la posición visual de la página.

## API

### Salud

```text
GET /api/health
```

### Escenario

```text
GET /api/scenario
```

### Planificación

```text
POST /api/plan
```

Ejemplo:

```json
{
  "start": "A1",
  "goal": "D4"
}
```

## Instalación local

### Crear el entorno

```powershell
py -3.12 -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -e ".[dev]"
```

No es necesario recrear `.venv` después de cada cambio. El mismo entorno puede
actualizarse con:

```powershell
pip install -e ".[dev]"
```

### Validar el despliegue

```powershell
python tools\deployment_check.py
```

Resultado esperado:

```text
Validación de despliegue: OK
Entrada ASGI: agenda_robota_strips.main:app
Escenario: 4x4, 16 celdas
Secretos requeridos: ninguno
```

### Ejecutar pruebas

```powershell
pytest -q
```

El resultado exacto debe terminar con todas las pruebas en estado `passed`.

### Iniciar la interfaz web

```powershell
agenda-robota-strips-web
```

Abrir:

```text
http://127.0.0.1:8000/
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Iniciar la versión de consola

```powershell
agenda-robota-strips-demo
```

## Flujo de uso

1. Abrir la aplicación.
2. Elegir una celda inicial.
3. Elegir una celda objetivo.
4. Pulsar **Generar plan STRIPS**.
5. Revisar la ruta y métricas.
6. Pulsar **Avanzar** para inspeccionar una acción.
7. Verificar `PRE`, `ADD` y `DEL`.
8. Revisar estado antes y después.
9. Utilizar **Reproducir** o **Pausar**.
10. Utilizar **Reiniciar** cuando se requiera repetir la simulación.

## Pruebas

La suite verifica, entre otros casos:

- normalización de hechos;
- precondiciones;
- efectos `ADD` y `DEL`;
- rechazo de efectos incompatibles;
- aplicación de acciones;
- BFS;
- ruta mínima;
- inicio igual a meta;
- validación de zonas;
- estructura 4×4;
- conexiones y acciones;
- servicio de planificación;
- traza STRIPS;
- API;
- seguridad HTTP;
- interfaz web;
- logo;
- controles de simulación;
- estabilidad del viewport;
- configuración del servidor;
- artefactos de despliegue.

## Seguridad y privacidad

Agenda Robota STRIPS no requiere autenticación ni secretos.

No deben publicarse:

```text
.env
.env.*
*.pem
*.key
secrets.toml
tokens
credenciales
cookies
logs con datos personales
```

La aplicación no solicita información personal y solamente procesa las celdas de
inicio y objetivo.

Consulte `SECURITY.md`.

## Archivos excluidos del repositorio

```text
.venv/
venv/
env/
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.env
.env.*
*.pem
*.key
logs/
*.log
.vscode/
.idea/
*.zip
```

Verificación recomendada:

```powershell
python tools\deployment_check.py
git status --ignored
git diff --cached --name-only
```

## GitHub Actions

El flujo:

```text
.github/workflows/quality.yml
```

ejecuta:

- instalación de Python 3.12;
- instalación del proyecto;
- compilación de módulos;
- validación de despliegue;
- pruebas con `pytest`.

No debe publicarse una versión si el flujo de calidad falla.

## Docker

Construir:

```powershell
docker build -t agenda-robota-strips:1.0.0 .
```

Ejecutar:

```powershell
docker run --rm -p 8000:8000 agenda-robota-strips:1.0.0
```

Abrir:

```text
http://127.0.0.1:8000/
```

Consulte `DEPLOYMENT.md`.


## Despliegue público

Agenda Robota STRIPS se encuentra desplegada en **Render** como Web Service.

Aplicación pública:

```text
https://agenda-robota-strips.onrender.com/
```

Repositorio oficial:

```text
https://github.com/edtech-mx-ve/agenda.robota.strips
```

Configuración utilizada en Render:

```text
Runtime: Python 3
Branch: main
Build Command: pip install .
Start Command: uvicorn agenda_robota_strips.main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```

La aplicación utiliza HTTPS proporcionado por Render y no requiere secretos ni
variables sensibles para su operación actual.

## Actualización

Repositorio oficial:

```text
https://github.com/edtech-mx-ve/agenda.robota.strips
```

Primera publicación del proyecto:

```powershell
git init
git branch -M main
git remote add origin https://github.com/edtech-mx-ve/agenda.robota.strips.git
git add .
git commit -m "release: Agenda Robota STRIPS 1.0.0"
git push -u origin main
```

Actualizaciones posteriores:

```powershell
git add .
git commit -m "fix: ajustar planificador o interfaz"
git push origin main
```

## Reversión

```powershell
git log --oneline
git revert IDENTIFICADOR_DEL_COMMIT
git push origin main
```

La reversión conserva la trazabilidad del historial.

## Limitaciones

- El escenario es fijo y conocido.
- Solo existe un robot.
- Los movimientos son deterministas.
- No existen obstáculos dinámicos.
- No existen sensores ni incertidumbre.
- No se modelan batería, recursos o duración.
- No se controlan motores físicos.
- No se utiliza PDDL externo.
- BFS no escala eficientemente a dominios de gran tamaño.
- El plan gratuito de Render puede suspender temporalmente la instancia cuando no recibe tráfico.

## Relación con la unidad académica

### Planificación automática

El sistema parte de un estado inicial, un conjunto de acciones y un objetivo.

### Representación STRIPS

Las acciones contienen precondiciones y efectos positivos/negativos.

### Estado inicial

```text
en(robot,A1)
```

junto con los hechos de conectividad del escenario.

### Acción de movimiento

```text
mover(A1,A2)
```

### Objetivo

```text
en(robot,D4)
```

### Implementación en Python

El proyecto utiliza:

- funciones;
- clases con responsabilidad definida;
- `dataclass`;
- `frozenset`;
- `tuple`;
- `set`;
- `deque`;
- excepciones específicas;
- logging;
- validación;
- anotaciones de tipo;
- modularidad;
- pruebas;
- API;
- interfaz web.

## Uso académico

Proyecto desarrollado para la asignatura **Razonamiento Inteligente** de la
**Maestría en Inteligencia Artificial para la Transformación Digital**.

La finalidad es demostrar de forma ejecutable y explicable cómo un sistema STRIPS
puede representar y resolver un problema básico de movimiento de un robot.
