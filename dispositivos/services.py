import json
from django.conf import settings


def _cargar_json(nombre_archivo):
    ruta = settings.BASE_DIR / "data" / nombre_archivo
    with ruta.open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    if not isinstance(datos, list):
        raise ValueError(f"Se esperaba una lista en {nombre_archivo}")
    return datos


def cargar_zonas():
    return _cargar_json("zonas.json")


def cargar_categorias():
    return _cargar_json("categorias.json")


def cargar_dispositivos():
    return _cargar_json("dispositivos.json")


def obtener_zonas_con_resumen():
    zonas = cargar_zonas()
    dispositivos = cargar_dispositivos()

    resumen = []

    for zona in zonas:
        dispositivos_zona = [
            d for d in dispositivos
            if d["zona_id"] == zona["id"]
        ]

        consumo_total = sum(
            d["consumo_kwh"] for d in dispositivos_zona
        )

        estado = (
            "LÍMITE SUPERADO"
            if consumo_total > zona["limite_kwh"]
            else "DENTRO DEL LIMITE"

        )

        resumen.append({
            "id": zona["id"],
            "nombre": zona["nombre"],
            "cantidad_dispositivos": len(dispositivos_zona),
            "consumo_total": consumo_total,
            "limite_kwh": zona["limite_kwh"],
            "estado": estado,
        })

    return resumen


def obtener_detalle_zona(zona_id):
    zonas = cargar_zonas()
    categorias = cargar_categorias()
    dispositivos = cargar_dispositivos()

    zona = next((z for z in zonas if z["id"] == zona_id), None)
    if zona is None:
        return None

    categorias_por_id = {c["id"]: c["nombre"] for c in categorias}

    dispositivos_zona = []
    consumo_total = 0
    for d in dispositivos:
        if d["zona_id"] == zona_id:
            dispositivos_zona.append({
                "nombre": d["nombre"],
                "categoria": categorias_por_id.get(
                    d["categoria_id"], "Sin categoría"
                ),
                "consumo_kwh": d["consumo_kwh"],
            })
            consumo_total += d["consumo_kwh"]

    estado = "ALERTA" if consumo_total > zona["limite_kwh"] else "NORMAL"

    return {
        "zona": zona,
        "dispositivos": dispositivos_zona,
        "consumo_total": consumo_total,
        "estado": estado,
    }