from pages.base_page import BasePage
from utils.config import Config

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Selectores
        self.input_user = "input[formcontrolname='username']"
        self.input_pass = "input[formcontrolname='password']"
        self.btn_login = "//button[contains(., 'Ingresar')]"

    def iniciar_sesion(self):
        print(f"Navegando a {Config.BASE_URL}...")
        self.ir_a(Config.BASE_URL)
        
        print("Ingresando credenciales...")
        # En Playwright usamos 'fill' para escribir y locator para encontrar elementos
        self.page.locator(self.input_user).fill(Config.USERNAME)
        self.page.locator(self.input_pass).fill(Config.PASSWORD)
        
        self.page.locator(self.btn_login).click()
        print("Credenciales enviadas.")