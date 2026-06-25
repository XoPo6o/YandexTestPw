import pytest
from typing import Generator
from playwright.sync_api import Browser, BrowserContext
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def browser_context(browser: Browser) -> Generator[BrowserContext, None, None]:
    logger.info("🚀 Создан свежий браузерный контекст (функция)")

    context = browser.new_context(
        locale="ru-RU",
        timezone_id="Europe/Moscow",
        geolocation={"latitude": 55.7558, "longitude": 37.6173},
        permissions=[],
        extra_http_headers={
            "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8"
        },
        viewport={"width": 1280, "height": 1024},
    )
    
    context.clear_cookies()
    
    yield context
    context.close()
