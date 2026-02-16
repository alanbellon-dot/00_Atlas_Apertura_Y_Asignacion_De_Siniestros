from busquedas.estrategia_base import BusquedaEstrategia

class BusquedaInciso(BusquedaEstrategia):
    def __init__(self, page):
        super().__init__(page)
        # Selectores nativos para Playwright
        self.selector_input_sucursal = "input[formcontrolname='p_sucursal']"
        self.selector_input_poliza_central = "input[formcontrolname='p_poliza_central']"
        self.selector_btn_buscar = "//button[contains(., 'Buscar')]"

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Inciso...")

        # 1. Llenar campos específicos
        print("Escribiendo sucursal...")
        self.page.locator(self.selector_input_sucursal).fill("H00")
        
        print("Escribiendo póliza central...")
        self.page.locator(self.selector_input_poliza_central).fill("65063")
        
        # 2. Buscar
        print("Clic en botón Buscar...")
        self.page.locator(self.selector_btn_buscar).click(force=True)