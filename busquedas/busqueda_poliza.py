from busquedas.estrategia_base import BusquedaEstrategia

class BusquedaPoliza(BusquedaEstrategia):
    def __init__(self, page):
        super().__init__(page)
        self.selector_input_sucursal = "input[formcontrolname='p_sucursal']"
        self.selector_input_poliza = "input[formcontrolname='p_poliza_central']"
        self.selector_input_inciso = "input[formcontrolname='p_inciso']"
        self.selector_btn_buscar = "//button[contains(., 'Buscar')]"

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Póliza (Tradicional)...")
        self.page.locator(self.selector_input_sucursal).fill("MS1")
        self.page.locator(self.selector_input_poliza).fill("57089")
        self.page.locator(self.selector_input_inciso).fill("1")
        
        print("Clic en botón Buscar...")
        self.page.locator(self.selector_btn_buscar).click(force=True)