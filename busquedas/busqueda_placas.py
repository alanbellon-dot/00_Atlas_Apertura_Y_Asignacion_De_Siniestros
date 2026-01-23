import time
from selenium.webdriver.common.by import By

# --- SELECTORES ESPECÍFICOS DE ESTA ESTRATEGIA ---
SELECTOR_INPUT_PLACAS = (By.CSS_SELECTOR, "input[formcontrolname='p_placas']")
SELECTOR_BTN_BUSCAR = (By.XPATH, "//button[contains(., 'Buscar')]")

# --- SELECTORES COMUNES (TABLA DE RESULTADOS) ---
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
        print(">> [Estrategia] Iniciando búsqueda por Placas...")

        # 1. Llenar campos específicos
        print("Escribiendo número de placas...")
        self.bot._escribir_js(SELECTOR_INPUT_PLACAS, "MSN6456")

        # 2. Buscar (ESTE ES EL ÚNICO CLIC NECESARIO)
        print("Clic en botón Buscar...")
        self.bot._click_js(SELECTOR_BTN_BUSCAR)

        # 3. Llamar al método interno para seleccionar en la tabla
        self.procesar_seleccion_en_tabla()

    def procesar_seleccion_en_tabla(self):
        """
        Lógica reutilizable para seleccionar el resultado y manejar popups.
        """
        # --- CORRECCIÓN: ELIMINADO EL SEGUNDO CLIC A BUSCAR ---
        
        print("Esperando resultados y seleccionando registro...")
        
        # 1. Espera de seguridad para que la tabla cargue los datos
        time.sleep(3)
        
        # Seleccionamos el primer resultado
        self.bot._click_js(SELECTOR_CHECKBOX_LABEL)
        time.sleep(1)
        
        print("Clic en botón Seleccionar...")
        self.bot._click_js(SELECTOR_BTN_SELECCIONAR)
        
        # 2. Espera para animaciones
        time.sleep(2)
        
        # 3. Doble confirmación segura
        try:
            self.bot._click_js(SELECTOR_BTN_SELECCIONAR)
        except:
            pass # Si no es necesario el segundo clic, continuamos
        
        time.sleep(2)
        
        print("Aceptando confirmaciones...")
        self.bot._click_js(SELECTOR_BTN_ACEPTAR)
        
        # 4. Espera larga para la alerta final (SweetAlert)
        time.sleep(5)
        self.bot._click_js(SELECTOR_BTN_SWAL_ACEPTAR)