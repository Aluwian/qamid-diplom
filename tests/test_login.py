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

        toast_text = login_page.get_toast_message(timeout=5)
        assert "Логин и пароль не могут быть пустыми" in toast_text

    # Проверка отправки формы с невалидными данными
    @pytest.mark.parametrize(
        "login, password, expected_message",
        [
            # Оба поля невалидные
            ("incorrect", "incorrect", "Что-то пошло не так. Попробуйте позднее."),
            # Поле login валидное, а поле password невалидное
            ("login2", "incorrect", "Что-то пошло не так. Попробуйте позднее."),
            # Поле login невалидное, а поле password валидное
            ("incorrect", "password2", "Что-то пошло не так. Попробуйте позднее."),
        ]
    )
    def test_invalid_credentials(self, fresh_driver, login, password, expected_message):
        driver = fresh_driver
        login_page = LoginPage(driver)
        login_page.login(login=login, password=password)

        auth_title = login_page.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Авторизация")',
            timeout=10
        )
        assert auth_title.is_displayed()

        toast_text = login_page.get_toast_message(timeout=5)
        assert expected_message in toast_text