from selenium.webdriver.common.by import By

# --- SELECTORES ESPECÍFICOS DE ESTA ESTRATEGIA ---
SELECTOR_INPUT_CANAL = (By.CSS_SELECTOR, "input[formcontrolname='p_canal']")
SELECTOR_INPUT_RAMO = (By.CSS_SELECTOR, "input[formcontrolname='p_ramo']")
SELECTOR_INPUT_POLIZA_SANTANDER = (By.CSS_SELECTOR, "input[formcontrolname='p_poliza']")
SELECTOR_INPUT_ANO_EMISION = (By.CSS_SELECTOR, "input[formcontrolname='p_ano_emision']")
SELECTOR_BTN_BUSCAR = (By.XPATH, "//button[contains(., 'Buscar')]")



class BusquedaSantander:
    def __init__(self, bot_instance):
        """
        :param bot_instance: Instancia del bot principal (Atlas) para acceder a sus métodos.
        """
        self.bot = bot_instance

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Póliza (Santander)...")

        # 1. Llenar campos específicos
        print("Escribiendo canal")
        self.bot._escribir_js(SELECTOR_INPUT_CANAL, "6")
        print("Escribiendo ramo")
        self.bot._escribir_js(SELECTOR_INPUT_RAMO, "91")
        print("Escribiendo póliza Santander")
        self.bot._escribir_js(SELECTOR_INPUT_POLIZA_SANTANDER, "069109028355501")
        print("Escribiendo año de emisión")
        self.bot._escribir_js(SELECTOR_INPUT_ANO_EMISION, "1")
        
        # 2. Buscar (ESTE ES EL ÚNICO CLIC NECESARIO)
        print("Clic en botón Buscar...")
        self.bot._click_js(SELECTOR_BTN_BUSCAR)

