import flet as ft
# import asyncio
from grid import load_grid
from add import add_classroom
from remove import remove_classroom

def main(page: ft.Page):
    page.title = "chinoapp"

    page.show_ips_globally = False 
    def toggle_show_ips(e):
        page.show_ips_globally = not page.show_ips_globally
        load_grid(page)
        if page.show_ips_globally:
            e.control.icon = ft.Icons.VISIBILITY_OFF
        else:
            e.control.icon = ft.Icons.VISIBILITY
        page.update()

    page.appbar = ft.AppBar(
        title=ft.Text("Estado de Aulas"),
        actions=[
            ft.IconButton(ft.Icons.VISIBILITY_OFF, on_click=toggle_show_ips),
            ft.IconButton(ft.Icons.ADD, on_click=lambda e: add_classroom(page)),
            ft.IconButton(ft.Icons.REMOVE, on_click=lambda e: remove_classroom(page)),
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