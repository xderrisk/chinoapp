import flet as ft
from grid import load_grid

def add_classroom(page: ft.Page):
    def close_dialog(e):
        page.close(add_dialog)
        page.update()

    def new_dialog(e):
        page.client_storage.set(f"Aula {classroom_number_field.value}",0)
        page.close(add_dialog)
        load_grid(page)
        page.update()

    classroom_number_field = ft.TextField(label="N° de salon", value="", keyboard_type=ft.KeyboardType.NUMBER)
    add_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar Salon"),
        content=classroom_number_field,
        actions=[
            ft.TextButton("Guardar", on_click=new_dialog),
            ft.TextButton("Cerrar", on_click=close_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.open(add_dialog)
    page.update()