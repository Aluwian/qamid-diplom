from appium import webdriver
from appium.options.android import UiAutomator2Options
import pytest
from pages.login_page import LoginPage

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'
APP_PACKAGE = "ru.iteco.fmhandroid"

# 1. Базовый драйвер для быстрых тестов (CRUD), где состояние не важно или мы управляем им вручную
@pytest.fixture(scope='function')
def create_android_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android"
    options.app_package = APP_PACKAGE
    options.app_activity = ".ui.AppActivity"
    options.no_reset = True

    driver = webdriver.Remote(
        command_executor=f'http://{APPIUM_HOST}:{APPIUM_PORT}',
        options=options
    )
    yield driver
    driver.quit()


# 2. "Свежий" драйвер специально для тестов АВТОРИЗАЦИИ
@pytest.fixture(scope="function")
def fresh_driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android"
    options.app_package = APP_PACKAGE
    options.app_activity = ".ui.AppActivity"
    options.no_reset = False

    driver = webdriver.Remote(
        command_executor=f'http://{APPIUM_HOST}:{APPIUM_PORT}',
        options=options
    )
    yield driver
    driver.quit()


# 3. Драйвер с уже выполненной авторизацией (для CRUD тестов)
@pytest.fixture(scope="function")
def authorized_driver(create_android_driver):
    driver = create_android_driver

    driver.terminate_app(APP_PACKAGE)
    driver.activate_app(APP_PACKAGE)

    login_page = LoginPage(driver)
    login_page.login(login="login2", password="password2")

    yield driver

    driver.terminate_app(APP_PACKAGE)