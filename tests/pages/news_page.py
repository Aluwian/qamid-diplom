from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class NewsPage(BasePage):
    CATEGORY_FIELD = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/news_item_category_text_auto_complete_text_view"
    )
    TITLE_FIELD = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/news_item_title_text_input_edit_text"
    )
    DESCRIPTION_FIELD = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/news_item_description_text_input_edit_text"
    )
    DATE_FIELD = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/news_item_publish_date_text_input_edit_text"
    )
    TIME_FIELD = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/news_item_publish_time_text_input_edit_text"
    )
    SAVE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Сохранить")
    EDIT_NEWS_BUTTON = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/edit_news_material_button"
    )
    ADD_NEWS_BUTTON = (
        AppiumBy.ACCESSIBILITY_ID,
        "Кнопка добавления новости"
    )
    ACTIVE_SWITCHER = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/switcher"
    )
    OK_BUTTON = (AppiumBy.ID, "android:id/button1")

    def open_control_panel(self):
        # Переход в панель управления новостями (кнопка с карандашом)
        self.click(*self.EDIT_NEWS_BUTTON)
