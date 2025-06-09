import flet as ft

def add_classroom(page: ft.Page):

    def new_dialog(e):
        from grid import load_grid

        aula_numero = classroom_number_field.value.strip()
        aula_ip_suffix = classroom_ip_field.value.strip()
        aula_ip = f"192.168.0.{aula_ip_suffix}"

        if not aula_numero or not classroom_ip_field.value:
            page.open(
                ft.SnackBar(ft.Text("Por favor, complete ambos campos."), open=True)
            )
            page.update()
            return
        
        if not aula_numero.isdigit():
            page.open(
                ft.SnackBar(
                    ft.Text("Error: El número de salón debe ser solo números.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                    open=True
                )
            )
            page.update()
            classroom_number_field.focus()
            return

        if not aula_ip_suffix.isdigit():
            page.open(
                ft.SnackBar(
                    ft.Text("Error: La dirección IP debe ser solo números.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                    open=True
                )
            )
            page.update()
            classroom_ip_field.focus()
            return

        key_to_check = f"Aula {aula_numero}"

        if page.client_storage.contains_key(key_to_check):
            page.open(
                ft.SnackBar(
                    ft.Text(
                        f"Error: El aula '{aula_numero}' ya existe. Por favor, elija otro número.",
                        color=ft.Colors.WHITE),
                        bgcolor=ft.Colors.RED_700,
                        open=True
                )
            )
            page.update()
            classroom_number_field.focus()
            return
        
        for key in page.client_storage.get_keys("Aula"):
            stored_data = page.client_storage.get(key)
            if stored_data and len(stored_data) > 1 and stored_data[1] == aula_ip:
                existing_aula_number = key.replace("Aula ", "")
                page.open(
                    ft.SnackBar(
                        ft.Text(
                            f"Error: La IP '{aula_ip}' ya está en uso por el aula '{existing_aula_number}'.",
                            color=ft.Colors.WHITE
                        ),
                        bgcolor=ft.Colors.RED_700,
                        open=True
                    )
                )
                page.update()
                classroom_ip_field.focus()
                return

        page.client_storage.set(
            key_to_check,
            [1, aula_ip]
        )
        
        page.close(add_dialog)
        load_grid(page)
        page.update()

    classroom_number_field = ft.TextField(
        label="N° de salon",
        value="",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=lambda e: classroom_ip_field.focus()
    )

    classroom_ip_field = ft.TextField(
        label="IP del Salon",
        prefix_text="192.168.0.",
        value="",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=lambda e: new_dialog(e)
    )

    add_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Agregar Salon"),
        content=ft.Column(
            [
                classroom_number_field,
                classroom_ip_field,
            ],
            tight=True,
        ),
        actions=[
            ft.TextButton("Cerrar", on_click=lambda e: page.close(add_dialog)),
            ft.TextButton("Guardar", on_click=new_dialog),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.open(add_dialog)
    classroom_number_field.focus()
    page.update()