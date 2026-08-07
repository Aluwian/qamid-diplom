from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class MainPage(BasePage):
    MAIN_MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Главное меню")
    NEWS_MENU_ITEM = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("Новости")'
    )

    def go_to_news(self):
        self.click(*self.MAIN_MENU_BUTTON)
        self.click(*self.NEWS_MENU_ITEM)
