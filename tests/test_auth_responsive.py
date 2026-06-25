import pytest
from playwright.sync_api import expect
from pages.ya_ru_page import YaRuPage
from pages.passport_auth_page import PassportAuthPage

# --- КОНФИГУРАЦИЯ ЭКРАНОВ ---
ALL_VIEWPORTS = [
    {"width": 320, "height": 568},
    {"width": 768, "height": 1024},
    {"width": 1280, "height": 1024},
    {"width": 1920, "height": 1080},
]

SINGLE_VIEWPORT = {"width": 1280, "height": 1024}


# --- ФИКСТУРЫ (Setup) ---

@pytest.fixture(scope="function")
def viewport_config(request):
    """
    Умная фикстура: определяет, какой viewport использовать.
    Если тест помечен маркером 'all_viewports', возвращает список.
    Иначе возвращает один стандартный экран.
    
    Это позволяет избежать дублирования логики в тестах.
    """
    if request.node.get_closest_marker("all_viewports"):
        return ALL_VIEWPORTS
    return SINGLE_VIEWPORT


@pytest.fixture(scope="function")
def auth_context(page, viewport_config):
    """
    Главная фикстура контекста авторизации.
    1. Настраивает viewport (автоматически подтягивает нужный из viewport_config).
    2. Инициализирует Page Objects.
    3. Выполняет базовый переход на ya.ru и клик по кнопке входа.
    
    Возвращает кортеж: (ya_page, passport_page, current_viewport)
    """
    
    vp = viewport_config
    
    # Если это список (случай параметризации), мы НЕ ставим viewport здесь, 
    # потому что параметризация работает ДО запуска фикстуры setup.
    # Мы просто возвращаем страницы. Настройка viewport останется в параметризованном тесте.
    if isinstance(vp, list):
        ya_page = YaRuPage(page)
        passport_page = PassportAuthPage(page)
        return ya_page, passport_page, None
    
    # Это обычный тест с одним экраном
    page.set_viewport_size(vp)
    ya_page = YaRuPage(page)
    passport_page = PassportAuthPage(page)
    
    # Базовые действия, общие для всех тестов (переход и открытие формы)
    ya_page.go_to_ya_ru().click_login()
    
    return ya_page, passport_page, vp


# --- ТЕСТЫ ---

@pytest.mark.all_viewports
@pytest.mark.parametrize("viewport", ALL_VIEWPORTS, ids=lambda v: f"{v['width']}x{v['height']}")
def test_login_elements_visible_on_all_viewports(page, viewport):
    """
    Тест адаптивности: прогоняется на всех экранах.
    Здесь мы управляем viewport вручную, так как используем parametrize.
    Фикстура auth_context здесь не используется напрямую для установки размера,
    чтобы не конфликтовать с механизмом parametrize, но страницы можно создать явно.
    """
    page.set_viewport_size(viewport)
    
    ya_page = YaRuPage(page)
    passport_page = PassportAuthPage(page)
    ya_page.go_to_ya_ru()
    ya_page.click_login()

    expect(passport_page.phone_input).to_be_visible(timeout=6000)
    expect(passport_page.ya_logo).to_be_visible(timeout=6000)

def test_phone_input_enables_next_button_on_valid_input(auth_context):
    ya_page, passport_page, _ = auth_context
    passport_page.enter_phone("+79990000000")
    expect(passport_page.next_phone_btn).to_be_enabled(timeout=6000)

def test_phone_input_clear(auth_context):
    ya_page, passport_page, _ = auth_context
    passport_page.enter_phone("+79180000000")
    passport_page.click_clear_phone_input()
    expect(passport_page.phone_input).to_be_empty(timeout=6000)

def test_phone_input_shows_error_for_invalid_number(auth_context):
    ya_page, passport_page, _ = auth_context
    passport_page.enter_phone("+71111111111")
    passport_page.click_next()
    expect(passport_page.phone_error_message).to_be_visible(timeout=6000)


def test_more_options_menu_toggles_on_click(auth_context):
    ya_page, passport_page, _ = auth_context
    passport_page.click_more_options()
    expect(passport_page.more_options_cant_enter).to_be_visible(timeout=6000)
    # passport_page.is_more_options_expanded()


def test_forgot_login_flow_opens_recovery_screen(auth_context):
    ya_page, passport_page, _ = auth_context
    passport_page.click_more_options()
    passport_page.restore_account()

    expect(passport_page.forgot_login_link).to_be_visible(timeout=8000)

def test_forgot_password_flow_opens_recovery_screen(auth_context):
    ya_page, passport_page, _ = auth_context
    passport_page.click_more_options()
    passport_page.restore_account()

    expect(passport_page.forgot_password_link).to_be_visible(timeout=8000)

def test_forgot_phone_flow_opens_recovery_screen(auth_context):
    ya_page, passport_page, _ = auth_context
    passport_page.click_more_options()
    passport_page.restore_account()

    expect(passport_page.forgot_phone_link).to_be_visible(timeout=8000)

def test_forgot_info_flow_opens_recovery_screen(auth_context):
    ya_page, passport_page, _ = auth_context
    passport_page.click_more_options()
    passport_page.restore_account()

    expect(passport_page.forgot_info_link).to_be_visible(timeout=8000)

def test_phone_input_receives_focus_after_login_click(auth_context):
    ya_page, passport_page, _ = auth_context
    passport_page.focus_phone_input()
    expect(passport_page.phone_input).to_be_focused(timeout=4000)

def test_webauthn_auth(auth_context):
    ya_page, passport_page, _ = auth_context
    current_url = ya_page.page.url
    passport_page.click_webauthn_auth()
    expect(passport_page.webauthn_auth_page).to_be_visible()

def test_all_key_login_elements_present_single_viewport(auth_context):
    ya_page, passport_page, _ = auth_context
    expect(passport_page.phone_input).to_be_visible(timeout=6000)
    expect(passport_page.more_options_btn).to_be_visible(timeout=6000)
    expect(passport_page.webauthn_auth_btn).to_be_visible(timeout=6000)
