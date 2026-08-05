import pytest
from appium.webdriver.common.appiumby import AppiumBy
import allure
from pages.login_page import LoginPage


@allure.epic("Мобильный хоспис")
@allure.feature("Авторизация")
class TestLogin:

    # Вход с валидными данными
    @allure.id("1.1")
    @allure.title("Вход с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Позитивные сценарии")
    def test_valid_authorization(self, fresh_driver):
        driver = fresh_driver
        login_page = LoginPage(driver)
        with allure.step("Авторизоваться валидными данными"):
            login_page.login(login="login2", password="password2")
        with allure.step("Проверить переход на главный экран"):
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
    @allure.id("1.6")
    @allure.title("Отправка пустой формы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
    def test_empty_form(self, fresh_driver):
        driver = fresh_driver
        login_page = LoginPage(driver)
        with allure.step("Кликнуть на кнопку «Войти» без ввода данных в поля авторизации"):
            login_page.click_login_button()

        with allure.step("Проверить, что остались на экране «Авторизация»"):
            news_title = login_page.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Авторизация")',
                timeout=10
            )
            assert news_title.is_displayed()

        with allure.step("Проверить сообщение: логин и пароль не могут быть пустыми"):
            toast_text = login_page.get_toast_message(timeout=5)
            assert "Логин и пароль не могут быть пустыми" in toast_text

    # Проверка отправки формы с невалидными данными
    @allure.id("1.3-1.5")
    @allure.title("Вход с невалидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
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

        with allure.step("Авторизоваться с невалидными данными"):
            login_page.login(login=login, password=password)

        with allure.step("Проверить, что остались на экране «Авторизация»"):
            auth_title = login_page.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Авторизация")',
                timeout=10
            )
            assert auth_title.is_displayed()

        with allure.step("Проверить сообщение об ошибке авторизации"):
            toast_text = login_page.get_toast_message(timeout=5)
            assert expected_message in toast_text

    # Обработка множественных нажатий на кнопку входа
    @allure.id("1.2")
    @allure.title("Обработка множественных нажатий на кнопку входа")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    def test_multiple_login_clicks(self, fresh_driver):
        login_page = LoginPage(fresh_driver)

        with allure.step("Заполнить валидные логин и пароль"):
            login_page.send_keys(*login_page.LOGIN_FIELD, "login2")
            login_page.send_keys(*login_page.PASSWORD_FIELD, "password2")

        # После клика по кнопке (использовать локатор, а не координаты)
        # кнопка блокируется и повторно кликнуть не удается
        with allure.step("Быстро нажать «Войти» 3 раза"):
            login_page.tap_login_button_multiple_times(3)

        with allure.step("Проверить успешный вход на главный экран"):
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
    @allure.id("1.7")
    @allure.title("Сохранение сессии после перезапуска приложения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Сессия")
    def test_save_session_after_restart(self, fresh_driver):
        driver = fresh_driver
        login_page = LoginPage(driver)
        app_package = "ru.iteco.fmhandroid"

        with allure.step("Авторизоваться с валидными данными"):
            login_page.login(login="login2", password="password2")

        with allure.step("Проверить успешную авторизацию"):
            news_title = login_page.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Новости")',
                timeout=10
            )
            assert news_title.is_displayed()

        with allure.step("Перезапустить приложение"):
            driver.terminate_app(app_package)
            driver.activate_app(app_package)

        with allure.step("Проверить, что сессия сохранилась"):
            news_title_after_restart = login_page.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().text("Новости")',
                timeout=10
            )
            assert news_title_after_restart.is_displayed()
