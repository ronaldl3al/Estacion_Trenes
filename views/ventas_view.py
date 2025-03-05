# views/ventas_view.py
import flet as ft
import threading, time
from datetime import datetime
import models.estacion as modelo_estacion 
from utils.helpers import mostrar_mensaje, toggle_theme

def build_schedule_view(horarios):
    pastel_colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]
    schedule_items = []
    for i, horario in enumerate(horarios):
        color = pastel_colors[i % len(pastel_colors)]
        schedule_items.append(
            ft.Container(
                content=ft.Text(horario, color="black"),
                bgcolor=color,
                padding=5,
                border_radius=5,
                margin=ft.Margin(left=0, top=0, right=5, bottom=0)
            )
        )
    return ft.Row(schedule_items, wrap=True)


def vista_ventas(page):
    estacion = modelo_estacion.usuario_actual  # usuario actual del módulo
    if estacion is None:
        mostrar_mensaje(page, "Error: usuario no autenticado", tipo="error")
        page.go("/login")
        return

    tickets_vendidos = 0

    def actualizar_hora_fecha():
        while True:
            hora_actual.value = datetime.now().strftime("%H:%M:%S")
            fecha_actual.value = datetime.now().strftime("%d/%m/%Y")
            page.update()
            time.sleep(1)
    
    hora_actual = ft.Text("00:00:00")
    fecha_actual = ft.Text("00/00/0000")
    contador_tickets = ft.Text(f"Tickets vendidos: {tickets_vendidos}")
    
    threading.Thread(target=actualizar_hora_fecha, daemon=True).start()
    
    sidebar = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(f"Hola, {estacion.operador}", size=18, color=ft.colors.WHITE),
                ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=lambda e: toggle_theme(page))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text("Estado: Activo", size=14, color=ft.colors.GREY_400),
            ft.Divider(color="#4511ED"),
            ft.Text(estacion.nombre, size=16, color=ft.colors.WHITE),
            ft.Text("Horarios:", size=14, color=ft.colors.GREY_400),
            build_schedule_view(estacion.horarios),
            ft.Divider(color="#4511ED"),
            ft.ElevatedButton(
                "Generar PDF",
                icon=ft.icons.PICTURE_AS_PDF,
                bgcolor="#4511ED",
                color="white",
                on_click=lambda e: mostrar_mensaje(page, "PDF generado", tipo="pdf")
            ),
            ft.ElevatedButton(
                        "Gestionar Horarios",
                        icon=ft.icons.SCHEDULE,
                        bgcolor="#4511ED",
                        color="white",
                        on_click=lambda e: page.go("/horarios")
                    ),
            hora_actual,
            fecha_actual,
            contador_tickets,
            ft.IconButton(
                icon=ft.icons.LOGOUT,
                icon_color=ft.colors.RED_400,
                on_click=lambda e: page.go("/login")
            )
        ], spacing=15),
        bgcolor="#2C2C2C",
        padding=20,
        width=300,
        border_radius=10
    )
    
    destino = ft.Dropdown(
        label="Destino",
        options=[ft.dropdown.Option(e.nombre) for e in modelo_estacion.estaciones if e != estacion]
    )
    
    horario = ft.Dropdown(
        label="Horario",
        options=[ft.dropdown.Option(h) for h in estacion.horarios]
    )
    
    cantidad = ft.TextField(label="Cantidad", keyboard_type=ft.KeyboardType.NUMBER)
    tipo = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Adulto", label="Adulto"),
            ft.Radio(value="Nino", label="Niño (50% descuento)")
        ])
    )
    
    total = ft.Text("Total: $0.00", size=20, weight=ft.FontWeight.BOLD)
    
    def calcular_total(e):
        try:
            precio = estacion.precio * (0.5 if tipo.value == "Nino" else 1)
            total.value = f"Total: ${float(cantidad.value) * precio:.2f}"
            page.update()
        except:
            pass
    
    cantidad.on_change = calcular_total
    tipo.on_change = calcular_total
    
    contenido_ventas = ft.Column(
        [
            ft.Text("Venta de Boletos", size=24),
            ft.Row([destino, horario], spacing=20),
            cantidad,
            tipo,
            total,
            ft.ElevatedButton(
                "Generar Boleto",
                icon=ft.icons.CONFIRMATION_NUM_OUTLINED,
                on_click=lambda e: vender_boleto()
            )
        ],
        spacing=20,
        expand=True
    )
    
    def vender_boleto():
        nonlocal tickets_vendidos
        try:
            if not all([destino.value, horario.value, cantidad.value, tipo.value]):
                raise Exception("Complete todos los campos")
            
            tickets_vendidos += int(cantidad.value)
            contador_tickets.value = f"Tickets vendidos: {tickets_vendidos}"
            mostrar_mensaje(page, f"{cantidad.value} boleto(s) vendido(s)!", tipo="success")
            page.update()
        except Exception as ex:
            mostrar_mensaje(page, f"Error: {str(ex)}", tipo="error")
    
    return ft.View(
        "/ventas",
        [
            ft.AppBar(
                title=ft.Text(f"Estación {estacion.nombre}"),
                actions=[
                    ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=lambda e: toggle_theme(page)),
                    ft.IconButton(ft.icons.LOGOUT, icon_color=ft.colors.RED_400, on_click=lambda e: page.go("/login"))
                ]
            ),
            ft.Row([sidebar, ft.VerticalDivider(), contenido_ventas], expand=True)
        ]
    )
