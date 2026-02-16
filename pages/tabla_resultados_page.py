from pages.base_page import BasePage

class TablaResultadosPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        
        # --- SELECTORES ---
        self.checkbox_tabla = "(//td[contains(@class, 'mat-column-checkbox')]//input[@type='checkbox'])[1]"
        self.btn_seleccionar = "//button[contains(., 'Seleccionar')]"
        
        # Selectores de Popups genéricos buscando botones visibles
        self.popups = [
            "button.swal2-cancel:visible",
            "button.swal2-confirm:visible",
            ".swal2-actions button:visible",
            "mat-dialog-container button:visible",
            "button[status='warning']:visible"
        ]

    def procesar_seleccion(self):
        print("Procesando selección de registro en tabla...")
        
        # 1. ESPERA A QUE APAREZCA LA TABLA
        print("Esperando a que carguen los resultados...")
        try:
            # Esperamos que el input de la tabla exista
            self.page.locator(self.checkbox_tabla).wait_for(state="attached", timeout=15000)
            self.page.wait_for_timeout(1000) # Respiro para que terminen las animaciones
        except Exception:
            print(">> [!] La tabla de resultados no cargó o tardó demasiado.")
            return

        # 2. MARCAR EL CHECKBOX (CON VERIFICACIÓN)
        print("Intentando marcar el registro...")
        
        # En Angular, es más seguro darle clic a la celda que al input oculto
        celda_checkbox = self.page.locator("(//td[contains(@class, 'mat-column-checkbox')])[1]")
        input_checkbox = self.page.locator(self.checkbox_tabla)

        marcado_exitoso = False
        # Intentamos marcarlo hasta 3 veces y verificamos si funcionó
        for intento_check in range(3):
            celda_checkbox.click(force=True)
            self.page.wait_for_timeout(1000) # Dar tiempo a que Angular registre el evento
            
            # Verificar si realmente se marcó en el sistema
            if input_checkbox.is_checked():
                marcado_exitoso = True
                print(">> Checkbox marcado y verificado exitosamente.")
                break
            else:
                print(f"   [!] El checkbox no se marcó, intentando de nuevo... ({intento_check + 1}/3)")

        if not marcado_exitoso:
            print(">> [!] Advertencia: No se pudo confirmar visualmente el check. Avanzando...")

        # 3. MANEJO DE POPUPS Y BOTÓN SELECCIONAR
        for intento in range(20):
            # A. Éxito si la tabla se cerró (el botón seleccionar ya no está)
            if not self.page.locator(self.btn_seleccionar).is_visible():
                print(">> Selección completada (Tabla cerrada correctamente).")
                break

            # B. Intentar Seleccionar
            try:
                if self.page.locator(self.btn_seleccionar).is_enabled():
                    self.page.locator(self.btn_seleccionar).click(timeout=1000)
            except Exception:
                pass
            
            # C. Buscar y matar UN popup por iteración
            popup_manejado = False
            for selector in self.popups:
                popup = self.page.locator(selector).filter(has_text="Aceptar").first
                
                if popup.is_visible():
                    print(f"   [!] Popup detectado (Intento {intento+1}), eliminando...")
                    self.page.wait_for_timeout(500)
                    
                    try:
                        popup.evaluate("node => node.click()")
                        popup.press("Enter")
                        self.page.evaluate("() => { if(window.Swal) { window.Swal.close(); } }")
                        print("   >> Clic y comandos de cierre ejecutados.")
                    except Exception as e:
                        print(f"   >> Error al intentar cerrar: {e}")
                        
                    self.page.wait_for_timeout(1000)
                    popup_manejado = True
                    break
            
            if not popup_manejado:
                self.page.wait_for_timeout(1000)