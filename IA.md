EcoEnergy Fase 1

## Herramienta utilizada

Se utilizó Claude a través de la interfaz de chat, como apoyo conceptual y de revisión de código durante todo el desarrollo de la Fase 1.

## Uso general

Se usó IA para: proponer estructura de código para `services.py`, proponer estilos Bootstrap para los templates y depurar errores concretos que aparecían al ejecutar el proyecto (tracebacks de `runserver`, `NoReverseMatch`, `TemplateDoesNotExist`, `LookupError`, `AttributeError`).

## Prompts principales y respuesta utilizada

1. **Prompt**: "Ayúdame a construir la función que carga y relaciona zonas, categorías y dispositivos desde JSON."
   **Respuesta utilizada**: estructura de `services.py` con `_cargar_json()`, `obtener_zonas_con_resumen()` y `obtener_detalle_zona()`.
   **Cambios propios**: se ajustaron los nombres de archivo JSON y los `id` de zonas/categorías según los datos reales que definí (`zonas.json` con id 10, 11, 12; `categorias.json` con id 21, 22, 23), lo que obligó a corregir manualmente los `zona_id` y `categoria_id` de `dispositivos.json` para que coincidieran.
   **Verificación**: se probó en el navegador que `/zonas/` mostrara la cantidad correcta de dispositivos por zona, y se corrigieron los `id` hasta que coincidieron.

2. **Prompt**: "Diseña el contenido de catalogo.html [luego adaptado a lista_zonas.html y detalle_zona.html] usando Bootstrap 5 y heredando de base.html, con las variables reales del contexto."
   **Respuesta utilizada**: estructura HTML con tarjetas (`card`), tabla `table-responsive`, y badge de estado NORMAL/ALERTA.
   **Cambios propios**: se integraron los templates propuestos respetando el `{% block title %}` y la navegación (`<nav>`) que ya existían en mi `base.html`, sin sobrescribir esas partes.
   **Verificación**: se probó visualmente en el navegador (capturas en `/zonas/` y `/zonas/10/`), confirmando que el badge cambia de verde a rojo según el consumo real de cada zona.

3. **Prompt**: pegar tracebacks de errores reales al ejecutar `python manage.py runserver` (ej. `LookupError: No installed app with label 'admin'`, `NoReverseMatch: Reverse for 'catalogo' not found`, `TemplateDoesNotExist`).
   **Respuesta utilizada**: diagnóstico de la causa exacta de cada error (ej. `INSTALLED_APPS` duplicado en `settings.py`, un `{% url %}` apuntando a una vista eliminada, un archivo con nombre distinto al esperado).
   **Cambios propios**: se corrigió cada archivo manualmente siguiendo el diagnóstico, y se verificó en cada caso volviendo a correr `runserver` hasta que el error desapareciera.

## Partes NO generadas por IA

- Los datos concretos de `zonas.json`, `categorias.json` y `dispositivos.json` (nombres, límites, consumos) fueron definidos por mí.

- Views, Services y base html se utilizaron de base las creadas en laboratorios en clases y fueron adaptadas a los nuevos requerimientos.

- La decisión de cómo categorizar los medidores/sensores (bajo "Solar") fue una decisión propia.

- Todos los comandos de Git (`add`, `commit`, `push`) y la organización de los 4 commits progresivos fueron creados y ejecutados por mi.

## Verificación final

Se ejecutó `python manage.py check` sin errores, y se probaron manualmente en el navegador todos los criterios de aceptación (CA-01 a CA-13) antes de la entrega.