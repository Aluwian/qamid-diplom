from appium import webdriver
from appium.options.android import UiAutomator2Options
import pytest
from pages.login_page import LoginPage

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'
APP_PACKAGE = "ru.iteco.fmhandroid"

# 1. Создание драйвера с нужными настройками
def create_driver(no_reset=True):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android"
    options.app_package = APP_PACKAGE
    options.app_activity = ".ui.AppActivity"
    options.no_reset = no_reset

    driver = webdriver.Remote(
        command_executor=f'http://{APPIUM_HOST}:{APPIUM_PORT}',
        options=options
    )
    return driver

# 2. Базовый драйвер(для быстрого старта, сохраняется состояние)
@pytest.fixture(scope='function')
def android_driver():
    driver = create_driver(no_reset=True)
    yield driver
    driver.quit()

# 3. "Свежий" драйвер специально для тестов АВТОРИЗАЦИИ(чистый старт без авторизации, состояние не сохраняется)
@pytest.fixture(scope="function")
def fresh_driver():
    driver = create_driver(no_reset=False)
    yield driver
    driver.quit()


# 3. Драйвер с уже выполненной авторизацией (для CRUD тестов)
@pytest.fixture(scope="function")
def authorized_driver(android_driver):
    driver = android_driver

    driver.terminate_app(APP_PACKAGE)
    driver.activate_app(APP_PACKAGE)

    login_page = LoginPage(driver)
    login_page.login(login="login2", password="password2")

    yield driver

    driver.terminate_app(APP_PACKAGE)