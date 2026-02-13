from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def ir_a(self, url: str):
        self.page.goto(url)

    # Playwright hace el scroll y la espera automática, pero si necesitas un clic forzado
    # similar a tu método _click_js actual:
    def click_forzado(self, selector: str):
        self.page.locator(selector).click(force=True)