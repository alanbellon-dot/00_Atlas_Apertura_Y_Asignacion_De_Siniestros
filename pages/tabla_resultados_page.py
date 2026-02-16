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
        self.page.wait_for_timeout(3000) 
        
        print("Intentando marcar el registro...")
        try:
            self.page.locator(self.checkbox_tabla).check(force=True, timeout=2000)
            print(">> Checkbox marcado exitosamente.")
        except Exception:
            pass

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
            # C. Buscar y matar UN popup por iteración
            popup_manejado = False
            for selector in self.popups:
                # Buscamos botones que contengan el texto 'Aceptar'
                popup = self.page.locator(selector).filter(has_text="Aceptar").first
                
                if popup.is_visible():
                    print(f"   [!] Popup detectado (Intento {intento+1}), eliminando...")
                    
                    # 1. Pausa breve para estabilización
                    self.page.wait_for_timeout(500)
                    
                    try:
                        # 2. MÉTODO TRIPLE ACCIÓN:
                        # A) Intentamos el clic de JS que ya tenías
                        popup.evaluate("node => node.click()")
                        
                        # B) Mandamos la tecla Enter por si el foco se perdió
                        popup.press("Enter")
                        
                        # C) LA SOLUCIÓN DEFINITIVA: 
                        # Si es un SweetAlert, le pedimos a la librería que se cierre inmediatamente
                        # o removemos el overlay visual mediante JS para que deje de bloquear la pantalla.
                        self.page.evaluate("() => { if(window.Swal) { window.Swal.close(); } }")
                        
                        print("   >> Clic y comandos de cierre ejecutados.")
                    except Exception as e:
                        print(f"   >> Error al intentar cerrar: {e}")
                        
                    # 3. Pausa para permitir que Angular procese el cierre
                    self.page.wait_for_timeout(1000)
                    
                    popup_manejado = True
                    break
            
            # Si en esta iteración no hubo popups, esperamos un poco antes de volver a intentar "Seleccionar"
            if not popup_manejado:
                self.page.wait_for_timeout(1000)