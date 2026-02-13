from playwright.sync_api import sync_playwright
from utils.config import Config
from pages.login_page import LoginPage
from pages.siniestro_page import SiniestroPage

def probar_flujo():
    print("\n--- INICIANDO PRUEBA DE MIGRACIÓN (PLAYWRIGHT) ---")
    
    with sync_playwright() as p:
        # 1. Levantar el navegador visible
        browser = p.chromium.launch(headless=Config.HEADLESS, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        try:
            # 2. Instanciar las páginas
            login_page = LoginPage(page)
            siniestro_page = SiniestroPage(page)
            
            # 3. Ejecutar Inicio de Sesión
            login_page.iniciar_sesion()
            
            # 4. Ejecutar Flujo de Siniestro
            # Llamamos al método envolvente que creamos para ejecutar todos los pasos
            siniestro_page.completar_flujo_siniestro()
            
            print("\n✅ ¡Prueba completada con éxito!")
            print("Abriendo el Inspector de Playwright. Cierra el inspector para terminar el script...")
            
            # 🔥 MAGIA DE PLAYWRIGHT: Esto pausará el script y abrirá un inspector
            # Te permite explorar la página, ver selectores y continuar paso a paso.
            page.pause()
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            page.screenshot(path="error_prueba.png")
            print("Captura de pantalla del error guardada como 'error_prueba.png'.")
        finally:
            browser.close()

if __name__ == "__main__":
    probar_flujo()