# views/login_view.py
import flet as ft
import models.estacion as modelo_estacion 
from utils.helpers import mostrar_mensaje

def vista_login(page):
    def validar_ingreso(e):
        for est in modelo_estacion.estaciones:
            if campo_usuario.value == est.operador and campo_contrasena.value == est.contrasena:
                modelo_estacion.usuario_actual = est 
                page.go("/ventas" if est.operador != "admin" else "/panel")
                return
        mostrar_mensaje(page, "Credenciales incorrectas", tipo="error")

    # ----------------------------------------------------------------
    # Logo y mensaje de bienvenida
    # ----------------------------------------------------------------
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
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        width=300,
        height=50,
        border_radius=16,
        prefix_icon=ft.icons.LOGIN,
        focused_border_color="#4511ED",
        focus_color="#4511ED",      
    )
    campo_contrasena = ft.TextField(
        label="Contraseña",
        password=True,
        filled=True,
        border_color="#F4F9FA",
        bgcolor=ft.colors.TRANSPARENT,
        width=300,
        height=50,
        border_radius=16,
        can_reveal_password=True,
        prefix_icon=ft.icons.PASSWORD,
        focused_border_color="#4511ED",
    )

    # ----------------------------------------------------------------
    # Botón para iniciar sesión
    # ----------------------------------------------------------------
    login_btn = ft.ElevatedButton(
        text="INICIAR",
        on_click=validar_ingreso,
        bgcolor="#4511ED",
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
        width=600,
        height=630,
        bgcolor="#121212",
        border_radius=16,
        alignment=ft.alignment.center,
        image_src="https://i.ibb.co/KcJtwGpG/upscalemedia-transformed-2-1.png",
        image_fit=ft.ImageFit.COVER,
    )

    # ----------------------------------------------------------------
    # Contenedor principal 
    # ----------------------------------------------------------------
    main_container = ft.Container(
        content=ft.Row(
            [
                ft.Container(expand=1),  
                login_container,
                ft.Container(expand=1), 
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        expand=True,
        alignment=ft.alignment.center,
    )

    return ft.View(
        "/login",
        [
            ft.AppBar(title=ft.Text("Bienvenido")),
            main_container
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
