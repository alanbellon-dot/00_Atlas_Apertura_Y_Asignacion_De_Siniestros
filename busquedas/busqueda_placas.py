from busquedas.estrategia_base import BusquedaEstrategia

class BusquedaPlacas(BusquedaEstrategia):
    def __init__(self, page):
        super().__init__(page)
        # Playwright soporta CSS nativamente
        self.selector_input_placas = "input[formcontrolname='p_placas']"
        self.selector_btn_buscar = "//button[contains(., 'Buscar')]"

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Placas...")
        self.page.locator(self.selector_input_placas).fill("MSN6456")
        self.page.locator(self.selector_btn_buscar).click()