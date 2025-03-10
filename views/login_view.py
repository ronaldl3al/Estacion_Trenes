import flet as ft
import models.estacion as modelo_estacion 
from utils.helpers import mostrar_mensaje

def vista_login(page):
    # Establecer el modo oscuro al iniciar
    page.theme_mode = ft.ThemeMode.DARK

    def validar_ingreso(e):
        # Primero, verificar si las credenciales corresponden al admin
        if (campo_usuario.value.lower() == modelo_estacion.admin_credentials["operador"].lower() and 
            campo_contrasena.value == modelo_estacion.admin_credentials["contrasena"]):
            # Creamos un objeto simple para representar al admin
            admin = type("Admin", (), {})()
            admin.operador = modelo_estacion.admin_credentials["operador"]
            admin.contrasena = modelo_estacion.admin_credentials["contrasena"]
            modelo_estacion.usuario_actual = admin
            page.go("/panel")
            return

        # Verificar las credenciales de las estaciones (operadores)
        for est in modelo_estacion.estaciones:
            if campo_usuario.value == est.operador and campo_contrasena.value == est.contrasena:
                modelo_estacion.usuario_actual = est 
                page.go("/ventas")
                return
        mostrar_mensaje(page, "Credenciales incorrectas", tipo="error")

    logo = ft.Text(
        "Trenes Venezuela",
        size=40,
        weight=ft.FontWeight.BOLD,
        color="#F4F9FA",
        font_family="Arial Black italic"
    )
    bienvenido = ft.Text(
        "¡Bienvenido de vuelta!",
        weight=ft.FontWeight.BOLD,
        size=20,
        color="#F4F9FA"
    )

    # ----------------------------------------------------------------
    # Campos de entrada para el usuario y la contraseña
    # ----------------------------------------------------------------
    campo_usuario = ft.TextField(
        label="Usuario",
        label_style=ft.TextStyle(color="#F4F9FA", size=20), 
        text_style=ft.TextStyle(color=ft.colors.WHITE),  
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        width=300,
        height=50,
        border_radius=7,
        prefix_icon=ft.icons.LOGIN,
        focused_border_color="#A7107F",
        focus_color="#A7107F",      
    )

    campo_contrasena = ft.TextField(
        label="Contraseña",
        label_style=ft.TextStyle(color="#F4F9FA", size=20),
        text_style=ft.TextStyle(color=ft.colors.WHITE),  
        password=True,
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        width=300,
        height=50,
        border_radius=7,
        can_reveal_password=True,
        prefix_icon=ft.icons.PASSWORD,
        focused_border_color="#A7107F",
        focus_color="#A7107F",     
    )

    # ----------------------------------------------------------------
    # Botón para iniciar sesión
    # ----------------------------------------------------------------
    login_btn = ft.ElevatedButton(
        text="INICIAR",
        on_click=validar_ingreso,
        bgcolor="#A7107F",
        color=ft.colors.WHITE,
    )

    # ----------------------------------------------------------------
    # Contenedor del formulario de inicio de sesión
    # ----------------------------------------------------------------
    login_container = ft.Container(
        content=ft.Column(
            [
                logo,
                ft.Container(height=30), 
                bienvenido,
                ft.Container(height=20),  
                campo_usuario,
                campo_contrasena,
                ft.Row([login_btn], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        ),
        padding=30,
        width=500,
        height=600,
        border_radius=16,
        alignment=ft.alignment.center,
        blur=ft.Blur(sigma_x=15, sigma_y=15),  
        border=ft.Border(
            left=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            top=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            right=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
            bottom=ft.BorderSide(color=ft.colors.WHITE12, width=1.5),
        ),
    )

    # ----------------------------------------------------------------
    # Contenedor principal con imagen de fondo
    # ----------------------------------------------------------------
    background_container = ft.Container(
        content=ft.Stack(
            [
                ft.Column(
                    [
                        ft.Container(expand=1),  
                        ft.Row([login_container], alignment=ft.MainAxisAlignment.CENTER),
                        ft.Container(expand=1), 
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ]
        ),
        expand=True,
        alignment=ft.alignment.center,
        image_src="https://i.ibb.co/B2rfDdMd/3312580.jpg",
        image_fit=ft.ImageFit.COVER,
        border_radius=16,
        blur=ft.Blur(sigma_x=10, sigma_y=10),  
    )

    return ft.View(
        "/login",
        [background_container],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
