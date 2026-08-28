from django.shortcuts import render
from django.http import HttpResponse, Http404

from .services import (
    cargar_dispositivos,
    obtener_zonas_con_resumen,
    obtener_detalle_zona,
)


def inicio(request):
    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
    }
    return render(
        request,
        "dispositivos/inicio.html",
        contexto,
    )


def dispositivos_zona(request, zona_id):
    if zona_id != 3:
        return HttpResponse(
            "Zona no encontrada", status=404
        )
    return HttpResponse(
        f"Dispositivos de la zona {zona_id}"
    )


def estado_dispositivo(request, dispositivo_id):
    if dispositivo_id != 1:
        return HttpResponse(
            "Dispositivo no encontrado", status=404
        )
    return HttpResponse(
        f"Estado del dispositivo {dispositivo_id}: activo"
    )


def lista_zonas(request):
    zonas = obtener_zonas_con_resumen()

    contexto = {
        "zonas": zonas,
        "total_zonas": len(zonas),
    }

    return render(request, "dispositivos/lista_zonas.html", contexto)


def detalle_zona(request, zona_id):
    detalle = obtener_detalle_zona(zona_id)

    if detalle is None:
        raise Http404("La zona solicitada no existe.")

    return render(request, "dispositivos/detalle_zona.html", detalle)


def resumen_zonas(request):
    zonas = obtener_zonas_con_resumen()

    total_zonas = len(zonas)
    total_dispositivos = sum(zona["cantidad_dispositivos"] for zona in zonas)
    consumo_total = sum(zona["consumo_total"] for zona in zonas)

    contexto = {
        "zonas": zonas,
        "total_zonas": total_zonas,
        "total_dispositivos": total_dispositivos,
        "consumo_total": consumo_total,
    }

    return render(
        request,
        "dispositivos/resumen_zonas.html",
        contexto,
    )


