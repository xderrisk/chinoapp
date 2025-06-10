import flet as ft

def remove_classroom(page: ft.Page):

    def delete_dialog(e):
        from grid import load_grid
        aula_numero = delete_classroom_number_field.value.strip()
        if not aula_numero.isdigit():
            page.open(
                ft.SnackBar(
                    ft.Text("Error: El número de salón debe ser solo números.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                    open=True
                )
            )
            page.update()
            delete_classroom_number_field.focus()
            return
        
        key_to_delete = f"Aula {aula_numero}"
        if page.client_storage.contains_key(key_to_delete):
            page.client_storage.remove(key_to_delete)
            page.close(remove_dialog)
            load_grid(page) 
            page.open(
                ft.SnackBar(
                    ft.Text(f"Aula '{aula_numero}' eliminada con éxito."),
                    open=True
                )
            )
        else:
            page.open(
                ft.SnackBar(
                    ft.Text(f"Error: El aula '{aula_numero}' no existe.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                    open=True
                )
            )
            delete_classroom_number_field.focus()
        
    delete_classroom_number_field = ft.TextField(
        label="N° de aula a eliminar",
        value="",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=lambda e: delete_dialog(e)
    )

    remove_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Eliminar Salon"),
        content=ft.Column(
            [
                delete_classroom_number_field,
            ],
            tight=True,
        ),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(remove_dialog)),
            ft.TextButton("Borrar", on_click=delete_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.open(remove_dialog)
    delete_classroom_number_field.focus()
    page.update()