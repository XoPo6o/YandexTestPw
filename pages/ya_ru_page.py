from playwright.sync_api import Page

class YaRuPage:
    def __init__(self, page: Page):
        self.page = page
        self.login_button = page.get_by_role("link", name="Войти")
        self.phone_input = page.get_by_test_id("text-field-input")
        self.next_button = page.get_by_test_id("split-add-user-next-phone")

    def go_to_ya_ru(self) -> "YaRuPage":
        self.page.goto("https://ya.ru")
        return self

    def click_login(self) -> "YaRuPage":
        self.login_button.click()
        self.page.wait_for_load_state("load") 
        return self

    def enter_phone(self, phone: str) -> "YaRuPage":
        self.phone_input.fill(phone)
        return self

    def click_next(self) -> "YaRuPage":
        self.next_button.click()
        return self
