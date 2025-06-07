import flet as ft

# Define las constantes de color aquí, si solo se usan en este archivo
# o asegúrate de importarlas si las tienes definidas globalmente en otro lugar.
W = ft.Colors.WHITE
BG = ft.Colors.BLUE_GREY_900
B = ft.Colors.BLACK


def Dialog(title, content, lista):
    d = ft.AlertDialog(  # Usa ft.AlertDialog
        open=False,
        title=ft.Text(title, color=W),  # Usa ft.Text
        content=ft.Text(content, color=W),  # Usa ft.Text
        actions=lista,
        bgcolor=BG,
        icon_padding=ft.padding.only(top=20, bottom=10),  # ft.padding
        actions_alignment=ft.MainAxisAlignment.END
    )
    return d

# Declara dialog5 a nivel global en este módulo si lo necesitas fuera de add_classroom,
# o pásalo como argumento si solo lo usas dentro de add_classroom.
# En este caso, lo declararemos dentro de add_classroom para mantenerlo encapsulado,
# ya que su uso está atado a la lógica de navegación/cierre del diálogo.

def add_classroom(page: ft.Page):
    # La instancia del diálogo de salida se creará cada vez que se llame a add_classroom,
    # lo cual es aceptable si este diálogo se usa específicamente para la salida
    # desde la lógica de "add_classroom".
    # Si quieres un único diálogo global para toda la app, tendrías que mover
    # su definición a main.py o a un módulo de utilidades.
    dialog5 = Dialog("Exit.", "Want to exit?", [
        ft.TextButton("No", on_click=lambda e: close_dialog(e, dialog5)), # Pasa el diálogo
        ft.TextButton("Yes", on_click=lambda e: Destroy()) # Pasa el evento
    ])

    def close_dialog(e, dialog_to_close):
        dialog_to_close.open = False
        page.update()

    def Destroy():
        page.window.destroy()

    def BACK(view_event):
        # Esta función `BACK` solo tiene sentido si `add_classroom` controla
        # la lógica de retroceso global, lo cual generalmente no es el caso.
        # `page.on_view_pop` se asigna en `main.py` (o en un módulo global de ruteo).
        # Si esta `BACK` es para la app completa, debería estar en `main.py`
        # o en un módulo de ruteo importado por `main.py`.
        # Para el propósito de este `add.py`, la quito de aquí a menos que tengas
        # una razón específica para que controle el botón de retroceso global.
        pass

    # Este `page.on_view_pop` no debe ir aquí si `main.py` ya lo maneja.
    # Si lo pones aquí, sobrescribirás la configuración de `main.py`.
    # Asumo que la lógica de `page.on_view_pop` (con el diálogo de salida)
    # se gestiona en `main.py` o un módulo de ruteo global.
    # page.on_view_pop = lambda e: BACK(e)
    # page.window.prevent_close = True

    # El resto de tu lógica para agregar salones
    def new_dialog(e):
        from grid import load_grid # Importación local para evitar dependencia circular
        page.client_storage.set(f"Aula {classroom_number_field.value}", 0)
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
            ft.TextButton("Guardar", on_click=new_dialog),
            ft.TextButton("Cerrar", on_click=lambda e: page.close(add_dialog)), # Usa lambda para cerrar
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.open(add_dialog)
    page.update()