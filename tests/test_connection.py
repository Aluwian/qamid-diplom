import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


def test_app_launches():
    """Тест: приложение успешно запускается"""
    options = UiAutomator2Options()
    options.platform_name = 'Android'
    options.device_name = 'Pixel_4_API_29'  # ← Имя вашего эмулятора
    options.app_package = 'ru.iteco.fmhandroid'
    options.app_activity = '.ui.AppActivity'
    options.automation_name = 'UiAutomator2'
    options.no_reset = True  # Не сбрасывать данные приложения

    driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)

    # Проверяем, что приложение запустилось
    assert driver.current_activity is not None

    driver.quit()