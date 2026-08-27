# EcoEnergy — Fase 1

Creación proyecto para la asignatura de BlackEnd con Django que permite a EcoEnergy consultar zonas de consumo energético y revisar el detalle de los dispositivos instalados en cada una, identificando el consumo total y si la zona está en estado normal o de alerta.

Esta primera versión (Fase 1) no utiliza base de datos ni Models: toda la información se lee desde archivos JSON y Django se encarga de cargarla, relacionarla y presentarla mediante Templates con Bootstrap.

## Requisitos

- Python 3.14+
- pip

## Instalación

1. Clonar el repositorio:
git clone <https://github.com/maricelVM/EcoEnergy>
cd EcoEnergy

2. Crear y activar entorno virtual:
python -m venv .venv
.venv\Scripts\Activate.ps1

3. Instalar dependencias:
pip install -r requirements.txt


## Ejecución
python manage.py runserver


La aplicación queda disponible en `http://localhost:8000/`.

## Rutas funcionales

| Ruta | Qué hace |
|---|---|
| `http://localhost:8000/` | Página de inicio con presentación general del sistema. |
| `http://localhost:8000/zonas/` | Listado de todas las zonas registradas en `zonas.json`, con nombre, límite de consumo y cantidad de dispositivos que tiene cada una. |
| `http://localhost:8000/zonas/<id>/` | Detalle de una zona específica: lista sus dispositivos con categoría y consumo, además del consumo total calculado y el estado (NORMAL o ALERTA). |
| `http://localhost:8000/zonas/999/` | Ejemplo de identificador inexistente: responde con una página 404 personalizada. |

## Estructura de datos (fuente JSON)

Los datos viven en `data/`, como tres archivos independientes relacionados entre sí por identificadores:

- **`data/zonas.json`** — cada zona tiene `id`, `nombre` y `limite_kwh` (el tope de consumo permitido).
- **`data/categorias.json`** — cada categoría tiene `id`, `nombre` y `descripcion` (ej. Solar, Iluminación, Climatizador).
- **`data/dispositivos.json`** — cada dispositivo tiene `id`, `nombre`, `consumo_kwh`, y dos claves de conexión: `zona_id` (a qué zona pertenece) y `categoria_id` (a qué categoría pertenece).

La relación entre estos archivos no se guarda en el JSON directamente (no hay listas anidadas): se resuelve en Python, comparando estos identificadores en tiempo de ejecución.

## Qué hace cada parte del código

- **`dispositivos/services.py`** — contiene toda la lógica de datos, separada de las vistas:
  - `_cargar_json()`: lee y valida cualquiera de los 3 archivos JSON (evita repetir el mismo código de lectura tres veces).
  - `cargar_zonas()`, `cargar_categorias()`, `cargar_dispositivos()`: devuelven la lista cruda de cada archivo.
  - `obtener_zonas_con_resumen()`: arma el listado de zonas, contando cuántos dispositivos tiene cada una — esto es lo que usa la vista de listado.
  - `obtener_detalle_zona(zona_id)`: busca una zona por su id, une sus dispositivos con el nombre de su categoría, suma el consumo total y calcula si el estado es NORMAL o ALERTA (comparando contra `limite_kwh`). Si la zona no existe, devuelve `None`.

- **`dispositivos/views.py`**:
  - `lista_zonas`: llama a `obtener_zonas_con_resumen()` y entrega el contexto al template de listado.
  - `detalle_zona`: llama a `obtener_detalle_zona()`; si el resultado es `None` (zona inexistente), lanza `Http404` para responder con la página de error controlada en vez de romper la aplicación.

- **`dispositivos/urls.py`** — define las rutas `zonas/` y `zonas/<int:zona_id>/`, conectando cada una con su vista correspondiente.

- **`templates/dispositivos/lista_zonas.html`** — muestra cada zona como una tarjeta Bootstrap con su nombre, límite, cantidad de dispositivos y un botón "Ver detalle". Si no hubiera zonas, muestra un mensaje en vez de una grilla vacía.

- **`templates/dispositivos/detalle_zona.html`** — muestra 4 tarjetas de resumen (límite, consumo total, cantidad de dispositivos, estado) y una tabla con el detalle de cada dispositivo (nombre, categoría, consumo). Si la zona no tiene dispositivos, muestra un mensaje en vez de una tabla vacía. El estado usa texto ("NORMAL"/"ALERTA") además de color, para que no dependa solo del color.

- **`templates/404.html`** — página de error personalizada que mantiene la misma navegación y estilo del resto del sitio, con un botón para volver al listado de zonas, en vez de mostrar el error técnico por defecto de Django.

## Dependencia externa: django-bootstrap5

- **Necesidad**: dar estructura visual (tarjetas, tabla responsive, badges de estado) sin escribir CSS desde cero.
- **Uso**: se carga en `templates/base.html` mediante `{% load django_bootstrap5 %}`, `{% bootstrap_css %}` y `{% bootstrap_javascript %}`, y sus clases (`card`, `table-responsive`, `badge`, etc.) se usan en los templates de zonas.
- **Comprobación**: al visitar cualquier ruta, la página muestra tipografía, espaciado y componentes con estilo Bootstrap en vez de HTML sin formato.
- **Registro**: está en `requirements.txt` y en `INSTALLED_APPS` de `config/settings.py`.

## Pruebas realizadas

Escenario : Resultado observado 

Listado de zonas : Muestra las 3 zonas con nombre, límite y cantidad de dispositivos correcta. 
Detalle de zona con consumo bajo el límite : Estado se muestra como NORMAL (badge verde). 
Detalle de zona con consumo sobre el límite : Estado se muestra como ALERTA (badge rojo)ej. zona "Oficina". 
Zona sin dispositivos : Se muestra el mensaje "Esta zona no tiene dispositivos" en vez de una tabla vacía. 
Identificador de zona inexistente (`/zonas/999/`) : Responde con página 404 personalizada, sin exponer detalles técnicos. 
`python manage.py check` : Ejecuta sin errores. 