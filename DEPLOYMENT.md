# Despliegue — Agenda Robota STRIPS

La versión 1.0.0 está preparada para ejecución local, servidor ASGI y contenedor
Docker. No se declara una URL pública hasta que el repositorio y el proveedor
sean configurados realmente.

## Entrada ASGI

```text
agenda_robota_strips.main:app
```

## Variables de entorno

| Variable | Obligatoria | Valor por defecto |
|---|---:|---|
| `AGENDA_ROBOTA_HOST` | No | `127.0.0.1` |
| `PORT` | No | `8000` |
| `AGENDA_ROBOTA_PORT` | No | `8000` si `PORT` no existe |

No se requieren secretos.

## Ejecución ASGI

```powershell
$env:AGENDA_ROBOTA_HOST = "0.0.0.0"
$env:PORT = "8000"
agenda-robota-strips-web
```

## Docker

Construcción:

```powershell
docker build -t agenda-robota-strips:1.0.0 .
```

Ejecución:

```powershell
docker run --rm -p 8000:8000 agenda-robota-strips:1.0.0
```

Validación:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/api/health
http://127.0.0.1:8000/docs
```

## Plataforma administrada

En un servicio capaz de ejecutar aplicaciones Python/ASGI se deben configurar:

```text
Build:
pip install .

Start:
agenda-robota-strips-web
```

Si la plataforma suministra `PORT`, la aplicación lo usa automáticamente.
Para exposición pública debe configurarse `AGENDA_ROBOTA_HOST=0.0.0.0`.

## Validación previa

```powershell
python tools\deployment_check.py
pytest -q
```

No publique una versión si cualquiera de los comandos falla.


## Repositorio oficial

```text
https://github.com/edtech-mx-ve/agenda.robota.strips
```

### Primera publicación

```powershell
git init
git branch -M main
git remote add origin https://github.com/edtech-mx-ve/agenda.robota.strips.git
git add .
git commit -m "release: Agenda Robota STRIPS 1.0.0"
git push -u origin main
```

Antes del `push`:

```powershell
python tools\deployment_check.py
pytest -q
git status
```

No deben publicarse archivos listados en `.gitignore`.


## Despliegue público actual

Proveedor: **Render**

```text
https://agenda-robota-strips.onrender.com/
```

Configuración:

```text
Runtime: Python 3
Branch: main
Build Command: pip install .
Start Command: uvicorn agenda_robota_strips.main:app --host 0.0.0.0 --port $PORT
Instance Type: Free
```
