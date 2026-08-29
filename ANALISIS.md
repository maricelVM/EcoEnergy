# ANALISIS.md — EcoEnergy Fase 1

## 1. Relaciones y multiplicidades

El modelo de datos sigue el diagrama UML entregado en el enunciado (Figura 1), con tres entidades relacionadas mediante identificadores en archivos JSON (sin base de datos ni Models):
Zona (1) ---- contiene ---- (0..) Dispositivo (0..) ---- clasifica ---- (1) Categoria


**Zona → Dispositivo**: una zona puede tener **cero o muchos** dispositivos (`0..*`), y cada dispositivo pertenece exactamente a **una** zona (`1`). Ejemplo: la zona "Oficina" (id 10) tiene 3 dispositivos asociados.

**Dispositivo → Categoria**: cada dispositivo pertenece exactamente a **una** categoría (`1`), y una categoría puede clasificar **cero o muchos** dispositivos (`0..*`). Ejemplo: la categoría "Solar" (id 21) clasifica a varios medidores de distintas zonas.

Esta relación no está anidada dentro del JSON (no hay listas de dispositivos dentro de cada zona); se resuelve en Python, comparando identificadores en tiempo de ejecución dentro de `dispositivos/services.py`.

## 2. Claves de conexión

| Archivo | Clave primaria | Claves foráneas (conectan con) 
 `zonas.json` | `id` | — |
 `categorias.json` | `id` | — |
 `dispositivos.json` | `id` | `zona_id` → `zonas.json[].id`; `categoria_id` → `categorias.json[].id` 

Ejemplo real de una relación completa:

json
// dispositivos.json
{ "id": 4, "nombre": "Aire acondicionado oficina", "consumo_kwh": 60.0, "zona_id": 10, "categoria_id": 23 }


Esto se lee como: el dispositivo "Aire acondicionado oficina" pertenece a la zona con `id: 10` (Oficina) y a la categoría con `id: 23` (Climatizador).

## 3. Cómo se resuelve la relación en código

En `dispositivos/services.py` la función `obtener_detalle_zona(zona_id)`:

1. Busca la zona cuyo `id` coincide con `zona_id` (si no existe, devuelve `None`).
2. Recorre todos los dispositivos y filtra los que tienen `zona_id` igual al de la zona buscada.
3. Para cada dispositivo filtrado, busca el nombre de su categoría en un diccionario `categorias_por_id` (construido antes, para no recorrer la lista de categorías repetidamente).
4. Suma el `consumo_kwh` de todos los dispositivos filtrados → `consumo_total`.
5. Compara `consumo_total` contra `limite_kwh` de la zona → determina `estado` (`"ALERTA"` si lo supera, `"NORMAL"` si no).

## 4. Matriz de criterios de aceptación

Criterio | Archivo / Componente | Prueba realizada |

CA-01 : `services.py` (`obtener_zonas_con_resumen`), `lista_zonas.html` | Se visitó `/zonas/` y se verificó que aparecen las 3 zonas de `zonas.json`. 

CA-02 : `services.py`, `lista_zonas.html` | Cada tarjeta muestra nombre, límite, cantidad de dispositivos y botón "Ver detalle" funcional. 

CA-03 : `services.py` (`obtener_detalle_zona`), `detalle_zona.html` | Se visitó `/zonas/10/` y se verificó que muestra dispositivos, categoría, consumo, métricas (tarjetas) y estado. 

CA-04 : `services.py` | Las cantidades y sumas se calculan con `len()` y `sum()` en Python; no hay números escritos manualmente en los templates. 

CA-05 : `services.py` (comparación `consumo_total > limite_kwh`) | Zona "Oficina" (consumo 71.2 > límite 70.0) mostró badge ALERTA; zonas "Bodega" y "Planta" mostraron NORMAL. 

CA-06 : `services.py`, `dispositivos.json` | Se pueden agregar dispositivos nuevos al JSON sin modificar código; el `for` en `services.py` los procesa automáticamente. 

CA-07 : `services.py`, `detalle_zona.html` (`{% if dispositivos %}`) | Se probó una zona sin dispositivos: mostró el mensaje "Esta zona no tiene dispositivos" en vez de una tabla vacía o error. 

CA-08 : `views.py` (`raise Http404`), `templates/404.html` | Se visitó `/zonas/999/` (id inexistente): respondió con página 404 personalizada, sin exponer detalles técnicos (probado con `DEBUG = False`). 

CA-09 : `lista_zonas.html`, `detalle_zona.html` (uso de `{% for %}`) | La estructura no depende de cantidad fija de elementos; se mantiene estable al variar la cantidad de zonas o dispositivos. |

CA-10 : `detalle_zona.html` (clase `table-responsive`) | La tabla de dispositivos permite scroll horizontal dentro de su contenedor sin desbordar la página. 

CA-11 : `base.html`, `lista_zonas.html`, `detalle_zona.html` | Header, navegación, tarjetas, tabla y botones mantienen estilo Bootstrap coherente en todas las páginas. 

CA-12 : `detalle_zona.html` (badge con texto + ícono) | El estado se comunica con texto ("NORMAL"/"ALERTA") y símbolo (✓/⚠), no solo con color. 

CA-13 : Proyecto completo | Se ejecutó `python manage.py check` sin errores; el proyecto corre siguiendo los pasos del `README.md`. 