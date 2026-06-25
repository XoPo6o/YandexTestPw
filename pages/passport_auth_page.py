from playwright.sync_api import Page, expect

class PassportAuthPage:
    def __init__(self, page: Page):
        self.page = page
        # Кнопки
        self.phone_input = page.get_by_test_id("text-field-input")
        self.next_phone_btn = page.get_by_test_id("split-add-user-next-phone")
        self.more_options_btn = page.get_by_test_id("split-add-user-more-button")
        self.webauthn_auth_btn = page.get_by_test_id("webauthn-auth-button")
        self.webauthn_auth_page = page.get_by_text("Make sure that your face or")
        self.clear_input_btn = page.get_by_test_id("int-phone-clear-input-btn")
        # Еще - Не могу войти
        self.more_options_cant_enter = page.get_by_test_id("menu-option-restoreAccount")
        self.more_options_restore_account = page.get_by_test_id("menu-option-restoreAccount")
        self.forgot_password_link = page.get_by_test_id("cant-login-forgot-password-link")
        self.forgot_login_link = page.get_by_test_id("cant-login-forgot-login-link")
        self.forgot_phone_link = page.get_by_test_id("cant-login-by-phone-link")
        self.forgot_info_link = page.get_by_test_id("cant-login-find-solution-link")
        # Остальное
        self.phone_error_message = page.get_by_test_id("error-message")
        self.ya_logo = page.get_by_test_id("auth-logo")

    def enter_phone(self, phone: str):
        self.phone_input.fill(phone)
        return self

    def click_next(self):
        self.next_phone_btn.click()
        return self

    def click_webauthn_auth(self):
        self.webauthn_auth_btn.click()
        return self
    
    def focus_phone_input(self):
        self.phone_input.focus()
        return self
    
    def click_clear_phone_input(self):
        self.clear_input_btn.click()
        return self

    def click_more_options(self):
        self.more_options_btn.click()
        return self

    def is_more_options_expanded(self):
        self.more_options_cant_enter.to_be_visible()
        return self
    
    def restore_account(self):
        self.more_options_restore_account.click()
        return self

    def click_login_password(self):
        self.forgot_login_link.click()
        return self
    
    def click_forgot_password(self):
        self.forgot_password_link.click()
        return self
