import pytest

from playwright.sync_api import sync_playwright


@pytest.fixture(scope='session')
def playwright():
    """Создает и возвращает экземпляр Playwright для тестовой сессии."""
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope='session')
def browser(playwright, request):
    """Запускает браузер по выбранному типу."""
    browser_name = request.config.getoption("--driver")
    headless = request.config.getoption("--headless")
    match browser_name:
        case 'chromium':
            browser = playwright.chromium.launch(headless=headless)
        case 'firefox':
            browser = playwright.firefox.launch(headless=headless)
        case _:
            raise ValueError(f'Unknown browser: {browser_name}')

    yield browser, browser_name
    browser.close()

@pytest.fixture(scope="session")
def context(browser, request):
    """Создает браузерный контекст с настройками для конкретного браузера."""
    browser, browser_name = browser
    match browser_name:
        case "chromium":
            context = browser.new_context(ignore_https_errors=True,
                                          permissions=["clipboard-read", "clipboard-write"],
                                          record_video_dir="videos/")
        case "firefox":
            context = browser.new_context(ignore_https_errors=True)
        case _:
            raise ValueError(f"Unsupported browser: {browser_name}")

    yield context

@pytest.fixture(scope='function')
def page(context):
    """Создает новую вкладку страницы."""
    page = context.new_page()
    yield page
    page.close()

