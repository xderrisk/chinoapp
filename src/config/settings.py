import flet as ft

# Esta función se encargará de mostrar el diálogo de ajustes.
# Necesita 'page' para poder añadir el diálogo al overlay de la página.
def open_settings_dialog(page: ft.Page):

    # Función auxiliar para cerrar el diálogo
    def close_dialog(e):
        settings_dialog.open = False
        page.overlay.remove(settings_dialog) # Limpia el diálogo del overlay
        page.update()

    # Define el contenido del diálogo de ajustes
    settings_dialog = ft.AlertDialog(
        modal=True, # Hace que el diálogo sea modal (bloquea la interacción con el fondo)
        title=ft.Text("Configuración de la Aplicación"),
        content=ft.Column(
            [
                ft.Text("Aquí puedes ajustar las opciones de tu app."),
                ft.Switch(label="Habilitar Modo Oscuro", value=False),
                ft.TextField(label="Nombre de Usuario", value="Usuario ChinoApp"),
                ft.Dropdown(
                    label="Idioma",
                    options=[
                        ft.dropdown.Option("Español"),
                        ft.dropdown.Option("Inglés"),
                    ]
                ),
            ],
            spacing=10, # Espacio entre los controles
        ),
        actions=[
            ft.TextButton("Cerrar", on_click=close_dialog),
            # Podrías añadir un botón de "Guardar" aquí si tus ajustes necesitan ser guardados
            # ft.ElevatedButton("Guardar", on_click=save_settings)
        ],
        actions_alignment=ft.MainAxisAlignment.END, # Alinea los botones a la derecha
    )

    # Añade el diálogo al overlay de la página
    page.overlay.append(settings_dialog)
    # Abre el diálogo
    settings_dialog.open = True
    # Actualiza la página para mostrar el diálogo
    page.update()