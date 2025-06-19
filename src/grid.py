import flet as ft
import urllib.request
import json
import threading
import asyncio

# aqui voy a meter un local storage
API_BASE_URL = "http://192.168.1.115:5000/aulas"

# --- Funciones de Ayuda para las Solicitudes HTTP (integradas para Flet) ---

def fetch_aulas_from_api(page: ft.Page):
    """
    Realiza una solicitud GET a la API para obtener todas las aulas.
    Esta función se ejecuta en un hilo separado.
    """
    try:
        req = urllib.request.Request(API_BASE_URL, method='GET')
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_body = response.read().decode('utf-8')

            if status_code == 200:
                aulas_data = json.loads(response_body)
                # Encola la actualización de la UI en el hilo principal de Flet
                page.loop.call_soon_threadsafe(update_grid_with_api_data, page, aulas_data)
            else:
                print(f"Error al obtener aulas: Código de estado {status_code}, Respuesta: {response_body}")
                page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error API: {status_code} - {response_body}")

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"Error HTTP: {e.code} - {e.reason}, Body: {error_body}")
        page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error HTTP: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"Error de red o URL: {e.reason}")
        page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error de red: {e.reason}. Asegúrate de que la API de Flask esté corriendo en {API_BASE_URL}.")
    except json.JSONDecodeError:
        print("Error al decodificar la respuesta JSON de la API.")
        page.loop.call_soon_threadsafe(show_error_snackbar, page, "Error al decodificar respuesta de la API.")
    except Exception as e:
        print(f"Error inesperado al conectar con la API: {e}")
        page.loop.call_soon_threadsafe(show_error_snackbar, page, f"Error inesperado: {e}")

def update_grid_with_api_data(page: ft.Page, aulas_data):
    """
    Actualiza los controles de la cuadrícula de Flet con los datos obtenidos de la API.
    Esta función se ejecuta en el hilo principal de la UI.
    """
    classroom_containers = []

    for aula in aulas_data:
        aula_id = aula.get('id_aula')
        aula_ip = aula.get('ip_aula')
        estado = aula.get('estado')

        # Ajusta la lógica del estado. Si tu API devuelve "ocupado" o "disponible" como cadenas.
        colorStatus = ft.Colors.RED if estado == 1 else ft.Colors.GREEN

        content_controls = [
            ft.Text(str(aula_id), weight=ft.FontWeight.BOLD),
        ]
        # La propiedad show_ips_globally ya está siendo manejada en main.py
        if hasattr(page, 'show_ips_globally') and page.show_ips_globally:
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

    # Reemplaza el contenido de la página con la nueva cuadrícula de aulas
    # Asegúrate de que la página tenga un control donde se pueda agregar la cuadrícula,
    # por ejemplo, un ft.Column vacío al inicio en main.py si no lo hay.
    
    # Para asegurar que la cuadrícula se muestre correctamente, asumimos que
    # main.py tiene un contenedor principal (como un ft.Column) donde
    # se pueden añadir o reemplazar los controles.
    # El método más limpio es que `load_grid` retorne el control
    # o que `main` le pase un placeholder específico para actualizar.
    # Por ahora, simplemente reemplazamos el contenido de `page.controls[0]`
    # asumiendo que es el contenedor principal después del AppBar.

    # Es mejor que `load_grid` actualice el `page.controls` de una manera controlada
    # por ejemplo, si tienes un `ft.Column` en `main.py` con `expand=True`,
    # puedes acceder a sus `controls` directamente.
    
    # Si tu `main.py` solo tiene el AppBar y luego un Column vacío para el contenido,
    # el índice 1 (después del AppBar que es el 0) debería ser el Column.
    # Si no estás seguro, revisa la estructura de page.controls.
    
    # Una forma más robusta es que el `main.py` le pase a `load_grid`
    # la referencia al control específico que debe actualizar.
    
    # Sin embargo, basándonos en tu `main.py` actual, lo más probable es
    # que quieras que `load_grid` reemplace el contenido del `page`.
    # Vamos a asegurarnos de que solo el contenido dinámico sea afectado.

    # En lugar de `page.controls.clear()` y `page.add()`,
    # si el contenido de las aulas está en un `ft.Column` dentro de `main.py`,
    # deberías actualizar los `controls` de ese `ft.Column`.
    
    # Para este ejemplo, voy a asumir que `main.py` tiene un `ft.Column`
    # que será el **segundo** control en `page.controls` (después del AppBar).
    # Si tu `main.py` tiene una estructura diferente, ajusta esto.
    if len(page.controls) > 1 and isinstance(page.controls[1], ft.Column):
        page.controls[1].controls = [
            ft.Row(
                controls=classroom_containers,
                wrap=True,
                spacing=10,
                run_spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        ]
    else:
        # Fallback si la estructura no es la esperada, limpia y añade directamente a la página
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
    page.snack_bar = ft.SnackBar(ft.Text("Aulas cargadas desde la API!"), open=True)
    page.update()

def show_error_snackbar(page: ft.Page, message: str):
    """Muestra un SnackBar con un mensaje de error. Se ejecuta en el hilo principal."""
    page.snack_bar = ft.SnackBar(ft.Text(message), open=True, bgcolor=ft.Colors.RED_700)
    page.update()


# --- Función Principal de Carga de la Cuadrícula ---
# Esta es la única función que `main.py` llamará de este archivo.
def load_grid(page: ft.Page):
    # page.show_ips_globally se define en main.py, así que solo lo usamos aquí.
    # Ya no necesitamos inicializarlo, main.py se encarga de eso.

    # Limpia los controles actuales y muestra un mensaje de carga
    # Asume que el segundo control de la página es el contenedor principal para la cuadrícula
    if len(page.controls) > 1 and isinstance(page.controls[1], ft.Column):
        page.controls[1].controls = [ft.Text("Cargando aulas desde la API...", size=16)]
    else:
        # Fallback si la estructura no es la esperada
        page.controls.clear()
        page.add(ft.Text("Cargando aulas desde la API...", size=16))

    page.update()

    # Inicia la llamada a la API en un hilo separado
    threading.Thread(target=fetch_aulas_from_api, args=(page,)).start()

# No hay necesidad de `if __name__ == "__main__":` aquí,
# ya que `main.py` es el punto de entrada principal.