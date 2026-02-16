from busquedas.estrategia_base import BusquedaEstrategia

class BusquedaSantander(BusquedaEstrategia):
    def __init__(self, page):
        super().__init__(page)
        # Selectores nativos para Playwright
        self.selector_input_canal = "input[formcontrolname='p_canal']"
        self.selector_input_ramo = "input[formcontrolname='p_ramo']"
        self.selector_input_poliza_santander = "input[formcontrolname='p_poliza']"
        self.selector_input_ano_emision = "input[formcontrolname='p_ano_emision']"
        self.selector_btn_buscar = "//button[contains(., 'Buscar')]"

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Póliza (Santander)...")

        # 1. Llenar campos específicos
        print("Escribiendo canal...")
        self.page.locator(self.selector_input_canal).fill("6")
        
        print("Escribiendo ramo...")
        self.page.locator(self.selector_input_ramo).fill("91")
        
        print("Escribiendo póliza Santander...")
        self.page.locator(self.selector_input_poliza_santander).fill("069109028355501")
        
        print("Escribiendo año de emisión...")
        self.page.locator(self.selector_input_ano_emision).fill("1")
        
        # 2. Buscar
        print("Clic en botón Buscar...")
        # Usamos force=True equivalente a tu _click_js de Selenium por si Angular intercepta el clic
        self.page.locator(self.selector_btn_buscar).click(force=True)