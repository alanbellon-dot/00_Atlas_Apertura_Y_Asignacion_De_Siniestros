from busquedas.busqueda_poliza import BusquedaPoliza
from busquedas.busqueda_serie import BusquedaSerie
from busquedas.busqueda_placas import BusquedaPlacas
from busquedas.busqueda_santader import BusquedaSantander
from busquedas.busqueda_inciso import BusquedaInciso
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys



# ==========================================
# 1. CONFIGURACIÓN Y CONSTANTES
# ==========================================

# --- Datos de acceso ---
BASE_URL = "https://prometeo-qa-demo.web.app/login"
USERNAME = "Testing"
PASSWORD = "123456*"

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
INPUT_PLACAS = (By.CSS_SELECTOR, 'input[formcontrolname="placas_cabina"]')
BTN_COLOR = (By.XPATH, "//span[contains(text(), 'Color')]")
OPCION_COLOR_AMARILLO = (By.XPATH, "//span[contains(text(), 'AMARILLO')]")

# ---SELECTORES: AJUSTE REMOTO ---
SELECTOR_RADIO_NO = (By.XPATH, "//input[@name='mat-radio-group-4' and @value='false']")
SELECTOR_RADIO_GROUP_5_NO = (By.XPATH, "//input[@name='mat-radio-group-5' and @value='false']")
SELECTOR_RADIO_GROUP_6_NO = (By.XPATH, "//input[@name='mat-radio-group-6' and @value='false']")
SELECTOR_RADIO_GROUP_7_NO = (By.XPATH, "//input[@name='mat-radio-group-7' and @value='false']")


# --- SELECTORES: BÚSQUEDA GENÉRICA ---
# Selector para abrir el dropdown que dice "Buscar por"
SELECTOR_DROPDOWN_CRITERIO = (By.XPATH, "//mat-label[contains(text(), 'Buscar por')]/ancestor::mat-form-field//mat-select")

# Opciones dentro del dropdown (Angular las renderiza fuera del DOM normal, en un cdk-overlay)
OPCION_DROPDOWN_POLIZA = (By.XPATH, "//mat-option//span[contains(text(), 'Póliza')]")
OPCION_DROPDOWN_SERIE = (By.XPATH, "//mat-option//span[contains(text(), 'Serie')]")
OPCION_DROPDOWN_PLACAS = (By.XPATH, "//mat-option//span[contains(text(), 'Placas')]")
OPCION_DROPDOWN_SANTANDER = (By.XPATH, "//mat-option//span[contains(text(), 'Santander')]")
OPCION_DROPDOWN_INCISO = (By.XPATH, "//mat-option//span[contains(text(), 'Inciso')]")


# --- SELECTORES: MENÚ SEGUIMIENTO AJUSTADORES ---
SELECTOR_MENU_SEGUIMIENTO = (By.XPATH, "//a[@title='Seguimiento ajustadores']")
SELECTOR_TAB_POR_ASIGNAR = (By.XPATH, "//span[contains(., 'Por Asignar')]")
SELECTOR_BTN_ASIGNAR_PRIMERA_FILA = (By.XPATH, "(//tbody//tr)[1]//button[contains(., 'Asignar')]")

# --- SELECTORES: SELECCIÓN DE AJUSTADOR ---
SELECTOR_BTN_ASIGNACION_MANUAL = (By.XPATH, "//button[contains(., 'Asignación manual')]")
# Alternativa: Busca SOLO dentro de la ventana modal/dialogo
SELECTOR_TXT_ASIGNAR = (By.XPATH, "//span[normalize-space()='Asignar']")
SELECTOR_BTN_ASIGNAR_FINAL = (By.XPATH, "//button[@status='success' and contains(., 'Asignar')]")



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

    def _click_scroll_js(self, locator):
        """Localiza, hace scroll hasta el elemento, espera un momento y da clic."""
        element = self._esperar_elemento(locator)
        # Scroll suave para poner el elemento en el centro
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1) # Pausa importante para que la animación del scroll termine
        self.driver.execute_script("arguments[0].click();", element)


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
    def _escribir_js(self, locator, texto):
        """Scroll, click forzado y escritura."""
        element = self._esperar_elemento(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", element)
        element.send_keys(texto)

    def _esperar_elemento(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def _esperar_desaparicion(self, locator):
        """Espera a que un elemento (como un loader) desaparezca."""
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
        except Exception as e:
            print(f"Advertencia: El elemento {locator} no desapareció o no existía: {e}")

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
        print("Esperando que desaparezca la pantalla de carga (contenedorBlock)...")
        self._esperar_desaparicion((By.CSS_SELECTOR, ".contenedorBlock"))
        print("Intentando de encontrar los campos de datos del reportante...")
        self._escribir(INPUT_NOMBRE, "Juan")
        self._escribir(INPUT_PATERNO, "Galindo")
        self._escribir(INPUT_MATERNO, "Peres")

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
        time.sleep(2)  # Esperar a que la sección esté lista
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

        self._escribir(INPUT_PLACAS, "TX11111")
        print("Seleccionando color del vehículo...")
        self._click_js(BTN_COLOR)                    
        self._click(OPCION_COLOR_AMARILLO)
        


    def ajuste_remoto(self):
        print("Seleccionando opción 'No' para ajuste remoto...")
        self._click_js(SELECTOR_RADIO_NO)
        self._click_js(SELECTOR_RADIO_GROUP_5_NO)
        self._click_js(SELECTOR_RADIO_GROUP_6_NO)
        self._click_js(SELECTOR_RADIO_GROUP_7_NO)

    def buscar_poliza_dinamica(self, criterio="PLACAS"):
        """
        Función orquestadora que decide qué estrategia usar.
        :param criterio: String ('POLIZA', 'SERIE', 'PLACAS')
        """
        print(f"--- Iniciando módulo de búsqueda por: {criterio} ---")

        # 1. SELECCIONAR EL CRITERIO EN EL DROPDOWN
        # Primero verificamos si necesitamos cambiar el dropdown
        try:
            print(f"Abriendo menú 'Buscar por'...")
            self._click_js(SELECTOR_DROPDOWN_CRITERIO)
            time.sleep(1) # Esperar animación del menú

            if criterio == "POLIZA":
                print("Eligiendo opción 'Póliza'...")
                self._click_js(OPCION_DROPDOWN_POLIZA)
            elif criterio == "SERIE":
                print("Eligiendo opción 'Serie'...")
                self._click_js(OPCION_DROPDOWN_SERIE)
            elif criterio == "PLACAS":
                print("Eligiendo opcin 'Placas'...")
                self._click_js(OPCION_DROPDOWN_PLACAS)
            elif criterio == "SANTANDER":
                print("Eligiendo opcin 'Santander'...")
                self._click_js(OPCION_DROPDOWN_SANTANDER)
            elif criterio == "INCISO":
                print("Eligiendo opcin 'Inciso'...")
                self._click_js(OPCION_DROPDOWN_INCISO)
            else:
                return
            
            # Pequeña pausa para que Angular renderice los inputs correspondientes
            time.sleep(1)
            
        except Exception as e:
            print(f"Error seleccionando el criterio en el dropdown: {e}")
            # Si falla, quizás ya estaba seleccionado por defecto, intentamos continuar...

        # 2. EJECUTAR LA ESTRATEGIA CORRESPONDIENTE
        if criterio == "POLIZA":
            # Instanciamos la clase y le pasamos 'self' (este bot Atlas)
            estrategia = BusquedaPoliza(self)
            estrategia.ejecutar()
            
        elif criterio == "SERIE":
            print("Buscando por SERIE...")
            estrategia = BusquedaSerie(self)
            estrategia.ejecutar()
        
        elif criterio == "PLACAS":
            estrategia = BusquedaPlacas(self)
            estrategia.ejecutar()

        elif criterio == "SANTANDER":
            estrategia = BusquedaSantander(self)
            estrategia.ejecutar()
        elif criterio == "INCISO":
            estrategia = BusquedaInciso(self)
            estrategia.ejecutar()
        else:
            return   

    def seguimiento_ajustadores(self):
        print("Navegando al menú de Seguimiento de Ajustadores...")
        
        # 1. Pequeña pausa para asegurar que el modal anterior (SweetAlert) desapareció completamente
        time.sleep(2) 
        
        # Clic en el menú
        self._click_js(SELECTOR_MENU_SEGUIMIENTO)
        
        print("Esperando carga de la pantalla de Seguimiento...")
        # Damos tiempo a que cargue la nueva página (aumentado por seguridad)
        time.sleep(5)
        
        print("Seleccionando la pestaña 'Por Asignar'...")
        try:
            # 2. CAMBIO CLAVE: Esperar a que el elemento sea VISIBLE, no solo presente
            tab_element = self.wait.until(EC.visibility_of_element_located(SELECTOR_TAB_POR_ASIGNAR))
            
            # 3. Movernos al elemento para asegurar que nada lo tapa
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab_element)
            time.sleep(1) # Pausa para que el scroll termine
            
            # 4. Intentar clic
            # Intentamos clic nativo primero (es más seguro para detectar si algo lo tapa)
            try:
                tab_element.click()
            except Exception:
                # Si falla, forzamos con JS
                print("Clic nativo falló, forzando con JS...")
                self.driver.execute_script("arguments[0].click();", tab_element)
                
            print(">> Pestaña 'Por Asignar' seleccionada.")

        except Exception as e:
            print(f"ERROR: No se pudo encontrar o clickear la pestaña 'Por Asignar'. Detalles: {e}")
            # Opcional: Imprimir el código fuente para depurar si el error persiste
            # print(self.driver.page_source)
            raise # Re-lanzamos el error para detener el bot si esto falla
        
        print("Esperando a que cargue la tabla de registros...")
        # Aumentamos el tiempo de espera para asegurar que la tabla aparezca
        time.sleep(5) 
        
        print("Intentando asignar la primera fila...")
        try:
            # Usamos el wait explícito para asegurar que el botón es clickeable
            btn_asignar = self.wait.until(EC.element_to_be_clickable(SELECTOR_BTN_ASIGNAR_PRIMERA_FILA))
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_asignar)
            time.sleep(1) 
            self.driver.execute_script("arguments[0].click();", btn_asignar)
            print(">> Botón 'Asignar' clickeado correctamente.")
            
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo clickear el botón 'Asignar'. "
                  f"Puede que la tabla esté vacía o tardó demasiado. Detalles: {e}")


    def seleccionar_ajustador(self):
        print("Seleccionando ajustador manualmente...")
        self._click_js(SELECTOR_BTN_ASIGNACION_MANUAL)
        time.sleep(2)
        print("Asignando ajustador...")
        self._click_js(SELECTOR_TXT_ASIGNAR)
        time.sleep(2)
        try:
            # 1. Intenta hacer clic en el primer botón
            self._click_scroll_js(SELECTOR_TXT_ASIGNAR)
            
            # 2. Si la línea de arriba NO falló, ejecuta lo siguiente:
            print("Botón encontrado. Procediendo...")
            time.sleep(2)
            print("Confirmando asignación...")
            self._click_scroll_js(SELECTOR_BTN_ASIGNAR_FINAL)

        except Exception:
            # 3. Si no encuentra el botón, entra aquí y no hace nada (o imprime un log)
            print("El botón de asignar no apareció, el flujo ha terminado.")
            pass

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
    # 1. PREGUNTAR AL USUARIO ANTES DE INICIAR EL BOT
    print("\n--- CONFIGURACIÓN INICIAL ---")
    print("Opciones disponibles: POLIZA, SERIE, PLACAS, SANTANDER, INCISO")
    criterio_usuario = input("Ingrese el criterio de búsqueda deseado en mayusculas: ").strip().upper()
    
    # Validación: Si el usuario solo da Enter, usar un valor por defecto
    if not criterio_usuario:
        print("Entrada vacía. Se usará el valor por defecto: PLACAS")
        criterio_usuario = "PLACAS"

    # 2. INICIAR EL BOT
    # Ahora sí coincide el argumento con el __init__
    bot = Atlas(headless=False)
    
    try:
        bot.iniciar_sesion()
        bot.datos_del_reportante()
        bot.datos_del_conductor()
        bot.ubicacion_del_siniestro()
        bot.finalizar_registro()
        bot.datos_del_siniestro()
        bot.ajuste_remoto()
        
        # 3. PASAR LA VARIABLE CAPTURADA AL INICIO
        bot.buscar_poliza_dinamica(criterio=criterio_usuario)
        
        bot.seguimiento_ajustadores()
        bot.seleccionar_ajustador()        

        print(">> Automatización finalizada con éxito.")
        time.sleep(5) 
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        # bot.driver.save_screenshot("error_log.png")
        
    finally:
        bot.cerrar()