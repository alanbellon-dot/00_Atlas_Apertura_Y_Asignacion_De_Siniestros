import time
from selenium.webdriver.common.by import By

# --- SELECTORES ESPECÍFICOS DE ESTA ESTRATEGIA ---
SELECTOR_INPUT_PLACAS = (By.CSS_SELECTOR, "input[formcontrolname='p_placas']")
SELECTOR_BTN_BUSCAR = (By.XPATH, "//button[contains(., 'Buscar')]")

# --- SELECTORES COMUNES (TABLA DE RESULTADOS) ---
# Se definen aquí para que la clase los pueda usar
SELECTOR_CHECKBOX_LABEL = (By.XPATH, "(//td[contains(@class, 'mat-column-checkbox')]//label)[1]")
SELECTOR_BTN_SELECCIONAR = (By.XPATH, "//button[contains(., 'Seleccionar')]")
SELECTOR_BTN_ACEPTAR = (By.XPATH, "//button[contains(., 'Aceptar')]")
SELECTOR_BTN_SWAL_ACEPTAR = (By.XPATH, "//button[contains(@class, 'swal2') and contains(., 'Aceptar')]")

class BusquedaPlacas:
    def __init__(self, bot_instance):
        """
        :param bot_instance: Instancia del bot principal (Atlas) para acceder a sus métodos.
        """
        self.bot = bot_instance

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Póliza...")

        # 1. Llenar campos específicos
        print("Escribiendo número de placas...")
        self.bot._escribir_js(SELECTOR_INPUT_PLACAS, "MSN6456")

        # 2. Buscar
        print("Clic en botón Buscar...")
        self.bot._click_js(SELECTOR_BTN_BUSCAR)

        # 3 Llamar al método interno para seleccionar en la tabla
        self.procesar_seleccion_en_tabla()

    def procesar_seleccion_en_tabla(self):
        """
        Lógica reutilizable para seleccionar el resultado y manejar popups.
        """
        print("Clic en botón Buscar...")
        self.bot._click_js(SELECTOR_BTN_BUSCAR)
        print("Seleccionando registro en la tabla...")
        # Nota: Usamos self.bot._click_js porque la función _click_js vive en el bot principal
        self.bot._click_js(SELECTOR_CHECKBOX_LABEL)
        time.sleep(1)
        
        print("Clic en botón Seleccionar...")
        self.bot._click_js(SELECTOR_BTN_SELECCIONAR)
        time.sleep(4)
        
        # Doble confirmación habitual
        self.bot._click_js(SELECTOR_BTN_SELECCIONAR)
        time.sleep(2)
        
        print("Aceptando confirmaciones...")
        self.bot._click_js(SELECTOR_BTN_ACEPTAR)
        time.sleep(10)
        self.bot._click_js(SELECTOR_BTN_SWAL_ACEPTAR)