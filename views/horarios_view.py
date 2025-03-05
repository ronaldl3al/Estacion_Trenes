# views/horarios_view.py
import flet as ft
import models.estacion as modelo_estacion
from models.estacion import estaciones
from utils.helpers import toggle_theme

def vista_horarios(page):
    pastel_colors = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]

    rows = []
    for idx, est in enumerate(estaciones):
        color = pastel_colors[idx % len(pastel_colors)]
        horarios_str = ", ".join(est.horarios) if est.horarios else "Sin Horarios"
        station_cell = ft.DataCell(
            ft.Container(
                content=ft.Text(est.nombre, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK),
                bgcolor=color,
                padding=ft.Padding(left=8, top=8, right=8, bottom=8),
                border_radius=8
            )
        )
        horarios_cell = ft.DataCell(
            ft.Container(
                content=ft.Text(horarios_str),
                padding=ft.Padding(left=8, top=8, right=8, bottom=8)
            )
        )
        rows.append(
            ft.DataRow(
                cells=[
                    station_cell,
                    horarios_cell
                ]
            )
        )

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Estación", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Horarios", weight=ft.FontWeight.BOLD)),
        ],
        rows=rows,
        heading_row_color=ft.colors.BLUE_GREY_200,
        border=ft.border.all(1, ft.colors.BLUE_GREY),
        divider_thickness=1,
        expand=True
    )

    return ft.View(
        "/horarios",
        [
            ft.AppBar(
                title=ft.Text("Horarios Registrados"),
                actions=[
                    ft.IconButton(ft.icons.BRIGHTNESS_6, on_click=lambda e: toggle_theme(page)),
                    ft.IconButton(
                        ft.icons.ARROW_BACK,
                        on_click=lambda e: page.go("/panel") if modelo_estacion.usuario_actual.operador == "admin" else page.go("/ventas")
                    )
                ]
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Listado de Horarios Registrados", size=24, weight=ft.FontWeight.BOLD),
                        table
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=20,
                alignment=ft.alignment.center
            )
        ]
    )
