from selenium.webdriver.common.by import By

# --- SELECTORES ESPECÍFICOS DE ESTA ESTRATEGIA ---
SELECTOR_INPUT_SUCURSAL = (By.CSS_SELECTOR, "input[formcontrolname='p_sucursal']")
SELECTOR_INPUT_POLIZA = (By.CSS_SELECTOR, "input[formcontrolname='p_poliza_central']")
SELECTOR_INPUT_INCISO = (By.CSS_SELECTOR, "input[formcontrolname='p_inciso']")
SELECTOR_BTN_BUSCAR = (By.XPATH, "//button[contains(., 'Buscar')]")


class BusquedaPoliza:
    def __init__(self, bot_instance):
        """
        :param bot_instance: Instancia del bot principal (Atlas) para acceder a sus métodos.
        """
        self.bot = bot_instance

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Póliza (Tradicional)...")

        # 1. Llenar campos específicos
        print("Escribiendo sucursal, póliza e inciso...")
        self.bot._escribir_js(SELECTOR_INPUT_SUCURSAL, "MS1")
        self.bot._escribir_js(SELECTOR_INPUT_POLIZA, "57089")
        self.bot._escribir_js(SELECTOR_INPUT_INCISO, "1")

        # 2. Buscar
        print("Clic en botón Buscar...")
        self.bot._click_js(SELECTOR_BTN_BUSCAR)
        

    