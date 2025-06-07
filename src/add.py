import flet as ft

def add_classroom(page: ft.Page):

    def new_dialog(e):
        from grid import load_grid
        page.client_storage.set(f"Aula {classroom_number_field.value}",0)
        page.close(add_dialog)
        load_grid(page)
        page.update()

    classroom_number_field = ft.TextField(
        label="N° de salon",
        value="",
        keyboard_type=ft.KeyboardType.NUMBER
    )

    add_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar Salon"),
        content=classroom_number_field,
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(add_dialog)),
            ft.TextButton("Guardar", on_click=new_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.open(add_dialog)
    page.update()