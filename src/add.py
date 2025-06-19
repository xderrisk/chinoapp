import flet as ft
import urllib.request
import urllib.parse # Necesario para codificar datos en POST/PUT
import json
import threading # Para evitar que la UI se congele mientras se hace la petición de red
import asyncio # Necesario para page.loop.call_soon_threadsafe

# --- Configuración de la API ---
# ASEGÚRATE de que esta URL coincida con la dirección donde tu API de Flask está corriendo.
API_BASE_URL = "http://192.168.1.115:5000/aulas"

def add_classroom(page: ft.Page):

    # Función auxiliar para manejar el éxito y la actualización de la UI
    def on_aula_add_success(page: ft.Page, dialog_to_close: ft.AlertDialog, aula_id: int):
        from grid import load_grid # Importación local para evitar dependencia circular al inicio
        page.close(dialog_to_close)
        page.snack_bar.content = ft.Text(f"Aula {aula_id} añadida exitosamente.")
        page.snack_bar.bgcolor = ft.Colors.GREEN_700
        page.snack_bar.open = True
        page.update()
        load_grid(page) # Recargar la cuadrícula después de añadir

    def send_aula_to_api(aula_data_to_send: dict, dialog_to_close: ft.AlertDialog):
        """
        Envía los datos de la nueva aula a la API usando un hilo separado.
        """
        try:
            request_data = json.dumps(aula_data_to_send).encode('utf-8')
            headers = {'Content-Type': 'application/json'}

            req = urllib.request.Request(API_BASE_URL, data=request_data, headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                status_code = response.getcode()
                response_body = response.read().decode('utf-8')

                if status_code == 201: # 201 Created es el esperado para un POST exitoso
                    # Encola la función de éxito en el hilo principal de Flet
                    page.loop.call_soon_threadsafe(
                        on_aula_add_success, page, dialog_to_close, aula_data_to_send['id_aula']
                    )
                else:
                    print(f"Error API (POST): Código de estado {status_code}, Respuesta: {response_body}")
                    page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error al añadir aula: {status_code} - {response_body}")

        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8')
            print(f"Error HTTP (POST): {e.code} - {e.reason}, Body: {error_body}")
            page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error HTTP: {e.code} - {e.reason}. La IP o ID del aula podría ya existir.")
        except urllib.error.URLError as e:
            print(f"Error de red o URL (POST): {e.reason}")
            page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error de red: {e.reason}. Asegúrate de que la API de Flask esté corriendo en {API_BASE_URL}.")
        except json.JSONDecodeError:
            print("Error al decodificar la respuesta JSON de la API.")
            page.loop.call_soon_threadsafe(show_error_snackbar, page, "Error al decodificar respuesta de la API al añadir aula.")
        except Exception as e:
            print(f"Error inesperado al conectar con la API (POST): {e}")
            page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error inesperado al añadir aula: {e}")

    def new_dialog(e):
        aula_numero_str = classroom_number_field.value.strip()
        aula_ip_suffix = classroom_ip_field.value.strip()

        if not aula_numero_str or not aula_ip_suffix:
            page.open(
                ft.SnackBar(ft.Text("Por favor, complete ambos campos."), open=True)
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
            classroom_number_field.focus()
            return

        if not aula_ip_suffix.isdigit() or not (0 <= int(aula_ip_suffix) <= 255):
            page.open(
                ft.SnackBar(
                    ft.Text("Error: El último octeto de la IP debe ser un número entre 0 y 255.", color=ft.Colors.WHITE),
                    bgcolor=ft.Colors.RED_700,
                    open=True
                )
            )
            page.update()
            classroom_ip_field.focus()
            return

        aula_id = int(aula_numero_str)
        aula_ip = f"192.168.0.{aula_ip_suffix}"
        
        initial_state = 0

        aula_data = {
            "id_aula": aula_id,
            "ip_aula": aula_ip,
            "estado": initial_state
        }
        
        # Inicia el envío a la API en un hilo separado
        threading.Thread(target=send_aula_to_api, args=(aula_data, add_dialog)).start()


    def show_error_snackbar(page: ft.Page, message: str):
        """Muestra un SnackBar con un mensaje de error. Se ejecuta en el hilo principal."""
        page.snack_bar = ft.SnackBar(ft.Text(message), open=True, bgcolor=ft.Colors.RED_700)
        page.update()

    classroom_number_field = ft.TextField(
        label="N° de salon",
        value="",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=lambda e: classroom_ip_field.focus()
    )

    classroom_ip_field = ft.TextField(
        label="Último octeto de IP",
        prefix_text="192.168.0.",
        value="",
        keyboard_type=ft.KeyboardType.NUMBER,
        on_submit=new_dialog
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