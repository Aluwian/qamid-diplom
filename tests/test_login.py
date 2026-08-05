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
    def test_invalid_credentials(
            self,
            fresh_driver,
            login,
            password,
            expected_message
    ):
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

    # Обработка множественных нажатий на кнопку входа
    def test_multiple_login_clicks(self, fresh_driver):
        login_page = LoginPage(fresh_driver)

        login_page.send_keys(*login_page.LOGIN_FIELD, "login2")
        login_page.send_keys(*login_page.PASSWORD_FIELD, "password2")

        # После клика по кнопке (использовать локатор, а не координаты)
        # кнопка блокируется и повторно кликнуть не удается
        login_page.tap_login_button_multiple_times(3)

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

    # Сохранение сессии после перезапуска приложения
    def test_save_session_after_restart(self, fresh_driver):
        driver = fresh_driver
        login_page = LoginPage(driver)
        app_package = "ru.iteco.fmhandroid"

        # Авторизация
        login_page.login(login="login2", password="password2")

        # Проверка того, что авторизация прошла успешно
        news_title = login_page.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Новости")',
            timeout=10
        )
        assert news_title.is_displayed()

        # Выключаем приложение и запускаем его вновь
        driver.terminate_app(app_package)
        driver.activate_app(app_package)

        # Проверка сохранения сесиии после перезагрузки
        news_title_after_restart = login_page.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Новости")',
            timeout=10
        )
        assert news_title_after_restart.is_displayed()
