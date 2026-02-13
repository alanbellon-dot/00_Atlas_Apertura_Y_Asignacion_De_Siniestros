from playwright.sync_api import sync_playwright
from pages.login_page import LoginPage
from busquedas.busqueda_placas import BusquedaPlacas
from utils.config import Config

def main():
    print("\n--- INICIANDO AUTOMATIZACIÓN (PLAYWRIGHT) ---")
    
    # 1. Iniciar Playwright
    with sync_playwright() as p:
        # Configurar el navegador
        browser = p.chromium.launch(headless=Config.HEADLESS, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True) # Para mantener el maximizado real
        page = context.new_page()

        try:
            # 2. Instanciar los Page Objects
            login_page = LoginPage(page)
            # siniestro_page = SiniestroPage(page)   <-- Migrarás esta página luego
            # asignacion_page = AsignacionPage(page) <-- Migrarás esta página luego
            
            # 3. Flujo de Ejecución
            login_page.iniciar_sesion()
            
            # -- Aquí irán los demás pasos abstraídos --
            # siniestro_page.llenar_datos_reportante("Juan", "Galindo")
            # siniestro_page.llenar_ubicacion("Metrobús Nápoles...")
            
            # 4. Uso del patrón estrategia pasándole la página
            estrategia_busqueda = BusquedaPlacas(page)
            estrategia_busqueda.ejecutar()
            
            # asignacion_page.procesar_seleccion()
            
            print(">> Automatización finalizada con éxito.")
            # time.sleep(5)  # En Playwright es page.wait_for_timeout(5000) si realmente quieres pausar al final
            
        except Exception as e:
            print(f"CRITICAL ERROR: {e}")
            page.screenshot(path="error_log.png") # Captura de error nativa muy útil
        finally:
            browser.close()

if __name__ == "__main__":
    main()