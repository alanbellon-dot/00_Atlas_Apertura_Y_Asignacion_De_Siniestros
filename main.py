import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains # Igual que arriba

# ==========================================
# 1. CONFIGURACIÓN Y CONSTANTES
# ==========================================

# --- Datos de acceso ---
BASE_URL = "https://prometeo-qa-demo.web.app/login"
USERNAME = "anaPrueba"
PASSWORD = "Anaprueba26"

# --- SELECTORES ---
# HE AQUÍ EL CAMBIO PRINCIPAL:
# Usamos CSS Selector apuntando al 'formcontrolname' de Angular.
INPUT_USER = (By.CSS_SELECTOR, "input[formcontrolname='username']")

# Nota: Asumo que el password tendrá un formcontrolname similar. 
# Si falla, necesitaré el HTML del input de password.
INPUT_PASS = (By.CSS_SELECTOR, "input[formcontrolname='password']") 

# Selector genérico para el botón (ajustar si es necesario)
BTN_LOGIN  = (By.XPATH, "//button[contains(., 'Ingresar')]")


# --- SELECTORES: DATOS DEL REPORTANTE ---
INPUT_NOMBRE = (By.CSS_SELECTOR, "input[formcontrolname='nombre']")
INPUT_PATERNO = (By.CSS_SELECTOR, "input[formcontrolname='apellido_paterno']")
INPUT_MATERNO = (By.CSS_SELECTOR, "input[formcontrolname='apellido_materno']")
BTN_DESPLEGABLE = (By.CSS_SELECTOR, ".mat-mdc-select-value")
OPCION_CELULAR = (By.XPATH, "//span[contains(text(), 'Celular')]")
INPUTS_TELEFONO = (By.CSS_SELECTOR, "input[formcontrolname='telefono']")
OPCION_CELULAR_CONFIRM = (By.XPATH, "(//span[contains(text(), 'Celular')])[2]") 
BTN_DESPLEGABLE_CONFIRM = (By.XPATH, "(//div[contains(@class, 'mat-mdc-select-value')])[2]")
INPUT_CONFIRM_TEL = (By.XPATH, "(//input[@formcontrolname='telefono'])[2]")
BTN_CAUSA = (By.XPATH, "//span[contains(text(), 'Causa')]")
OPCION_COLISION = (By.XPATH, "//span[contains(text(), 'COLISION')]")

# --- SELECTORES: DATOS DEL CONDUCTOR ---
CHECKBOX_CONDUCTOR = (By.ID, "mat-mdc-checkbox-2-input")
CHECKBOX_1 = (By.ID, "mat-mdc-checkbox-1-input")

# -- SELECTORES: UBICACIÓN DEL SINIESTRO ---
BTN_LUPA = (By.CSS_SELECTOR, "button[aria-label='Btn búsqueda']")
INPUT_MAPA = (By.CSS_SELECTOR, "input.pac-target-input")
BTN_CREAR_FOLIO = (By.XPATH, "//button[contains(text(), 'Crear folio')]")


# --- SELECTORES: DATOS DEL SINIESTRO ---
BTN_CALENDARIO = (By.CSS_SELECTOR, "mat-datepicker-toggle button")
BTN_DIA_HOY = (By.CSS_SELECTOR, "button[aria-current='date']")
BTN_RELOJ = (By.XPATH, "//mat-icon[contains(text(), 'schedule')]/ancestor::button")
TEXTAREA_HECHOS = (By.CSS_SELECTOR, "textarea[formcontrolname='que_ocurrio']")

# ==========================================
# 2. CLASE PRINCIPAL DEL BOT
# ==========================================

class Atlas:
    def __init__(self, headless=False):
        """
        Se ejecuta al crear el bot.
        Acepta 'headless' para decidir si mostrar o no el navegador.
        """
        print("Inicializando configuración del Bot...")
        
        # 1. LIMPIEZA DE ZOMBIES
        try:
            os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
            time.sleep(1) 
        except:
            pass

        # 2. CONFIGURACIÓN DE CHROME
        chrome_options = Options()
        
        # Modo Headless (sin interfaz gráfica) si se solicita
        if headless:
            chrome_options.add_argument("--headless=new")

        # Desactivar guardar contraseñas y popups molestos
        prefs = {
            "credentials_enable_service": False, 
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        chrome_options.add_experimental_option("prefs", prefs)

        # Configuración anti-detección y estabilidad
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--remote-allow-origins=*")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")

        # 3. INICIAR EL DRIVER
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        print("Bot iniciado correctamente.")

    # ==========================================
    # 3. MÉTODOS AUXILIARES (WRAPPERS)
    # ==========================================
    
    def _click(self, locator):
        """Espera a que un elemento sea clickeable y hace click."""
        try:
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except Exception as e:
            print(f"Error al intentar click en {locator}: {e}")
            raise
    def _click_js(self, locator):
        """Fuerza un click usando JavaScript (útil para checkboxes rebeldes)."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def _escribir(self, locator, texto):
        """Espera a que sea visible, limpia el campo y escribe."""
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.click() # A veces Angular necesita un click previo para 'despertar' el input
            element.clear()
            element.send_keys(texto)
        except Exception as e:
            print(f"Error al escribir en {locator}: {e}")
            raise

    def _esperar_elemento(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    # ==========================================
    # 4. LÓGICA DE NEGOCIO
    # ==========================================

    def iniciar_sesion(self):
        print(f"Navegando a {BASE_URL}...")
        self.driver.get(BASE_URL)
        
        print("Intentando ingresar credenciales...")
        # Aquí usa las constantes definidas arriba
        self._escribir(INPUT_USER, USERNAME)
        self._escribir(INPUT_PASS, PASSWORD)
        self._click(BTN_LOGIN)
        
        print("Credenciales enviadas.")

    def datos_del_reportante(self):
        print("Intentando de encontrar los campos de datos del reportante...")
        self._escribir(INPUT_NOMBRE, "AN")
        self._escribir(INPUT_PATERNO, "Apellido Paterno")
        self._escribir(INPUT_MATERNO, "Apellido Materno")

        # Primer Teléfono
        print("Llenando primer teléfono...")
        self._click(BTN_DESPLEGABLE)    # Abre el menú 1
        self._click(OPCION_CELULAR)     # Elige Celular
        self._escribir(INPUTS_TELEFONO, "5555555555")
        

        # Segundo Teléfono
        print("Llenando segundo teléfono...")
        self._click(BTN_DESPLEGABLE_CONFIRM)  # Abre el menú 2
        self._click(OPCION_CELULAR_CONFIRM)           # Elige Celular
        self._escribir(INPUT_CONFIRM_TEL, "5555555555")

        print("Seleccionando causa...")
        self._click(BTN_CAUSA)
        self._click(OPCION_COLISION)

    def datos_del_conductor(self):
        print("Llenando datos del conductor...")
        self._click_js(CHECKBOX_CONDUCTOR) 
        self._click_js(CHECKBOX_1)


    # ==========================================
    # 4. LÓGICA DE NEGOCIO
    # ==========================================

    def ubicacion_del_siniestro(self):
        """
        Despliega el buscador del mapa y escribe la dirección.
        """
        print("Iniciando ubicación del siniestro...")
        try:
            print("Desplegando buscador de mapa...")
            self._click_js(BTN_LUPA)
            
            time.sleep(1) 
            
            direccion = "Metrobús Nápoles, Avenida Insurgentes Sur, Colonia Nápoles, Mexico City, CDMX, Mexico"
            self._escribir(INPUT_MAPA, direccion)
            
            # 4. Opcional: Presionar ENTER para que el mapa busque
            self._esperar_elemento(INPUT_MAPA).send_keys(Keys.ENTER)
            
            print(f">> Dirección '{direccion}' ingresada con éxito.")
            time.sleep(2)

        except Exception as e:
            print(f"Error en ubicacion_del_siniestro: {e}")
            raise

    def finalizar_registro(self):
        print("Finalizando registro...")
        try:
            # 1. Localizar elemento
            elemento = self._esperar_elemento(BTN_CREAR_FOLIO)
            
            # 2. Scroll hacia el elemento para que esté visible
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
            time.sleep(1)
            
            # 3. Clic vía JavaScript
            self.driver.execute_script("arguments[0].click();", elemento)
            
            print(">> Clic exitoso en Crear Folio.")
        
        except Exception as e:
            print(f"Error: {e}")
            raise

    
    def datos_del_siniestro(self):
        print("Llenando datos del siniestro...")
        print("Dando clic en el calendario...")
        self._click_js(BTN_CALENDARIO)
        time.sleep(1)
        self._click_js(BTN_DIA_HOY)
        self._click_js(BTN_RELOJ)
        print("Escribiendo hechos...")
        campo = self._esperar_elemento(TEXTAREA_HECHOS)
        
        # Scroll y Click forzado en una sola línea de JS
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", campo)
        time.sleep(0.5) # Pausa breve para estabilidad
        
        campo.send_keys("El conductor perdió el control del vehículo y chocó contra un poste.")
        print(">> Hechos listos.")



    def cerrar(self):
        print("Cerrando navegador...")
        try:
            self.driver.quit()
        except Exception:
            pass

# ==========================================
# 5. EJECUCIÓN
# ==========================================

if __name__ == "__main__":
    # Ahora sí coincide el argumento con el __init__
    bot = Atlas(headless=False)
    
    try:
        bot.iniciar_sesion()
        bot.datos_del_reportante()
        bot.datos_del_conductor()
        bot.ubicacion_del_siniestro()
        bot.finalizar_registro()
        bot.datos_del_siniestro()
        
        print(">> Automatización finalizada con éxito.")
        time.sleep(5) 
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        # bot.driver.save_screenshot("error_log.png")
        
    finally:
        bot.cerrar()