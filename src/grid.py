import flet as ft

def load_grid(page: ft.Page):

    classroom_keys = page.client_storage.get_keys("Aula")
    classroom_containers = []

    for key in classroom_keys:
        aula_numero = key
        value = page.client_storage.get(key)
        aula_ip = value[1]
        aula_numero = key.replace("Aula ", "")
        if value[0] == 1:
            colorStatus = ft.Colors.RED
        else:
            colorStatus = ft.Colors.GREEN

        content_controls = [
                ft.Text(aula_numero, weight=ft.FontWeight.BOLD),
            ]
        if page.show_ips_globally:
                content_controls.append(
                    ft.Text(aula_ip, size=10, color=ft.Colors.GREY_300)
                )
        
            
        cuadrado = ft.Container(
            content=ft.Column(
                content_controls,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=5
            ),
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
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )
    page.update()