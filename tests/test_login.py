import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage

class TestLogin:

    # 1.1 Авторизация. Вход с валидными данными
    def test_valid_authorization(self, create_android_driver):
        driver = create_android_driver
        login_page = LoginPage(driver)
        login_page.login(login="login2", password="password2")
        news_title = login_page.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Новости")',
            timeout=10
        )
        assert news_title.is_displayed()
        mission_button = login_page.find_element(
            AppiumBy.ACCESSIBILITY_ID, "Наша Миссия", timeout=10
        )
        assert mission_button.is_displayed()
        # driver.reset()