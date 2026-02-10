from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.url = "https://aseguradoradigitaldesarrollo.web.app/iniciar-sesion"

        # --- SELECTORES ---
        self.input_user = page.locator("#mat-input-0")
        self.input_pass = page.locator("#mat-input-1")
        # Definimos el nombre como 'btn_ingresar'
        self.btn_ingresar = page.locator("//button[contains(., 'Ingresar')]")

    def navigate(self):
        print(f"Navegando a: {self.url}")
        self.page.goto(self.url)

    def login(self, usuario, password):
        print("Ingresando credenciales...")
        self.input_user.fill(usuario) 
        self.input_pass.fill(password)
        
        print("Dando click en Ingresar...")
        # Aquí usamos EXACTAMENTE el mismo nombre definido arriba
        self.btn_ingresar.click()