from pages.base_page import BasePage

class SiniestroPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # --- SELECTORES: LOADER ---
        self.loader = ".contenedorBlock"
        
        # --- SELECTORES: DATOS DEL REPORTANTE ---
        self.input_nombre = "input[formcontrolname='nombre']"
        self.input_paterno = "input[formcontrolname='apellido_paterno']"
        self.input_materno = "input[formcontrolname='apellido_materno']"
        self.btn_desplegable = ".mat-mdc-select-value"
        self.opcion_celular = "//span[contains(text(), 'Celular')]"
        self.inputs_telefono = "input[formcontrolname='telefono']"
        
        # Como hay varios elementos iguales, en Playwright podemos seguir usando XPATH o nth
        self.btn_desplegable_confirm = "(//div[contains(@class, 'mat-mdc-select-value')])[2]"
        self.opcion_celular_confirm = "(//span[contains(text(), 'Celular')])[2]"
        self.input_confirm_tel = "(//input[@formcontrolname='telefono'])[2]"
        
        self.btn_causa = "//span[contains(text(), 'Causa')]"
        self.opcion_colision = "//span[contains(text(), 'COLISION')]"

        # --- SELECTORES: DATOS DEL CONDUCTOR ---
        # En Playwright podemos usar CSS con el #ID directamente
        self.checkbox_conductor = "#mat-mdc-checkbox-2-input"
        self.checkbox_1 = "#mat-mdc-checkbox-1-input"

        # --- SELECTORES: UBICACIÓN DEL SINIESTRO ---
        self.btn_lupa = "button[aria-label='Btn búsqueda']"
        self.input_mapa = "input.pac-target-input"
        self.btn_crear_folio = "//button[contains(text(), 'Crear folio')]"

        # --- SELECTORES: DATOS DEL SINIESTRO ---
        self.btn_calendario = "mat-datepicker-toggle button"
        self.btn_dia_hoy = "button[aria-current='date']"
        self.btn_reloj = "//mat-icon[contains(text(), 'schedule')]/ancestor::button"
        self.textarea_hechos = "textarea[formcontrolname='que_ocurrio']"
        self.input_placas = "input[formcontrolname='placas_cabina']"
        self.btn_color = "//span[contains(text(), 'Color')]"
        self.opcion_color_amarillo = "//span[contains(text(), 'AMARILLO')]"

        # --- SELECTORES: AJUSTE REMOTO ---
        self.radio_no = "//input[@name='mat-radio-group-4' and @value='false']"
        self.radio_group_5_no = "//input[@name='mat-radio-group-5' and @value='false']"
        self.radio_group_6_no = "//input[@name='mat-radio-group-6' and @value='false']"
        self.radio_group_7_no = "//input[@name='mat-radio-group-7' and @value='false']"

    def esperar_carga(self):
        """Espera a que el loader de Angular desaparezca."""
        print("Esperando que desaparezca la pantalla de carga...")
        # Playwright espera a que el elemento cumpla el estado 'hidden'
        self.page.locator(self.loader).wait_for(state="hidden")

    def llenar_datos_reportante(self, nombre="Juan", paterno="Galindo", materno="Peres", telefono="5555555555"):
        self.esperar_carga()
        print("Llenando datos del reportante...")
        
        # Agregamos .first para decirle a Playwright que tome el primero que encuentre (como hacía Selenium)
        self.page.locator(self.input_nombre).first.fill(nombre)
        self.page.locator(self.input_paterno).first.fill(paterno)
        self.page.locator(self.input_materno).first.fill(materno)

        print("Llenando primer teléfono...")
        self.page.locator(self.btn_desplegable).first.click()
        self.page.locator(self.opcion_celular).first.click()
        self.page.locator(self.inputs_telefono).first.fill(telefono)
        
        print("Llenando segundo teléfono...")
        # Nota: Aquí ya estabas usando [2] en el XPATH desde tu versión anterior, 
        # así que este no debería chocar, pero igual es seguro dejarlo normal.
        self.page.locator(self.btn_desplegable_confirm).click()
        self.page.locator(self.opcion_celular_confirm).click()
        self.page.locator(self.input_confirm_tel).fill(telefono)

        print("Seleccionando causa...")
        self.page.locator(self.btn_causa).first.click()
        self.page.locator(self.opcion_colision).first.click()

    def llenar_datos_conductor(self):
        print("Llenando datos del conductor...")
        # force=True reemplaza tu viejo self._click_js() de Selenium para checkboxes rebeldes
        self.page.locator(self.checkbox_conductor).click(force=True)
        self.page.locator(self.checkbox_1).click(force=True)

    def llenar_ubicacion_siniestro(self, direccion="Metrobús Nápoles, Avenida Insurgentes Sur, Colonia Nápoles, Mexico City, CDMX, Mexico"):
        print("Iniciando ubicación del siniestro...")
        self.page.locator(self.btn_lupa).click(force=True)
        
        # En Playwright es recomendable escribir pausado si es un mapa predictivo
        self.page.locator(self.input_mapa).press_sequentially(direccion, delay=50)
        self.page.locator(self.input_mapa).press("Enter")
        print(f">> Dirección '{direccion}' ingresada con éxito.")

    def finalizar_registro(self):
        print("Finalizando registro (Crear Folio)...")
        # Playwright hace el scroll de forma automática antes de dar clic
        self.page.locator(self.btn_crear_folio).click()
        print(">> Clic exitoso en Crear Folio.")

    def llenar_datos_siniestro(self, hechos="El conductor perdió el control del vehículo y chocó contra un poste.", placas="TX11111"):
        print("Llenando datos del siniestro...")
        
        # 1. Esperamos si aparece algún loader de Angular después de "Crear Folio"
        self.esperar_carga()
        
        # 2. Le damos un pequeño respiro a la UI de Angular (equivalente a tu time.sleep(2) original)
        self.page.wait_for_timeout(1000) 

        print("Dando clic en el calendario...")
        # Quitamos el force=True para que Playwright valide que el botón realmente está listo para recibir el clic
        self.page.locator(self.btn_calendario).click()

        # 3. Esperamos explícitamente a que la animación del calendario termine y el botón sea visible
        print("Seleccionando el día de hoy...")
        btn_hoy = self.page.locator(self.btn_dia_hoy)
        btn_hoy.wait_for(state="visible") 
        btn_hoy.click() # Aquí ya no necesitamos force=True

        self.page.locator(self.btn_reloj).click()

        print("Escribiendo hechos...")
        self.page.locator(self.textarea_hechos).fill(hechos)

        self.page.locator(self.input_placas).fill(placas)
        print("Seleccionando color del vehículo...")
        self.page.locator(self.btn_color).click(force=True)
        self.page.locator(self.opcion_color_amarillo).click()

    def seleccionar_ajuste_remoto(self):
        print("Seleccionando opción 'No' para ajuste remoto...")
        self.page.locator(self.radio_no).click(force=True)
        self.page.locator(self.radio_group_5_no).click(force=True)
        self.page.locator(self.radio_group_6_no).click(force=True)
        self.page.locator(self.radio_group_7_no).click(force=True)
        
    def completar_flujo_siniestro(self):
        """Método de conveniencia para ejecutar todo el flujo de esta página de una vez"""
        self.llenar_datos_reportante()
        self.llenar_datos_conductor()
        self.llenar_ubicacion_siniestro()
        self.finalizar_registro()
        self.llenar_datos_siniestro()
        self.seleccionar_ajuste_remoto()