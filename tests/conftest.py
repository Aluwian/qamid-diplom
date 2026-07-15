from appium import webdriver
from appium.options.android import UiAutomator2Options
import pytest

APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'

@pytest.fixture(scope='session')
def create_android_driver():
    options = UiAutomator2Options()

    # Новый синтаксис (через свойства, а не методы set_*)
    options.platform_name = "Android"
    options.device_name = "Android"
    options.app_package = "ru.iteco.fmhandroid"
    options.app_activity = ".ui.AppActivity"
    options.auto_grant_permissions = True

    driver = webdriver.Remote(
        command_executor=f'http://{APPIUM_HOST}:{APPIUM_PORT}',
        options=options
    )

    yield driver

    driver.quit()