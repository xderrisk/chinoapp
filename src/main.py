import flet as ft
import asyncio
from grid import load_grid
from add import add_classroom

def main(page: ft.Page):
    page.title = "chinoapp"
    page.appbar = ft.AppBar(
        title=ft.Text("Estado de Aulas"),
        actions=[
            ft.IconButton(ft.Icons.ADD, on_click=lambda e: add_classroom(page)),
            ft.IconButton(ft.Icons.UPDATE, on_click=lambda e: load_grid(page))
        ]
    )

    # async def refresh_grid_periodically():
    #     while True:
    #         await asyncio.sleep(5)
    #         load_grid(page)

    # page.run_task(refresh_grid_periodically)

    page.update()

ft.app(main)