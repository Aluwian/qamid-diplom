from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class MainPage(BasePage):
    MAIN_MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Главное меню")
    NEWS_MENU_ITEM = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Новости")'
    )
    MAIN_MENU_ITEM = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Главная")'
    )
    ABOUT_MENU_ITEM = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("О приложении")'
    )
    QUOTES_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Наша Миссия")
    ALL_NEWS_TEXT = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/all_news_text_view",
    )
    ABOUT_VERSION = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/about_version_title_text_view",
    )
    QUOTES_TITLE = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/our_mission_title_text_view",
    )
    AUTH_BUTTON = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/authorization_image_button",
    )
    LOGOUT_MENU_ITEM = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Выйти")',
    )

    def logout(self):
        self.click(*self.AUTH_BUTTON)
        self.click(*self.LOGOUT_MENU_ITEM)

    def go_to_news(self):
        self.click(*self.MAIN_MENU_BUTTON)
        self.click(*self.NEWS_MENU_ITEM)

    def go_to_main(self):
        self.click(*self.MAIN_MENU_BUTTON)
        self.click(*self.MAIN_MENU_ITEM)

    def go_to_about(self):
        self.click(*self.MAIN_MENU_BUTTON)
        self.click(*self.ABOUT_MENU_ITEM)

    def go_to_quotes(self):
        self.click(*self.QUOTES_BUTTON)

    def go_back(self):
        self.driver.press_keycode(4)
