from selenium.webdriver.common.by import By

# --- SELECTORES ESPECÍFICOS DE ESTA ESTRATEGIA ---
SELECTOR_INPUT_SUCURSAL = (By.CSS_SELECTOR, "input[formcontrolname='p_sucursal']")
SELECTOR_INPUT_POLIZA_CENTRAL = (By.CSS_SELECTOR, "input[formcontrolname='p_poliza_central']")
SELECTOR_BTN_BUSCAR = (By.XPATH, "//button[contains(., 'Buscar')]")



class BusquedaInciso:
    def __init__(self, bot_instance):
        """
        :param bot_instance: Instancia del bot principal (Atlas) para acceder a sus métodos.
        """
        self.bot = bot_instance

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Inciso...")

        # 1. Llenar campos específicos
        print("Escribiendo sucursal")
        self.bot._escribir_js(SELECTOR_INPUT_SUCURSAL, "H00")
        print("Escribiendo póliza central")
        self.bot._escribir_js(SELECTOR_INPUT_POLIZA_CENTRAL, "65063")
        
        # 2. Buscar (ESTE ES EL ÚNICO CLIC NECESARIO)
        print("Clic en botón Buscar...")
        self.bot._click_js(SELECTOR_BTN_BUSCAR)

