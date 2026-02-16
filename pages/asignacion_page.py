from pages.base_page import BasePage
import sys

class AsignacionPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # --- Selectores Generales ---
        self.loader = ".contenedorBlock"
        self.btn_lupita = "(//button[.//mat-icon[contains(text(), 'search')]])[2]"

        # --- Selectores Asignación Manual (Opción 1) ---
        self.btn_agregar_ajustador = "//span[contains(@class, 'mdc-button__label') and contains(text(), 'Agregar Ajustador')]"
        self.btn_asignacion_manual = "//button[contains(normalize-space(), 'Asignación manual')]"
        self.btn_asignar_final = "//button[@status='success' and contains(normalize-space(), 'Asignar')]"
        self.btn_cerrar_modal = "//button[contains(@class, 'btn-cerrar-modal')]"

        # Elementos de Cancelación
        self.btn_cambiar_estatus = "//span[contains(@class, 'mdc-button__label') and contains(normalize-space(), 'Cambiar Estatus')]"
        self.dropdown_estatus = "mat-select[formcontrolname='idEstatus']"
        self.opcion_pendiente = "//mat-option//span[contains(normalize-space(), 'Pendiente')]"
        self.dropdown_motivo = "mat-select[formcontrolname='idMotivo']"
        self.opcion_no_localizado = "//mat-option//span[contains(normalize-space(), 'No localizado')]"
        self.textarea_observaciones = "textarea[formcontrolname='observaciones']"
        self.btn_aceptar = "//button[@type='submit' and contains(normalize-space(), 'Aceptar')]"

        # --- Selectores Seguimiento (Opción 2) ---
        self.btn_swal_cancel_aceptar = "//button[contains(@class, 'swal2-cancel') and contains(., 'Aceptar')]"
        self.menu_seguimiento = "//a[@title='Seguimiento ajustadores']"
        self.tab_por_asignar = "//span[contains(., 'Por Asignar')]"
        self.btn_asignar_primera_fila = "(//tbody//tr)[1]//button[contains(., 'Asignar')]"
        self.txt_asignar = "//span[normalize-space()='Asignar']"

    def asignacion_manual(self, nombre_objetivo="MANUEL ALEJANDRO BOLAÑOS GAMIÑO"):
        print("Iniciando asignación manual (Lupa)...")
        self.page.wait_for_timeout(2000)
        self.page.locator(self.btn_lupita).click()
        
        self.page.wait_for_timeout(2000)
        print("Dando clic en Agregar Ajustador...")
        self.page.locator(self.btn_agregar_ajustador).click()
        
        print("Seleccionando Asignación manual...")
        self.page.locator(self.btn_asignacion_manual).click()
        
        print(f"Buscando a: {nombre_objetivo}...")
        self.page.wait_for_timeout(2000)

        # Usamos F-Strings para inyectar el nombre dinámicamente
        xpath_dinamico = f"//tr[.//span[contains(normalize-space(), '{nombre_objetivo}')]]//span[contains(normalize-space(), 'Asignar')]"
        
        if self.page.locator(xpath_dinamico).is_visible():
            print(f"¡Encontrado! Asignando a {nombre_objetivo}...")
            
            # Playwright hace el scroll automáticamente si lo necesita
            self.page.locator(xpath_dinamico).scroll_into_view_if_needed()
            self.page.locator(xpath_dinamico).click()
            
            self.page.wait_for_timeout(1000)
            self.page.locator(self.btn_asignar_final).click()
            
            print("Esperando 5 minutos (305s) para revisar estatus...")
            self.page.wait_for_timeout(305000) 

            print("Cerrando modal para leer la tabla principal...")
            self.page.locator(self.btn_cerrar_modal).click(force=True)
            self.page.wait_for_timeout(3000) 

            # Leer la tabla
            xpath_estatus_primera_fila = "//tbody/tr[1]//td[contains(@class, 'mat-column-estatus')]"
            # .inner_text() es el equivalente de .text en Selenium
            texto_estatus = self.page.locator(xpath_estatus_primera_fila).inner_text().strip().upper()
            
            print(f"👀 EL ROBOT LEYÓ EN LA PRIMERA FILA: '{texto_estatus}'")

            if "ACEPTADA" in texto_estatus:
                print("✅ ¡DETECTADO! El estatus es ACEPTADA.")
                print("🛑 APAGANDO EL PROGRAMA.")
                sys.exit()
            else:
                print(f"⚠️ El estatus NO es Aceptada (Es '{texto_estatus}').")
                print("⬇️ Continuando con la cancelación...")

            # --- Proceso de Cancelación ---
            print("Re-abriendo detalles (Lupa) para cancelar...")
            self.page.wait_for_timeout(2000)
            self.page.locator(self.btn_lupita).click() 
            
            print("Cambiando estatus a Pendiente / No localizado...")
            self.page.wait_for_timeout(2000)
            self.page.locator(self.btn_cambiar_estatus).click(force=True)
            
            self.page.locator(self.dropdown_estatus).click(force=True)
            self.page.locator(self.opcion_pendiente).click()
            
            self.page.locator(self.dropdown_motivo).click(force=True)
            self.page.locator(self.opcion_no_localizado).click()
            
            self.page.locator(self.textarea_observaciones).fill("Timeout 5 min.")
            self.page.locator(self.btn_aceptar).click(force=True)
            print(">> Cancelación finalizada.")

        else:
            print(f"NO se encontró a {nombre_objetivo} para asignar.")

    def seguimiento_ajustadores(self):
        print("--- INICIANDO MÓDULO DE SEGUIMIENTO ---")
        self.page.wait_for_timeout(1000)
        
        # Cerrar SweetAlert si existe
        try:
            if self.page.locator(self.btn_swal_cancel_aceptar).is_visible():
                self.page.locator(self.btn_swal_cancel_aceptar).click(force=True)
        except:
            pass
            
        # Esperar que desaparezca la pantalla de carga
        self.page.locator(self.loader).wait_for(state="hidden")

        print("Navegando al menú de Seguimiento...")
        self.page.locator(self.menu_seguimiento).click()
        
        self.page.wait_for_timeout(4000)

        print(">> Seleccionando pestaña 'Por Asignar'...")
        self.page.locator(self.tab_por_asignar).click()
        
        print(">> Esperando tabla de registros...")
        self.page.wait_for_timeout(3000) 
        
        try:
            self.page.locator(self.btn_asignar_primera_fila).click()
            print(">> Botón 'Asignar' clickeado.")
        except:
            print(">> Advertencia: No se pudo clickear 'Asignar' (¿Tabla vacía?).")

        print(">> Procesando asignación manual...")
        try:
            self.page.locator(self.btn_asignacion_manual).click(force=True)
            self.page.wait_for_timeout(2000)
            
            # En Playwright usamos .first para el equivalente a [1]
            self.page.locator(self.txt_asignar).first.click(force=True)
            self.page.wait_for_timeout(2000)
            
            self.page.locator(self.btn_asignar_final).click(force=True)
            self.page.wait_for_timeout(1000)
        except:
            pass