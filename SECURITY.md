# Seguridad y privacidad — Agenda Robota STRIPS

## Alcance

Agenda Robota STRIPS es una aplicación académica de planificación simbólica.
No requiere cuentas, autenticación, base de datos, cookies de sesión, claves de
API ni servicios externos para ejecutar el planificador.

## Datos procesados

La API recibe únicamente:

```json
{
  "start": "A1",
  "goal": "D4"
}
```

Las zonas son validadas contra el escenario permitido de 16 celdas.

## Controles implementados

- validación de entrada mediante Pydantic;
- rechazo de campos HTTP no definidos;
- límite de estados expandidos en BFS;
- estado de dominio inmutable mediante `frozenset`;
- encabezados HTTP defensivos;
- Content Security Policy de mismo origen;
- bloqueo de cámara, micrófono y geolocalización;
- frontend sin dependencias JavaScript de terceros;
- ausencia de ejecución dinámica de código recibido;
- logging sin credenciales ni datos personales.

## No publicar

No deben incorporarse al repositorio:

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

## Secretos

La versión 1.0.0 no requiere secretos.

Si en una evolución futura se agregan APIs externas, las credenciales deberán
leerse desde variables de entorno o el gestor de secretos del proveedor y nunca
quedar codificadas en Python, JavaScript, Git o archivos públicos.

## Reporte de vulnerabilidades

Para un repositorio público, los hallazgos de seguridad deben reportarse por un
canal privado del propietario del repositorio antes de abrir un issue público.
