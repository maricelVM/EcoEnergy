from django.http import HttpResponse

def inicio(request):
    return HttpResponse(
        "<h1>EcoEnergy</h1>"
        "<p>Back End en funcionamiento</p>"
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
