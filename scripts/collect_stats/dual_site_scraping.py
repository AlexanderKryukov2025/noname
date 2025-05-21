import asyncio
from playwright.async_api import async_playwright
from pages.login_page import LoginPageAsync
from pages.main_page import MainPageAsync
from pages.device_page import DevicePageAsync
from settings import STG


async def launch_browser():
    p = await async_playwright().start()
    browser = await p.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()
    return p, browser, context, page


async def perform_login(login_page, host, login, password):
    await login_page.open_page(host)
    await login_page.verify_language()
    await login_page.enter_email(login)
    await login_page.enter_password(password)
    await login_page.click_submit()


async def main():
    # Запускаем два браузера параллельно
    p1, browser1, context1, page1 = await launch_browser()
    p2, browser2, context2, page2 = await launch_browser()

    # Создаём экземпляры страниц для каждого браузера
    login_page1 = LoginPageAsync(page1)
    login_page2 = LoginPageAsync(page2)
    main_page1 = MainPageAsync(page1)
    main_page2 = MainPageAsync(page2)
    device_page1 = DevicePageAsync(page1)
    device_page2 = DevicePageAsync(page2)

    # Запускаем логин для обоих браузеров параллельно
    login_tasks = [
        perform_login(
            login_page1,
            STG.MGT['host'],
            STG.MGT['login'],
            STG.MGT['password']
        ),
        perform_login(
            login_page2,
            STG.PILLIGRIMM['host'],
            STG.PILLIGRIMM['login'],
            STG.PILLIGRIMM['password']
        )
    ]
    await asyncio.gather(*login_tasks)

    await main_page1.check_landing()
    await main_page2.check_landing()

    await main_page1.navigate_to_devices()
    await main_page2.navigate_to_devices()

    await device_page1.check_landing()
    await device_page2.check_landing()

    await device_page1.switch_columns()
    await device_page2.switch_columns()

    await device_page1.close_popup()
    await device_page2.close_popup()

    await device_page1.press_export_excel()
    await device_page2.press_export_excel()

    await device_page1.wait_notification()
    await device_page2.wait_notification()

    await device_page1.press_download()
    await device_page2.press_download()

    # Можно оставить паузу, если нужно
    await asyncio.sleep(15)

    # Закрытие браузеров
    await browser1.close()
    await browser2.close()
    await p1.stop()
    await p2.stop()


# Запуск основного асинхронного метода
asyncio.run(main())
