from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Логин")'
    )
    PASSWORD_FIELD = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Пароль")'
    )
    LOGIN_BUTTON = (AppiumBy.ID, "ru.iteco.fmhandroid:id/enter_button")
    TOAST_MESSAGE = (AppiumBy.XPATH, "//android.widget.Toast")

    def login(self, login, password):
        # Авторизация
        self.send_keys(*self.LOGIN_FIELD, login)
        self.send_keys(*self.PASSWORD_FIELD, password)
        self.click(*self.LOGIN_BUTTON)

    def click_login_button(self):
        self.click(*self.LOGIN_BUTTON)
