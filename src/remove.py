import flet as ft
import urllib.request
import urllib.parse # Aunque no se usa directamente para DELETE sin cuerpo, es bueno tenerlo
import json
import threading # Para evitar que la UI se congele mientras se hace la petición de red
import asyncio # Necesario para page.loop.call_soon_threadsafe

# --- Configuración de la API ---
# ASEGÚRATE de que esta URL coincida con la dirección donde tu API de Flask está corriendo.
API_BASE_URL = "http://192.168.1.115:5000/aulas"

def remove_classroom(page: ft.Page):

    # Función auxiliar para manejar el éxito y la actualización de la UI
    def on_aula_delete_success(page: ft.Page, dialog_to_close: ft.AlertDialog, aula_id: int):
        from grid import load_grid # Importación local para evitar dependencia circular al inicio
        page.close(dialog_to_close)
        page.snack_bar.content = ft.Text(f"Aula {aula_id} eliminada con éxito.")
        page.snack_bar.bgcolor = ft.Colors.GREEN_700
        page.snack_bar.open = True
        page.update()
        load_grid(page) # Recargar la cuadrícula después de eliminar

    # Función auxiliar para manejar errores de la API en la UI
    def show_error_snackbar(page: ft.Page, message: str):
        page.snack_bar = ft.SnackBar(ft.Text(message), open=True, bgcolor=ft.Colors.RED_700)
        page.update()

    def send_delete_to_api(aula_id_to_delete: int, dialog_to_close: ft.AlertDialog):
        """
        Envía una solicitud DELETE a la API para eliminar un aula por su ID.
        Esta función se ejecuta en un hilo separado.
        """
        delete_url = f"{API_BASE_URL}/{aula_id_to_delete}"
        try:
            req = urllib.request.Request(delete_url, method='DELETE')
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()
                response_body = response.read().decode('utf-8')

                if status_code == 200: # 200 OK es el esperado para un DELETE exitoso
                    # Encola la función de éxito en el hilo principal de Flet
                    page.loop.call_soon_threadsafe(
                        on_aula_delete_success, page, dialog_to_close, aula_id_to_delete
                    )
                elif status_code == 404:
                    print(f"Error API (DELETE): Código de estado {status_code}, Respuesta: {response_body}")
                    page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Aula {aula_id_to_delete} no encontrada.")
                else:
                    print(f"Error API (DELETE): Código de estado {status_code}, Respuesta: {response_body}")
                    page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error al eliminar aula: {status_code} - {response_body}")

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"Error HTTP (DELETE): {e.code} - {e.reason}, Body: {error_body}")
            if e.code == 404:
                page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Aula {aula_id_to_delete} no encontrada. Código de estado {e.code}.")
            else:
                page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error HTTP al eliminar: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            print(f"Error de red o URL (DELETE): {e.reason}")
            page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error de red: {e.reason}. Asegúrate de que la API de Flask esté corriendo en {API_BASE_URL}.")
        except Exception as e:
            print(f"Error inesperado al conectar con la API (DELETE): {e}")
            page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error inesperado al eliminar aula: {e}")

    def delete_dialog(e):
        aula_numero_str = delete_classroom_number_field.value.strip()

        if not aula_numero_str:
            page.open(
                ft.SnackBar(ft.Text("Por favor, ingrese el número del salón a eliminar."), open=True)
            )
            page.update()
            return
        
        if not aula_numero_str.isdigit():
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
        
        aula_id_to_delete = int(aula_numero_str)
        
        # Inicia el proceso de eliminación en un hilo separado
        threading.Thread(target=send_delete_to_api, args=(aula_id_to_delete, remove_dialog)).start()

    delete_classroom_number_field = ft.TextField(
        label="N° de aula a eliminar",
        value="",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=delete_dialog
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