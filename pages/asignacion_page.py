import random
import time
from playwright.sync_api import Page

class AsignacionPage:
    def __init__(self, page: Page):
        self.page = page

        # --- SELECTORES ---
        # Usamos .first para asegurar que tomamos el de la primera fila
        self.lbl_estatus = page.locator("td.mat-column-estatus").first
        self.btn_menu_opciones = page.locator("mat-icon:has-text('more_vert')").first
        
        # Selectores del flujo de asignación
        self.btn_buscar_persona_icon = page.locator("mat-icon:has-text('person_search')")
        self.btn_aceptar = page.locator("button.btn-aceptar")
        
        # Lista de proveedores (usaremos .all() dinámicamente)
        self.selector_proveedores = "span.id-proveedor"
        
        self.btn_seleccionar_ajustador = page.locator("button", has_text="Seleccionar ajustador")
        self.btn_asignar_final = page.locator("button", has_text="Asignar")

    def verificar_y_asignar(self):
        print("--- Verificando Estatus del Siniestro ---")
        
        # Esperamos a que la tabla cargue el estatus
        try:
            self.lbl_estatus.wait_for(state="visible", timeout=15000)
            estatus_texto = self.lbl_estatus.inner_text().strip()
            print(f"Estatus encontrado: '{estatus_texto}'")

            if "Registrada" in estatus_texto:
                print(">>> Estatus OK. Procediendo a asignar...")
                self._realizar_asignacion_manual()
            elif "Asignada" in estatus_texto:
                print(">>> El siniestro YA está asignado. Saltando paso.")
            else:
                print(f"⚠️ Estatus desconocido '{estatus_texto}'. No se asignará.")

        except Exception as e:
            print(f"Error leyendo la tabla (quizás no cargó a tiempo): {e}")

    def _realizar_asignacion_manual(self):
        # 1. Abrir menú de 3 puntos
        self.btn_menu_opciones.click()

        # 2. Click en lupa (Buscar persona)
        # A veces hay animaciones, esperamos un poco
        self.page.wait_for_timeout(500)
        self.btn_buscar_persona_icon.click()

        # 3. Confirmar modal inicial
        self.btn_aceptar.click()

        # 4. Click otra vez en buscar (según tu flujo original)
        self.page.wait_for_timeout(1000)
        self.btn_buscar_persona_icon.click()

        # 5. Selección Random de Proveedor
        print("Buscando proveedores disponibles...")
        # Esperamos a que aparezca al menos uno
        self.page.wait_for_selector(self.selector_proveedores, timeout=10000)
        
        # Obtenemos todos los elementos
        opciones = self.page.locator(self.selector_proveedores).all()
        
        if opciones:
            elegido = random.choice(opciones)
            texto_id = elegido.inner_text()
            print(f"Seleccionando proveedor al azar ID: {texto_id}")
            
            # Click al elegido
            elegido.click()
            
            # 6. Finalizar
            self.page.wait_for_timeout(500)
            self.btn_seleccionar_ajustador.click()
            
            self.page.wait_for_timeout(500)
            self.btn_asignar_final.click()
            print("¡Asignación completada!")
        else:
            print("⚠️ No se encontraron proveedores en la lista.")