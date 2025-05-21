import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

# @pytest_asyncio.fixture(scope='session')
# async def page_async():
#     playwright_async = await async_playwright().start()
#     browser = await playwright_async.chromium.launch(headless=False, args=None)
#     page = await browser.new_page()
#
#
#     yield page
#     await playwright_async.stop()
#
# @pytest.mark.asyncio
# async def test_start_browser(page_async):
#     # Обработчик для логов консоли
#     async def handle_console(msg):
#         print(f"[Console] {msg.type}: {msg.text}")
#         for arg in msg.args:
#             try:
#                 # Получить и вывести значение аргумента
#                 val = await arg.json_value()
#                 print(f"    Argument: {val}")
#             except:
#                 print("    Argument: [Could not retrieve JSON value]")
#
#     page_async.on("console", handle_console)
#
#     # Обработчик для сетевых запросов
#     async def handle_request(request):
#         print(f"[Request] {request.method} {request.url}")
#
#     async def handle_response(response):
#         print(f"[Response] {response.status} {response.url}")
#
#     page_async.on("request", handle_request)
#     page_async.on("response", handle_response)
#
#     # Можно также логировать другие события, например, ошибки страницы
#     async def handle_page_error(error):
#         print(f"[Page Error] {error}")
#
#     page_async.on("pageerror", handle_page_error)
#
#     await page_async.goto("https://stage-mgt.antisleep.ru/login")
#     await page_async.fill('#email', '123')
#     await page_async.fill('#password', '123')
#     await page_async.wait_for_selector('[type="submit"].btn', state='attached')
#     await page_async.click('[type="submit"].btn')

# import pytest
# import pytest_asyncio
# from playwright.async_api import async_playwright
#
# @pytest_asyncio.fixture(scope='session')
# async def playwright_async():
#     playwright_async = await async_playwright().start()
#     yield playwright_async
#     await playwright_async.stop()
#
# @pytest_asyncio.fixture(scope='session')
# async def browser_async(playwright_async, request):
#     browser = await playwright_async.chromium.launch(headless=False, args=None)
#     yield browser
#     await browser.close()
#
# @pytest_asyncio.fixture(scope="function")
# async def page_async(browser_async):
#     page = await browser_async.new_page()
#     yield page
#     await page.close()
#
# @pytest.mark.asyncio
# async def test_start_browser(page_async):
#     await page_async.goto("https://stage-mgt.antisleep.ru/login")
#     import time
#     time.sleep(5)
#     await page_async.fill('#email', '123')
#     await page_async.fill('#password', '123')
#     await page_async.wait_for_selector('[type="submit"].btn', state='attached')
#     await page_async.click('[type="submit"].btn')

@pytest.mark.asyncio
async def test_start_browser():
    browser = await async_playwright().start()
    browser = await browser.chromium.launch(headless=False, args=None)
    page = await browser.new_page()

    # Обработчик для логов консоли
    async def handle_console(msg):
        print(f"[Console] {msg.type}: {msg.text}")
        for arg in msg.args:
            try:
                # Получить и вывести значение аргумента
                val = await arg.json_value()
                print(f"    Argument: {val}")
            except:
                print("    Argument: [Could not retrieve JSON value]")

    page.on("console", handle_console)

    # Обработчик для сетевых запросов
    async def handle_request(request):
        print(f"[Request] {request.method} {request.url}")

    async def handle_response(response):
        print(f"[Response] {response.status} {response.url}")

    page.on("request", handle_request)
    page.on("response", handle_response)

    # Можно также логировать другие события, например, ошибки страницы
    async def handle_page_error(error):
        print(f"[Page Error] {error}")

    page.on("pageerror", handle_page_error)


    _ = await page.goto("https://stage-mgt.antisleep.ru/login")
    await page.fill('#email', '123')
    await page.fill('#password', '123')
    asd = 1
    # Rest of your code...

# Run the asynchronous function
# asyncio.run(start_browser())