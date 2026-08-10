from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from datetime import datetime, timedelta


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
    CANCEL_BUTTON = (AppiumBy.ID, "android:id/button2")
    NEXT_MONTH_BUTTON = (
        AppiumBy.ID,
        "android:id/next"
    )
    TIME_TOGGLE_MODE = (AppiumBy.ID, "android:id/toggle_mode")
    TIME_INPUT_HOUR = (AppiumBy.ID, "android:id/input_hour")
    TIME_INPUT_MINUTE = (AppiumBy.ID, "android:id/input_minute")

    def open_control_panel(self):
        # Переход в панель управления новостями (кнопка с карандашом)
        self.click(*self.EDIT_NEWS_BUTTON)

    def open_create_news_form(self):
        self.click(*self.ADD_NEWS_BUTTON)

    def select_category(self, category):
        # Выбор категории
        self.click(*self.CATEGORY_FIELD)
        self.send_keys(*self.CATEGORY_FIELD, category)
        category_option = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{category}")'
        )
        self.click(*category_option)

    def fill_title(self, title):
        # Ввод заголовка
        self.send_keys(*self.TITLE_FIELD, title)

    def select_today_date(self):
        # Открыть календарь и подтвердить текущую дату
        self.click(*self.DATE_FIELD)
        self.click(*self.OK_BUTTON)


    def select_current_time(self):
        # Открыть время и подтвердить текущее время
        self.click(*self.TIME_FIELD)
        self.click(*self.OK_BUTTON)

    def set_time_via_keyboard(self, hour, minute):
        # Открыть время → режим клавиатуры → ввести час и минуту → OK
        self.click(*self.TIME_FIELD)
        self.click(*self.TIME_TOGGLE_MODE)
        self.send_keys(*self.TIME_INPUT_HOUR, f"{hour:02d}")
        self.send_keys(*self.TIME_INPUT_MINUTE, f"{minute:02d}")
        self.click(*self.OK_BUTTON)

    def fill_description(self, description):
        # Ввод описания новости
        self.send_keys(*self.DESCRIPTION_FIELD, description)

    def save_news(self):
        # Клик на кнопку Сохранить
        self.click(*self.SAVE_BUTTON)

    def create_news(self, category, title, description, time_offset_minutes=1):
        # Полное заполнение формы и сохранение(для позитивных сценариев)
        self.select_category(category)
        self.fill_title(title)
        self.select_today_date()
        target = datetime.now() + timedelta(minutes=time_offset_minutes)
        self.set_time_via_keyboard(target.hour, target.minute)
        self.fill_description(description)
        self.save_news()

    def is_news_in_control_panel(self, title, timeout=10):
        # Поиск новости в панели управления по заголовку
        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector()'
            '.resourceId("ru.iteco.fmhandroid:id/news_item_title_text_view")'
            f'.text("{title}")'
        )
        element = self.find_element(*locator, timeout=timeout)
        return element.is_displayed()
