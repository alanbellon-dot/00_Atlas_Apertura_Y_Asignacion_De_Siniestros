# busquedas/estrategia_base.py
from abc import ABC, abstractmethod
from playwright.sync_api import Page

class BusquedaEstrategia(ABC):
    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    def ejecutar(self):
        pass

# busquedas/busqueda_placas.py
from busquedas.estrategia_base import BusquedaEstrategia

class BusquedaPlacas(BusquedaEstrategia):
    def __init__(self, page):
        super().__init__(page)
        # Playwright soporta CSS sin necesidad de importar 'By.CSS_SELECTOR'
        self.selector_input_placas = "input[formcontrolname='p_placas']"
        self.selector_btn_buscar = "//button[contains(., 'Buscar')]"

    def ejecutar(self):
        print(">> [Estrategia] Iniciando búsqueda por Placas...")
        self.page.locator(self.selector_input_placas).fill("MSN6456")
        self.page.locator(self.selector_btn_buscar).click()