import pytest
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage

class TestLogin:

    # Вход с валидными данными
    def test_valid_authorization(self, fresh_driver):
        driver = fresh_driver
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

    # Отправка пустой формы
    def test_empty_form(self, fresh_driver):
        driver = fresh_driver
        login_page = LoginPage(driver)
        login_page.click_login_button()

        news_title = login_page.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Авторизация")',
            timeout=10
        )
        assert news_title.is_displayed()

    # Проверка отправки формы с невалидными данными
    @pytest.mark.parametrize(
        "login, password",
        [
            # Оба поля невалидные
            ("incorrect", "incorrect"),
            # Поле login валидное, а поле password невалидное
            ("login2", "incorrect"),
            # Поле login невалидное, а поле password валидное
            ("incorrect", "password2"),
        ]
    )
    def test_invalid_credentials(self, fresh_driver, login, password):
        driver = fresh_driver
        login_page = LoginPage(driver)
        login_page.login(login=login, password=password)

        auth_title = login_page.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Авторизация")',
            timeout=10
        )
        assert auth_title.is_displayed()