import flet as ft

def load_grid(page: ft.Page):

    classroom_keys = page.client_storage.get_keys("Aula")
    classroom_containers = []

    for key in classroom_keys:
        value = page.client_storage.get(key)
        if value == 1:
            colorStatus = ft.Colors.RED
        else:
            colorStatus = ft.Colors.GREEN
        aula_numero = key
            
        cuadrado = ft.Container(
            content=ft.Text(aula_numero),
            width=100,
            height=100,
            bgcolor=colorStatus,
            border_radius=10,
            alignment=ft.alignment.center
        )
        classroom_containers.append(cuadrado)

    page.controls.clear()

    page.add(
        ft.Row(
            controls=classroom_containers,
            wrap=True,
            spacing=10,
            run_spacing=10,
            alignment=ft.MainAxisAlignment.SPACE_AROUND
        )
    )
    page.update()