from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
from datetime import datetime, timedelta
from selenium.common.exceptions import TimeoutException


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
    DELETE_NEWS_ITEM_BUTTON = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/delete_news_item_image_view"
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
    FILTER_NEWS_BUTTON = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/filter_news_material_button",
    )
    FILTER_BUTTON = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/filter_button",
    )
    FILTER_DATE_START = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/"
        "news_item_publish_date_start_text_input_edit_text",
    )
    FILTER_DATE_END = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/"
        "news_item_publish_date_end_text_input_edit_text",
    )
    EMPTY_CONTROL_PANEL = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/"
        "control_panel_empty_news_list_text_view",
    )
    FILTER_STATUS_ACTIVE = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/"
        "filter_news_active_material_check_box",
    )
    FILTER_STATUS_INACTIVE = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/"
        "filter_news_inactive_material_check_box",
    )
    NEWS_ITEM_TITLE = (
        AppiumBy.ID,
        "ru.iteco.fmhandroid:id/news_item_title_text_view",
    )
    MONTHS_RU = {
        1: "января", 2: "февраля", 3: "марта", 4: "апреля",
        5: "мая", 6: "июня", 7: "июля", 8: "августа",
        9: "сентября", 10: "октября", 11: "ноября", 12: "декабря",
    }

    def open_control_panel(self):
        # Переход в панель управления новостями (кнопка с карандашом)
        self.click(*self.EDIT_NEWS_BUTTON)

    def open_create_news_form(self):
        self.click(*self.ADD_NEWS_BUTTON)

    def open_filter(self):
        self.click(*self.FILTER_NEWS_BUTTON)

    def apply_filter(self):
        self.click(*self.FILTER_BUTTON)

    def sort_news(self):
        self.click(*self.SORT_NEWS_BUTTON)

    def set_filter_status(self, active, inactive):
        self._set_checkbox(self.FILTER_STATUS_ACTIVE, active)
        self._set_checkbox(self.FILTER_STATUS_INACTIVE, inactive)

    def _set_checkbox(self, locator, should_be_checked):
        el = self.find_element(*locator)
        checked = el.get_attribute("checked") == "true"
        if checked != should_be_checked:
            el.click()

    def select_filter_date(self, start=None, end=None):
        # End раньше Start: сначала End, иначе календарь уедет на завтра
        if start == "tomorrow" and end == "today":
            self._fill_filter_date(self.FILTER_DATE_END, "today")
            self._fill_filter_date(self.FILTER_DATE_START, "tomorrow")
            return
        if start is not None:
            self._fill_filter_date(self.FILTER_DATE_START, start)
        if end is not None:
            self._fill_filter_date(self.FILTER_DATE_END, end)

    def _date_content_desc(self, dt):
        return f"{dt.day:02d} {self.MONTHS_RU[dt.month]} {dt.year}"

    def _pick_calendar_day(self, dt=None):
        # Календарь уже открыт. dt=None → сегодня (только OK).
        if dt is not None:
            now = datetime.now()
            if (dt.year, dt.month) > (now.year, now.month):
                self.click(*self.NEXT_MONTH_BUTTON)
            self.click(
                AppiumBy.ACCESSIBILITY_ID,
                self._date_content_desc(dt),
            )
        self.click(*self.OK_BUTTON)

    def _fill_filter_date(self, field, day):
        self.click(*field)
        if day == "today":
            self._pick_calendar_day()
            return
        if day == "tomorrow":
            self._pick_calendar_day(datetime.now() + timedelta(days=1))
            return
        raise ValueError(f"Unsupported filter date: {day}")

    def select_filter_empty_period(self):
        # Один день в следующем месяце (Start и End). 6.8
        now = datetime.now()
        if now.month == 12:
            target = now.replace(year=now.year + 1, month=1, day=15)
        else:
            target = now.replace(month=now.month + 1, day=15)
        self.click(*self.FILTER_DATE_START)
        self._pick_calendar_day(target)
        self.click(*self.FILTER_DATE_END)
        self._pick_calendar_day()  # уже 15-е, только OK

    def is_control_panel_empty(self, timeout=10):
        try:
            el = self.find_element(
                *self.EMPTY_CONTROL_PANEL, timeout=timeout
            )
            return el.is_displayed()
        except TimeoutException:
            return False

    def select_filter_category(self, category):
        self.click(
            AppiumBy.ACCESSIBILITY_ID,
            "Показать раскрывающееся меню",
        )
        index = (
            "Объявление",
            "День рождения",
            "Зарплата",
            "Профсоюз",
            "Праздник",
            "Массаж",
            "Благодарность",
            "Нужна помощь",
        ).index(category)
        field = self.find_element(*self.CATEGORY_FIELD)
        rect = field.rect
        x = int(rect["x"] + rect["width"] / 2)
        row_h = int(rect["height"])
        y = int(rect["y"] + rect["height"] + row_h / 2 + index * row_h)
        self.driver.tap([(x, y)])

    def select_category(self, category):
        # Выбор категории на форме создания/редактирования
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
        self._pick_calendar_day()

    def select_tomorrow_date(self):
        # День в календаре: content-desc вида "13 августа 2026" (день с ведущим нулём)
        self.click(*self.DATE_FIELD)
        self._pick_calendar_day(datetime.now() + timedelta(days=1))

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

    def _register_title(self, title):
        titles = getattr(self.driver, "owned_titles", None)
        if titles is not None and title and title not in titles:
            titles.append(title)

    def _replace_title(self, old, new):
        titles = getattr(self.driver, "owned_titles", None)
        if titles is None or not new:
            return
        if old in titles:
            titles[titles.index(old)] = new
        elif new not in titles:
            titles.append(new)

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
        self._last_title = title
        self._register_title(title)
        # Возвращает (title, description) для ассертов
        return title, description

    def _scroll_to_title(self, title):
        title_locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiScrollable(new UiSelector().scrollable(true))'
            '.scrollIntoView(new UiSelector()'
            '.resourceId("ru.iteco.fmhandroid:id/news_item_title_text_view")'
            f'.text("{title}"))'
        )
        return self.find_element(*title_locator)

    def _find_title_visible(self, title):
        return self.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector()'
            '.resourceId("ru.iteco.fmhandroid:id/news_item_title_text_view")'
            f'.text("{title}")'
        )

    def _elements_below_title(self, title_el, locator):
        title_y = title_el.location["y"]
        below = [
            el for el in self.driver.find_elements(*locator)
            if el.is_displayed() and el.location["y"] > title_y
        ]
        below.sort(key=lambda el: el.location["y"])
        return below

    def _element_below_title(self, title, locator):
        # scrollIntoView ставит title вниз экрана — корзина/карандаш ниже не видны
        title_el = self._scroll_to_title(title)
        for _ in range(3):
            below = self._elements_below_title(title_el, locator)
            if below:
                return below[0]
            size = self.driver.get_window_size()
            self.driver.swipe(
                size["width"] // 2,
                int(size["height"] * 0.65),
                size["width"] // 2,
                int(size["height"] * 0.35),
                400,
            )
            title_el = self._find_title_visible(title)
        return self._elements_below_title(title_el, locator)[0]

    def open_edit_news_form(self, title):
        self._element_below_title(title, self.EDIT_NEWS_ITEM_BUTTON).click()

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
        return self._element_below_title(title, self.NEWS_ITEM_STATUS).text

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
            old = getattr(self, "_last_title", None)
            title = self.fill_title(title)
            self._replace_title(old, title)
            self._last_title = title
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

    def delete_news(self, title):
        self._element_below_title(title, self.DELETE_NEWS_ITEM_BUTTON).click()
        self.click(*self.OK_BUTTON)
        titles = getattr(self.driver, "owned_titles", None)
        if titles and title in titles:
            titles.remove(title)

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
        try:
            title_el = self.find_element(*title_locator, timeout=timeout)
        except TimeoutException:
            return False
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

    def get_titles_order(self, titles, max_swipes=40):
        # Порядок своих заголовков сверху вниз (чужие пропускаем).
        wanted = set(titles)
        seen = []
        self.find_element(*self.NEWS_ITEM_TITLE)
        for _ in range(max_swipes + 1):
            els = self.driver.find_elements(*self.NEWS_ITEM_TITLE)
            for el in sorted(els, key=lambda e: e.location["y"]):
                text = el.text
                if text in wanted and text not in seen:
                    seen.append(text)
                    if len(seen) == len(wanted):
                        return seen
            try:
                self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiScrollable(new UiSelector()'
                    '.scrollable(true)).scrollForward()',
                )
            except Exception:
                break
        return seen
