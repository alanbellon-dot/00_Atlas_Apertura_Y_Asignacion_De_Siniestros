from busquedas.busqueda_poliza import BusquedaPoliza
from busquedas.busqueda_serie import BusquedaSerie
from busquedas.busqueda_placas import BusquedaPlacas
from busquedas.busqueda_santader import BusquedaSantander
from busquedas.busqueda_inciso import BusquedaInciso
import time, os, sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

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

# --- SELECTORES COMUNES (TABLA DE RESULTADOS) ---
SELECTOR_CHECKBOX_LABEL = (By.XPATH, "(//td[contains(@class, 'mat-column-checkbox')]//label)[1]")
SELECTOR_BTN_SELECCIONAR = (By.XPATH, "//button[contains(., 'Seleccionar')]")
BTN_DESPLEGABLE_ACEPTAR = (By.XPATH, "//button[text()='Aceptar']")
SELECTOR_BTN_ACEPTAR_WARNING = (By.XPATH, "//button[@status='warning' and contains(normalize-space(), 'Aceptar')]")
SELECTOR_BTN_SWAL_ACEPTAR = (By.XPATH, "//button[contains(@class, 'swal2') and contains(., 'Aceptar')]")

# --- SELECTORES ASIGNACIÓN MANUAL ---
BTN_LUPITA = (By.XPATH, "(//button[.//mat-icon[contains(text(), 'search')]])[2]")
SELECTOR_BTN_AGREGAR_AJUSTADOR = (By.XPATH, "//span[contains(@class, 'mdc-button__label') and contains(text(), 'Agregar Ajustador')]")
SELECTOR_BTN_ASIGNACION_MANUAL = (By.XPATH, "//button[contains(normalize-space(), 'Asignación manual')]")
SELECTOR_BTN_ASIGNAR_FINAL = (By.XPATH, "//button[@status='success' and contains(normalize-space(), 'Asignar')]")
SELECTOR_BTN_CERRAR_MODAL = (By.XPATH, "//button[contains(@class, 'btn-cerrar-modal')]")
SELECTOR_BTN_CAMBIAR_ESTATUS = (By.XPATH, "//span[contains(@class, 'mdc-button__label') and contains(normalize-space(), 'Cambiar Estatus')]")
SELECTOR_DROPDOWN_ESTATUS = (By.CSS_SELECTOR, "mat-select[formcontrolname='idEstatus']")
SELECTOR_DROPDOWN_MOTIVO = (By.CSS_SELECTOR, "mat-select[formcontrolname='idMotivo']")
SELECTOR_OPCION_PENDIENTE = (By.XPATH, "//mat-option//span[contains(normalize-space(), 'Pendiente')]")
SELECTOR_TEXTAREA_OBSERVACIONES = (By.CSS_SELECTOR, "textarea[formcontrolname='observaciones']")
SELECTOR_OPCION_NO_LOCALIZADO = (By.XPATH, "//mat-option//span[contains(normalize-space(), 'No localizado')]")
SELECTOR_BTN_ACEPTAR = (By.XPATH, "//button[@type='submit' and contains(normalize-space(), 'Aceptar')]")
SELECTOR_BTN_ACTUALIZAR = (By.XPATH, "//button[@ng-reflect-message='Actualizar tabla']")
SELECTOR_BTN_ASIGNAR_FINAL = (By.XPATH, "//button[@status='success' and contains(normalize-space(), 'Asignar')]")

# --- SELECTORES: MENÚ SEGUIMIENTO AJUSTADORES ---
SELECTOR_MENU_SEGUIMIENTO = (By.XPATH, "//a[@title='Seguimiento ajustadores']")
SELECTOR_TAB_POR_ASIGNAR = (By.XPATH, "//span[contains(., 'Por Asignar')]")
SELECTOR_BTN_ASIGNAR_PRIMERA_FILA = (By.XPATH, "(//tbody//tr)[1]//button[contains(., 'Asignar')]")

# --- SELECTORES: SELECCIÓN DE AJUSTADOR ---
SELECTOR_BTN_ASIGNACION_MANUAL = (By.XPATH, "//button[contains(., 'Asignación manual')]")
# Alternativa: Busca SOLO dentro de la ventana modal/dialogo
SELECTOR_TXT_ASIGNAR = (By.XPATH, "//span[normalize-space()='Asignar']")
SELECTOR_BTN_ASIGNAR_FINAL = (By.XPATH, "//button[@status='success' and contains(., 'Asignar')]")

class Atlas:
    def __init__(self, headless=False):
        """
        Se ejecuta al crear el bot.
        Acepta 'headless' para decidir si mostrar o no el navegador.
        """
        print("Inicializando configuración del Bot...")
        
        try:
            os.system("taskkill /f /im chromedriver.exe >nul 2>&1")
            time.sleep(1) 
        except:
            pass

        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless=new")

        prefs = {
            "credentials_enable_service": False, 
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False
        }
        chrome_options.add_experimental_option("prefs", prefs)

        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--remote-allow-origins=*")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        
        print("Bot iniciado correctamente.")


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
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", element)


    def _click_js(self, locator):
        """Fuerza un click usando JavaScript (útil para checkboxes rebeldes)."""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].click();", element)

    def _click_if_exists(self, locator, timeout=3):
        """
        Intenta hacer clic en un elemento si aparece dentro del tiempo especificado.
        Si no aparece, simplemente lo ignora y continua (no lanza error).
        """
        try:
            # Usamos un wait con timeout corto personalizado para no esperar 10s si no es necesario
            wait_short = WebDriverWait(self.driver, timeout)
            element = wait_short.until(EC.presence_of_element_located(locator))
            
            # Scroll para asegurar visibilidad
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            
            # Clic JS
            self.driver.execute_script("arguments[0].click();", element)
            print(f"   -> Clic opcional exitoso en: {locator}")
            return True
        except Exception:
            # Si no existe o falla, simplemente retornamos False sin romper el programa
            # print(f"   (Info) Elemento opcional no encontrado o no necesario: {locator}") # Descomentar para debug
            return False

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

        print("Llenando primer teléfono...")
        self._click(BTN_DESPLEGABLE)    # Abre el menú 1
        self._click(OPCION_CELULAR)     # Elige Celular
        self._escribir(INPUTS_TELEFONO, "5555555555")
        
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
            
            self._esperar_elemento(INPUT_MAPA).send_keys(Keys.ENTER)
            
            print(f">> Dirección '{direccion}' ingresada con éxito.")
            time.sleep(2)

        except Exception as e:
            print(f"Error en ubicacion_del_siniestro: {e}")
            raise

    def finalizar_registro(self):
        print("Finalizando registro...")
        try:
            elemento = self._esperar_elemento(BTN_CREAR_FOLIO)
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
            time.sleep(1)
            
            self.driver.execute_script("arguments[0].click();", elemento)
            
            print(">> Clic exitoso en Crear Folio.")
        
        except Exception as e:
            print(f"Error: {e}")
            raise
    
    def datos_del_siniestro(self):
        print("Llenando datos del siniestro...")
        time.sleep(2)
        print("Dando clic en el calendario...")
        self._click_js(BTN_CALENDARIO)
        time.sleep(1)
        self._click_js(BTN_DIA_HOY)
        self._click_js(BTN_RELOJ)
        print("Escribiendo hechos...")
        campo = self._esperar_elemento(TEXTAREA_HECHOS)
        
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'}); arguments[0].click();", campo)
        time.sleep(0.5)
        
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

        try:
            print(f"Abriendo menú 'Buscar por'...")
            self._click_js(SELECTOR_DROPDOWN_CRITERIO)
            time.sleep(1)

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
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error seleccionando el criterio en el dropdown: {e}")

        if criterio == "POLIZA":
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

    def procesar_seleccion_en_tabla(self):
        print("Esperando resultados y seleccionando registro...")
        
        # Esperar a que la tabla cargue (es mejor esperar al checkbox que dormir 3s)
        try:
            self._esperar_elemento(SELECTOR_CHECKBOX_LABEL)
        except:
            print("No se encontraron resultados en la tabla.")
            return

        self._click_js(SELECTOR_CHECKBOX_LABEL)
        time.sleep(0.5) 
        
        print("Clic en botón Seleccionar...")
        self._click_js(SELECTOR_BTN_SELECCIONAR)
        
        # Manejo robusto del doble clic en Seleccionar (a veces necesario)
        if self._click_if_exists(SELECTOR_BTN_SELECCIONAR, timeout=2):
            print("   -> Se requirió un segundo clic en Seleccionar.")
        
        print("Gestionando confirmaciones y popups...")
 
        # 1. Botón Desplegable (Aceptar simple)
        # Usamos _click_if_exists en lugar de try/except manual
        if self._click_if_exists(BTN_DESPLEGABLE_ACEPTAR, timeout=5):
            print("Botón desplegable aceptado.")
            time.sleep(1) # Pequeña pausa para permitir transición
        else:
            print("El botón desplegable no apareció (continuando)...")

        # 2. Botón Warning (Amarillo) - AHORA ES OPCIONAL
        # Antes esto rompía el script si no salía el warning
        if self._click_if_exists(SELECTOR_BTN_ACEPTAR_WARNING, timeout=5):
            print("Advertencia (Warning) aceptada.")
            time.sleep(1)

        # 3. Sweet Alert (Swal) - AHORA ES OPCIONAL
        # Antes esto rompía el script si no salía la confirmación final
        if self._click_if_exists(SELECTOR_BTN_SWAL_ACEPTAR, timeout=5):
            print("Confirmación final (Swal) aceptada.")
            time.sleep(2) # Esperar a que el modal se cierre visualmente

    def asignacion_manual(self):
        print("Damos clic a la lupita")
        time.sleep(2)
        self._click(BTN_LUPITA)
        
        time.sleep(2)
        print("Dando clic en Agregar Ajustador...")
        self._click(SELECTOR_BTN_AGREGAR_AJUSTADOR)
        
        print("Seleccionando Asignación manual...")
        self._click(SELECTOR_BTN_ASIGNACION_MANUAL)
        
        NOMBRE_OBJETIVO = "MANUEL ALEJANDRO BOLAÑOS GAMIÑO"
        print(f"Buscando a: {NOMBRE_OBJETIVO}...")
        time.sleep(2)

        xpath_dinamico = f"//tr[.//span[contains(normalize-space(), '{NOMBRE_OBJETIVO}')]]//span[contains(normalize-space(), 'Asignar')]"
        
        try:
            btn_asignar_especifico = self.driver.find_element(By.XPATH, xpath_dinamico)
            print(f"¡Encontrado! Asignando a {NOMBRE_OBJETIVO}...")
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_asignar_especifico)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", btn_asignar_especifico)
            
            time.sleep(1)
            self._click(SELECTOR_BTN_ASIGNAR_FINAL)
            
            print("Esperando 5 minutos (305s)...")
            time.sleep(305) 

            print("Cerrando modal para leer la tabla principal...")
            self._click_js(SELECTOR_BTN_CERRAR_MODAL)
            time.sleep(3) # Espera para que se vea la tabla de fondo
            
            xpath_estatus_primera_fila = "//tbody/tr[1]//td[contains(@class, 'mat-column-estatus')]"
            
            celdas = self.driver.find_elements(By.XPATH, xpath_estatus_primera_fila)

            if celdas:
                texto_estatus = celdas[0].text.strip().upper()
                
                print(f"👀 EL ROBOT LEYÓ EN LA PRIMERA FILA: '{texto_estatus}'")

                if "ACEPTADA" in texto_estatus:
                    print("✅ ¡DETECTADO! El estatus es ACEPTADA.")
                    print("🛑 APAGANDO EL PROGRAMA.")
                    self.driver.quit()
                    sys.exit()
                else:
                    print(f"⚠️ El estatus NO es Aceptada (Es '{texto_estatus}').")
                    print("⬇️ Continuando con la cancelación...")
            else:
                print("❌ ERROR CRÍTICO: No se encontró la primera fila de la tabla. Cancelando por seguridad.")


            print("Re-abriendo detalles (Lupa) para cancelar...")
            time.sleep(2)
            self._click(BTN_LUPITA) 
            
            print("Cambiando estatus...")
            time.sleep(2)
            self._click_js(SELECTOR_BTN_CAMBIAR_ESTATUS)
            
            print("Seleccionando opcion pendiente")
            time.sleep(1)
            self._click_js(SELECTOR_DROPDOWN_ESTATUS)
            time.sleep(1)
            self._click_js(SELECTOR_OPCION_PENDIENTE)
            
            print("Escogiendo motivo")
            time.sleep(1)
            self._click_js(SELECTOR_DROPDOWN_MOTIVO)
            time.sleep(1)
            self._click_js(SELECTOR_OPCION_NO_LOCALIZADO)
            
            print("Escribiendo observaciones...")
            time.sleep(1)
            self._escribir(SELECTOR_TEXTAREA_OBSERVACIONES, "Timeout 5 min.")
            
            time.sleep(1)
            self._click_js(SELECTOR_BTN_ACEPTAR)
            print(">> Cancelación finalizada.")

        except NoSuchElementException:
            print(f"NO se encontró a {NOMBRE_OBJETIVO} para asignar.")
            return

    def seguimiento_ajustadores(self):
        print("Navegando al menú de Seguimiento de Ajustadores...")
        time.sleep(2) 
        self._click_js(SELECTOR_MENU_SEGUIMIENTO)
        
        print("Esperando carga de la pantalla de Seguimiento...")
        time.sleep(5)
        
        print("Seleccionando la pestaña 'Por Asignar'...")
        try:
            tab_element = self.wait.until(EC.visibility_of_element_located(SELECTOR_TAB_POR_ASIGNAR))
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", tab_element)
            time.sleep(1) # Pausa para que el scroll termine
            
            try:
                tab_element.click()
            except Exception:
                print("Clic nativo falló, forzando con JS...")
                self.driver.execute_script("arguments[0].click();", tab_element)
                
            print(">> Pestaña 'Por Asignar' seleccionada.")

        except Exception as e:
            print(f"ERROR: No se pudo encontrar o clickear la pestaña 'Por Asignar'. Detalles: {e}")
            raise
        
        print("Esperando a que cargue la tabla de registros...")
        time.sleep(5) 
        
        print("Intentando asignar la primera fila...")
        try:
            btn_asignar = self.wait.until(EC.element_to_be_clickable(SELECTOR_BTN_ASIGNAR_PRIMERA_FILA))
            
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_asignar)
            time.sleep(1)
            self.driver.execute_script("arguments[0].click();", btn_asignar)
            print(">> Botón 'Asignar' clickeado correctamente.")
            
        except Exception as e:
            print(f"ADVERTENCIA: No se pudo clickear el botón 'Asignar'. "
                  f"Puede que la tabla esté vacía o tardó demasiado. Detalles: {e}")

        print("Seleccionando ajustador manualmente...")
        self._click_js(SELECTOR_BTN_ASIGNACION_MANUAL)
        time.sleep(2)
        print("Asignando ajustador...")
        self._click_js(SELECTOR_TXT_ASIGNAR)
        time.sleep(2)
        try:
            self._click_scroll_js(SELECTOR_TXT_ASIGNAR)
            
            print("Botón encontrado. Procediendo...")
            time.sleep(2)
            print("Confirmando asignación...")
            self._click_scroll_js(SELECTOR_BTN_ASIGNAR_FINAL)
            time.sleep(1)
            print("Desplegando opciones de Motivo de Cancelación...")
            self._click_js(SELECTOR_DROPDOWN_MOTIVO)
            time.sleep(1)

        except Exception:
            print("El botón de asignar no apareció, el flujo ha terminado.")
            pass

    def cerrar(self):
        print("Cerrando navegador...")
        try:
            self.driver.quit()
        except Exception:
            pass

if __name__ == "__main__":
    print("\n--- CONFIGURACIÓN INICIAL ---")
    
    print("Opciones de Búsqueda: POLIZA, SERIE, PLACAS, SANTANDER, INCISO")
    criterio_usuario = input("Ingrese el criterio de búsqueda deseado en mayúsculas: ").strip().upper()
    
    if not criterio_usuario:
        print("Entrada vacía. Se usará el valor por defecto: PLACAS")
        criterio_usuario = "PLACAS"

    print("\n--- TIPO DE ASIGNACIÓN ---")
    print("1. Asignación Manual (Directa desde la tabla)")
    print("2. Asignación por Menú de Seguimiento")
    opcion_asignacion = input("Seleccione una opción (1 o 2): ").strip()

    bot = Atlas(headless=False)
    
    try:
        bot.iniciar_sesion()
        bot.datos_del_reportante()
        bot.datos_del_conductor()
        bot.ubicacion_del_siniestro()
        bot.finalizar_registro()
        bot.datos_del_siniestro()
        bot.ajuste_remoto()
        
        bot.buscar_poliza_dinamica(criterio=criterio_usuario)
        bot.procesar_seleccion_en_tabla()
        
        if opcion_asignacion == "2":
            bot.seguimiento_ajustadores()
        else:
            bot.asignacion_manual()  

        print(">> Automatización finalizada con éxito.")
        time.sleep(5) 
        
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        
    finally:
        bot.cerrar()