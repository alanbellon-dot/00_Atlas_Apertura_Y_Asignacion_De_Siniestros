from selenium.webdriver.common.by import By

# --- SELECTORES ESPECÍFICOS DE ESTA ESTRATEGIA ---
SELECTOR_INPUT_PLACAS = (By.CSS_SELECTOR, "input[formcontrolname='p_placas']")
SELECTOR_BTN_BUSCAR = (By.XPATH, "//button[contains(., 'Buscar')]")


class BusquedaPlacas:
    def __init__(self, bot_instance):
        """
        :param bot_instance: Instancia del bot principal (Atlas) para acceder a sus métodos.
        """
        self.bot = bot_instance

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Placas...")

        # 1. Llenar campos específicos
        print("Escribiendo número de placas...")
        self.bot._escribir_js(SELECTOR_INPUT_PLACAS, "MSN6456")

        # 2. Buscar (ESTE ES EL ÚNICO CLIC NECESARIO)
        print("Clic en botón Buscar...")
        self.bot._click_js(SELECTOR_BTN_BUSCAR)

