from playwright.sync_api import sync_playwright
from utils.config import Config
from pages.login_page import LoginPage
from pages.siniestro_page import SiniestroPage
from pages.tabla_resultados_page import TablaResultadosPage
from busquedas.busqueda_placas import BusquedaPlacas
# from busquedas.busqueda_serie import BusquedaSerie # Importarás las demás aquí

def main():
    print("\n--- INICIANDO AUTOMATIZACIÓN (PLAYWRIGHT) ---")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=Config.HEADLESS, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        try:
            # 1. Instanciar los Page Objects
            login_page = LoginPage(page)
            siniestro_page = SiniestroPage(page)
            tabla_page = TablaResultadosPage(page)
            # asignacion_page = AsignacionPage(page) <-- (Falta este último paso)
            
            # 2. Iniciar Sesión
            login_page.iniciar_sesion()
            
            # 3. Llenar los datos del Siniestro
            siniestro_page.completar_flujo_siniestro()
            
            # 4. Estrategia de búsqueda
            # Aquí puedes poner la lógica de input() para preguntar qué buscar, igual que en tu Selenium
            estrategia = BusquedaPlacas(page)
            estrategia.ejecutar()
            
            # 5. Manejar la selección y popups
            tabla_page.procesar_seleccion()
            
            print("\n>> E2E: Búsqueda y Selección finalizada con éxito.")
            page.pause() # Pausamos para que veas el resultado
            
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            page.screenshot(path="error_log.png")
        finally:
            browser.close()

if __name__ == "__main__":
    main()