import pytest
import pytest_asyncio

from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright


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
            browser = playwright.chromium.launch(headless=True)
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
            context = browser.new_context(
                ignore_https_errors=True,
                permissions=["clipboard-read", "clipboard-write"],
                viewport={'width': 1280, 'height': 720}
                # record_video_dir="videos/"
            )
        case "firefox":
            context = browser.new_context(ignore_https_errors=True)
        case _:
            raise ValueError(f"Unsupported browser: {browser_name}")

    yield context


@pytest.fixture(scope="function")
def page(context):
    """Создает новую вкладку страницы."""
    page = context.new_page()
    yield page
    page.close()


@pytest_asyncio.fixture(scope='session')
async def playwright_async():
    async with async_playwright() as p:
        yield p


@pytest_asyncio.fixture(scope='session')
async def browser_async(playwright_async, request):
    browser_name = request.config.getoption("--driver")
    headless = request.config.getoption("--headless")
    if browser_name == 'chromium':
        browser = await playwright_async.chromium.launch(headless=headless)
    elif browser_name == 'firefox':
        browser = await playwright_async.firefox.launch(headless=headless)
    else:
        raise ValueError(f'Unknown browser: {browser_name}')
    yield browser
    await browser.close()


@pytest_asyncio.fixture(scope="session")
async def context_async(browser_async, request):
    context = await browser_async.new_context(
        ignore_https_errors=True,
        permissions=["clipboard-read", "clipboard-write"],
        viewport={'width': 1280, 'height': 720}
        # record_video_dir="videos/"
    )
    yield context
    await context.close()


@pytest_asyncio.fixture(scope="function")
async def page_async(context_async):
    page = await context_async.new_page()
    yield page
    await page.close()


