# views/ventas_view.py
import flet as ft
import threading, time
from datetime import datetime
import models.estacion as modelo_estacion 
from utils.helpers import mostrar_mensaje, toggle_theme

def construir_horarios(horarios):
    colores_pastel = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]
    elementos_horarios = []
    for i, horario in enumerate(horarios):
        color = colores_pastel[i % len(colores_pastel)]
        elementos_horarios.append(
            ft.Container(
                content=ft.Text(horario, color="black"),
                bgcolor=color,
                padding=5,
                border_radius=5,
                margin=ft.Margin(left=0, top=0, right=5, bottom=0)
            )
        )
    return ft.Row(elementos_horarios, wrap=True)

def vista_ventas(page):
    estacion = modelo_estacion.usuario_actual  # Usuario actual del módulo
    if estacion is None:
        mostrar_mensaje(page, "Error: usuario no autenticado", tipo="error")
        page.go("/login")
        return

    boletos_vendidos = 0

    def actualizar_hora_fecha():
        while True:
            texto_hora.value = datetime.now().strftime("%H:%M:%S")
            texto_fecha.value = datetime.now().strftime("%d/%m/%Y")
            page.update()
            time.sleep(1)
    
    texto_hora = ft.Text("00:00:00")
    texto_fecha = ft.Text("00/00/0000")
    texto_boletos = ft.Text(f"Boletos vendidos: {boletos_vendidos}")
    
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
            construir_horarios(estacion.horarios),
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
            texto_hora,
            texto_fecha,
            texto_boletos,
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
    
    # Campos de cantidad reducidos y en la misma línea para adultos, niños y adultos mayores
    cantidad_adultos = ft.TextField(label="Adultos", keyboard_type=ft.KeyboardType.NUMBER, value="0", width=100)
    cantidad_niños = ft.TextField(label="Niños", keyboard_type=ft.KeyboardType.NUMBER, value="0", width=100)
    cantidad_adultos_mayores = ft.TextField(label="Adultos Mayores", keyboard_type=ft.KeyboardType.NUMBER, value="0", width=100)
    
    # Se muestran los precios de cada uno junto a los campos
    fila_precios = ft.Row(
        [
            ft.Column(
                [
                    cantidad_adultos,
                    ft.Text(f"Precio Adulto: ${estacion.precio:.2f}", size=12)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Column(
                [
                    cantidad_niños,
                    ft.Text(f"Precio Niño: ${(estacion.precio * 0.5):.2f}", size=12)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            ft.Column(
                [
                    cantidad_adultos_mayores,
                    ft.Text(f"Precio Adulto Mayor: ${(estacion.precio * 0.4):.2f}", size=12)
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        ],
        spacing=20
    )
    
    total = ft.Text("Total: $0.00", size=20, weight=ft.FontWeight.BOLD)
    
    def calcular_total(e):
        try:
            num_adultos = float(cantidad_adultos.value) if cantidad_adultos.value else 0
            num_niños = float(cantidad_niños.value) if cantidad_niños.value else 0
            num_adultos_mayores = float(cantidad_adultos_mayores.value) if cantidad_adultos_mayores.value else 0
            total_valor = (num_adultos * estacion.precio) + \
                          (num_niños * estacion.precio * 0.5) + \
                          (num_adultos_mayores * estacion.precio * 0.4)
            total.value = f"Total: ${total_valor:.2f}"
            page.update()
        except Exception as ex:
            print(ex)
    
    cantidad_adultos.on_change = calcular_total
    cantidad_niños.on_change = calcular_total
    cantidad_adultos_mayores.on_change = calcular_total
    
    contenido_ventas = ft.Column(
        [
            ft.Text("Venta de Boletos", size=24),
            ft.Row([destino, horario], spacing=20),
            fila_precios,
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
        nonlocal boletos_vendidos
        try:
            if not all([destino.value, horario.value]) or (cantidad_adultos.value == "" and 
                                                            cantidad_niños.value == "" and 
                                                            cantidad_adultos_mayores.value == ""):
                raise Exception("Complete todos los campos")
            
            num_adultos = int(cantidad_adultos.value) if cantidad_adultos.value else 0
            num_niños = int(cantidad_niños.value) if cantidad_niños.value else 0
            num_adultos_mayores = int(cantidad_adultos_mayores.value) if cantidad_adultos_mayores.value else 0
            
            total_boletos = num_adultos + num_niños + num_adultos_mayores
            if total_boletos == 0:
                raise Exception("La cantidad de boletos no puede ser 0")
            
            boletos_vendidos += total_boletos
            texto_boletos.value = f"Boletos vendidos: {boletos_vendidos}"
            mostrar_mensaje(page, f"{total_boletos} boleto(s) vendido(s)!", tipo="success")
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
