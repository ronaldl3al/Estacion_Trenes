# views/admin_panel_view.py
import flet as ft
from models.estacion import estaciones
from models.estacion import Estacion 
from utils.helpers import mostrar_mensaje, generar_archivo_ventas, toggle_theme

def vista_panel_admin(page):
    def crear_estacion(e):
        try:
            nueva_est = Estacion(
                operador=campo_operador.value,
                contrasena=campo_contrasena_nueva.value,
                nombre=campo_nombre_estacion.value,
                horarios=[h.strip() for h in campo_horarios.value.split(",")],
                precio=float(campo_precio.value)
            )
            
            estaciones.append(nueva_est)
            generar_archivo_ventas(nueva_est)
            mostrar_mensaje(page, "Estación creada!", tipo="success")
            limpiar_formulario()
        except Exception as ex:
            mostrar_mensaje(page, f"Error: {str(ex)}", tipo="error")
    
    def limpiar_formulario():
        campo_operador.value = ""
        campo_contrasena_nueva.value = ""
        campo_nombre_estacion.value = ""
        campo_horarios.value = ""
        campo_precio.value = "1.0"
        page.update()
    
    # formulario
    campo_operador = ft.TextField(label="Nombre del operador")
    campo_contrasena_nueva = ft.TextField(label="Contraseña", password=True)
    campo_nombre_estacion = ft.TextField(label="Nombre de la estación")
    campo_horarios = ft.TextField(label="Horarios (separar por comas)")
    campo_precio = ft.TextField(label="Precio base", value="1.0")
    
    # ----------------------------------------------------------------
    # Sidebar con información general de las estaciones
    # ----------------------------------------------------------------
    total_boletos = sum(est.boletos_vendidos for est in estaciones)
    active_operators = sum(1 for est in estaciones if est.estado == "Activo")
    inactive_operators = sum(1 for est in estaciones if est.estado != "Activo")
    stations_list = [ft.Text(est.nombre, color=ft.colors.WHITE) for est in estaciones]

    sidebar = ft.Container(
        content=ft.Column([
            ft.Text("Información General", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ft.Divider(color="#4511ED"),
            ft.Text(f"Total Boletos Vendidos: {total_boletos}", color=ft.colors.WHITE),
            ft.Text("Estaciones Registradas:", color=ft.colors.WHITE),
            ft.Column(stations_list, spacing=5),
            ft.Divider(color="#4511ED"),
            ft.Text(f"Operadores Activos: {active_operators}", color=ft.colors.WHITE),
            ft.Text(f"Operadores Inactivos: {inactive_operators}", color=ft.colors.WHITE),
            ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=lambda e: toggle_theme(page))
        ], spacing=15),
        bgcolor="#2C2C2C",
        padding=20,
        width=300,
        border_radius=10
    )

    # Formulario de creación de estación
    create_station_form = ft.Column([
        ft.Text("Crear Nueva Estación", size=24),
        ft.Column([
            campo_operador,
            campo_contrasena_nueva,
            campo_nombre_estacion,
            campo_horarios,
            campo_precio,
            ft.ElevatedButton("Crear Estación", on_click=crear_estacion)
        ], width=400)
    ], spacing=20)

    #Sidebar + Formulario
    content = ft.Row([
        sidebar,
        ft.VerticalDivider(width=20),
        create_station_form
    ], expand=True)

    return ft.View(
        "/panel",
        [
            ft.AppBar(
                title=ft.Text("Panel Admin - Crear Estaciones"),
                actions=[
                    ft.IconButton(ft.icons.LOGOUT, on_click=lambda _: page.go("/login")),
                    ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=lambda _: toggle_theme(page))
                ]
            ),
            content
        ]
    )
