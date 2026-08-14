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
    SAVE_BUTTON = (AppiumBy.ID, "ru.iteco.fmhandroid:id/save_button")
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
    SORT_NEWS_BUTTON = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/sort_news_material_button",
    )
    VIEW_NEWS_ITEM = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/view_news_item_image_view",
    )

    EDIT_NEWS_ITEM_BUTTON = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/edit_news_item_image_view"
    )
    NEWS_ITEM_CARD = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/news_item_material_card_view"
    )
    NEWS_ITEM_STATUS = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/news_item_published_text_view"
    )

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

    def fill_title(self, title=None, prefix="Автотест"):
        # title=None → уникальный заголовок: Автотест_ЧЧММСС
        # title передан → пишем как есть (для валидации: "A", "A"*100 и т.д.)
        if title is None:
            title = f"{prefix}_{datetime.now().strftime('%H%M%S')}"
        self.send_keys(*self.TITLE_FIELD, title)
        return title

    def select_today_date(self):
        # Открыть календарь и подтвердить текущую дату
        self.click(*self.DATE_FIELD)
        self.click(*self.OK_BUTTON)

    def select_tomorrow_date(self):
        # День в календаре: content-desc вида "13 августа 2026" (день с ведущим нулём)
        tomorrow = datetime.now() + timedelta(days=1)
        months_ru = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля",
            5: "мая", 6: "июня", 7: "июля", 8: "августа",
            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря",
        }
        date_label = (
            f"{tomorrow.day:02d} {months_ru[tomorrow.month]} {tomorrow.year}"
        )
        self.click(*self.DATE_FIELD)
        if tomorrow.day == 1:
            self.click(*self.NEXT_MONTH_BUTTON)
        self.click(AppiumBy.ACCESSIBILITY_ID, date_label)
        self.click(*self.OK_BUTTON)

    def select_date(self, date="today"):
        if date == "today":
            self.select_today_date()
        elif date == "tomorrow":
            self.select_tomorrow_date()
        else:
            raise ValueError(f"Unsupported date: {date}")

    def select_current_time(self):
        # Открыть время и подтвердить текущее время
        self.click(*self.TIME_FIELD)
        self.click(*self.OK_BUTTON)

    def set_time_via_keyboard(self, hour, minute):
        # Открыть время → клавиатура → час/минута → OK
        self.click(*self.TIME_FIELD)
        self.click(*self.TIME_TOGGLE_MODE)
        self.send_keys(*self.TIME_INPUT_HOUR, f"{hour:02d}")
        self.send_keys(*self.TIME_INPUT_MINUTE, f"{minute:02d}")
        self.click(*self.OK_BUTTON)

    def select_time(self, options=None):
        # options:
        #   {"type": "auto"}                         → текущее через OK
        #   {"type": "keyboard", "offset": 0}          → текущее с клавиатуры (2.25)
        #   {"type": "keyboard", "offset": 1}          → +1 мин (2.28)
        #   {"type": "keyboard", "hour": 10, "minute": 30}  → точное время
        options = options or {"type": "auto"}
        kind = options["type"]

        if kind == "auto":
            self.select_current_time()
            return

        if kind == "keyboard":
            if "hour" in options and "minute" in options:
                hour, minute = options["hour"], options["minute"]
            else:
                offset = options.get("offset", 0)
                target = datetime.now() + timedelta(minutes=offset)
                hour, minute = target.hour, target.minute
            self.set_time_via_keyboard(hour, minute)
            return

        raise ValueError(f"Unsupported time options: {options}")

    def fill_description(self, description=None, prefix="Описание автотеста"):
        # description=None → всегда уникальное: Описание автотеста_ЧЧММСС
        # description передан → пишем как есть (негативы и т.п.)
        if description is None:
            description = f"{prefix}_{datetime.now().strftime('%H%M%S')}"
        self.send_keys(*self.DESCRIPTION_FIELD, description)
        return description

    def clear_field(self, by, value):
        element = self.find_element(by, value)
        element.clear()

    def save_news(self):
        # После описания клавиатура/разросшееся поле прячут кнопку —
        # закрываем клавиатуру и скроллим к Save по resource-id.
        try:
            self.driver.hide_keyboard()
        except Exception:
            try:
                self.driver.press_keycode(4)  # BACK
            except Exception:
                pass
        save_in_scroll = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector()'
            '.resourceId("ru.iteco.fmhandroid:id/save_button"))',
        )
        self.click(*save_in_scroll)

    # Заполняет форму создания новости и нажимает «Сохранить»
    def create_news(
            self,
            category="Объявление",
            title=None,
            description=None,
            date="today",
            time=None,
    ):
        # category — по умолчанию «Объявление»
        self.select_category(category)
        # title — если не передать, подставятся уникальные
        title = self.fill_title(title)
        # date — по умолчанию сегодня
        self.select_date(date)
        # time — словарь для select_time; если не передать, берётся текущее время (auto)
        self.select_time(time)
        # description — если не передать, подставятся уникальные
        description = self.fill_description(description)
        self.save_news()
        # Возвращает (title, description) для ассертов
        return title, description

    def open_edit_news_form(self, title):
        title_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector()'
            '.resourceId("ru.iteco.fmhandroid:id/news_item_title_text_view")'
            f'.text("{title}"))'
        )
        title_el = self.find_element(*title_locator)
        title_y = title_el.location["y"]
        edits = self.driver.find_elements(*self.EDIT_NEWS_ITEM_BUTTON)
        below = [
            el for el in edits
            if el.is_displayed() and el.location["y"] > title_y
        ]
        below.sort(key=lambda el: el.location["y"])
        below[0].click()

    def set_status(self, active):
        switcher_in_scroll = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector()'
            '.resourceId("ru.iteco.fmhandroid:id/switcher"))',
        )
        el = self.find_element(*switcher_in_scroll)
        checked = el.get_attribute("checked") == "true"
        if checked != active:
            el.click()

    def get_news_status(self, title):
        card = self._card_by_title(title)
        return card.find_element(*self.NEWS_ITEM_STATUS).text

    def update_news(
            self,
            category=None,
            title=None,
            description=None,
            date=None,
            time=None,
            active=None,
    ):
        # Меняет только переданное; остальное не трогает (поля уже заполнены)
        if category is not None:
            self.select_category(category)
        if title is not None:
            title = self.fill_title(title)
        if date is not None:
            self.select_date(date)
        if time is not None:
            self.select_time(time)
        if description is not None:
            description = self.fill_description(description)
        if active is not None:
            self.set_status(active)
        self.save_news()
        return title, description

    def is_news_in_control_panel(self, title, description=None, timeout=10):
        # Скролл к новости по заголовку.
        # description=None → достаточно найти title (простой create, 2.2).
        # description передан → раскрываем карточку и сверяем описание (валидация).
        title_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector()'
            '.resourceId("ru.iteco.fmhandroid:id/news_item_title_text_view")'
            f'.text("{title}"))'
        )
        title_el = self.find_element(*title_locator, timeout=timeout)
        if not title_el.is_displayed():
            return False

        if description is None:
            return True

        self.click(*self.VIEW_NEWS_ITEM)
        desc_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector()'
            '.resourceId("ru.iteco.fmhandroid:id/news_item_description_text_view")'
            f'.text("{description}")'
        )
        desc_el = self.find_element(*desc_locator, timeout=timeout)
        return desc_el.is_displayed()
