import time
from selenium.webdriver.common.by import By

# --- SELECTORES ESPECÍFICOS DE ESTA ESTRATEGIA ---
SELECTOR_INPUT_SUCURSAL = (By.CSS_SELECTOR, "input[formcontrolname='p_sucursal']")
SELECTOR_INPUT_POLIZA = (By.CSS_SELECTOR, "input[formcontrolname='p_poliza_central']")
SELECTOR_INPUT_INCISO = (By.CSS_SELECTOR, "input[formcontrolname='p_inciso']")
SELECTOR_BTN_BUSCAR = (By.XPATH, "//button[contains(., 'Buscar')]")

# --- SELECTORES COMUNES (TABLA DE RESULTADOS) ---
SELECTOR_CHECKBOX_LABEL = (By.XPATH, "(//td[contains(@class, 'mat-column-checkbox')]//label)[1]")
SELECTOR_BTN_SELECCIONAR = (By.XPATH, "//button[contains(., 'Seleccionar')]")
SELECTOR_BTN_ACEPTAR = (By.XPATH, "//button[contains(., 'Aceptar')]")
SELECTOR_BTN_SWAL_ACEPTAR = (By.XPATH, "//button[contains(@class, 'swal2') and contains(., 'Aceptar')]")

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
        
        # 3. Llamar al método interno para seleccionar en la tabla
        self.procesar_seleccion_en_tabla()

    def procesar_seleccion_en_tabla(self):
        """
        Lógica reutilizable para seleccionar el resultado y manejar popups.
        """
        print("Esperando resultados y seleccionando registro...")
        
        # 1. Espera de seguridad para que la tabla cargue
        time.sleep(3) 
        
        # Seleccionamos el primer resultado
        self.bot._click_js(SELECTOR_CHECKBOX_LABEL)
        time.sleep(1)
        
        print("Clic en botón Seleccionar...")
        self.bot._click_js(SELECTOR_BTN_SELECCIONAR)
        
        # 2. Espera para animaciones
        time.sleep(2)
        
        # 3. Doble confirmación segura (si el botón sigue ahí, le damos click)
        try:
            self.bot._click_js(SELECTOR_BTN_SELECCIONAR)
        except:
            pass # Si ya desapareció, continuamos sin error
        
        time.sleep(2)
        
        print("Aceptando confirmaciones...")
        self.bot._click_js(SELECTOR_BTN_ACEPTAR)
        
        # 4. Espera larga para la alerta final
        time.sleep(5)
        self.bot._click_js(SELECTOR_BTN_SWAL_ACEPTAR)