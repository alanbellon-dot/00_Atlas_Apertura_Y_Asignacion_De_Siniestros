from abc import ABC, abstractmethod
from playwright.sync_api import Page

class BusquedaEstrategia(ABC):
    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    def ejecutar(self):
        pass