from busquedas.estrategia_base import BusquedaEstrategia

class BusquedaSerie(BusquedaEstrategia):
    def __init__(self, page):
        super().__init__(page)
        self.selector_input_serie = "input[formcontrolname='p_serie']"
        self.selector_btn_buscar = "//button[contains(., 'Buscar')]"

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Serie...")
        self.page.locator(self.selector_input_serie).fill("1L01A5329X1142266")
        self.page.locator(self.selector_btn_buscar).click()