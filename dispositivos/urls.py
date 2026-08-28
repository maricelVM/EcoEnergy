from django.urls import path
from . import views

app_name = "dispositivos"

urlpatterns = [
    path("", views.inicio, name="inicio"),

    path(
        "zonas/",
        views.lista_zonas,
        name="lista_zonas",
    ),

    path(
        "zonas/<int:zona_id>/",
        views.detalle_zona,
        name="detalle_zona",
    ),

    path(
        "resumen-zonas/",
        views.resumen_zonas,
        name="resumen_zonas",
    ),

    path(
        "zonas/<int:zona_id>/dispositivos/",
        views.dispositivos_zona,
        name="por_zona",
    ),

    path(
        "dispositivos/<int:dispositivo_id>/estado/",
        views.estado_dispositivo,
        name="estado",
    ),
]