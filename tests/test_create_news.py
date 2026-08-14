import pytest
from datetime import datetime
import allure


@allure.epic("Мобильный хоспис")
@allure.feature("Создание новостей")
class TestCreateNews:
    @allure.id("2.2")
    @allure.title("Создание новости с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Позитивные сценарии")
    def test_create_news_valid(self, create_news_form):
        news_page = create_news_form
        with allure.step("Заполнить форму и сохранить"):
            title, _ = news_page.create_news(
                time={"type": "keyboard", "offset": 1},
            )
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("2.1")
    @allure.title("Отправка пустой формы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
    def test_create_news_empty_form(self, create_news_form):
        news_page = create_news_form
        with allure.step("Кликнуть кнопку Сохранить без заполнения полей"):
            news_page.save_news()
        with allure.step("Проверить toast об ошибке"):
            toast = news_page.get_toast_message(timeout=5)
            assert "Заполните пустые поля" in toast

    @allure.id("2.3")
    @allure.title("Сохранение формы без выбора категории")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
    def test_create_news_without_category(self, create_news_form):
        news_page = create_news_form
        title = f"Автотест_{datetime.now().strftime('%H%M%S')}"
        with allure.step("Заполнить все поля, кроме категории"):
            news_page.fill_title(title)
            news_page.select_today_date()
            news_page.select_current_time()
            news_page.fill_description("Описание автотеста")
        with allure.step("Кликнуть Сохранить без категории"):
            news_page.save_news()
        with allure.step("Проверить toast об ошибке"):
            toast = news_page.get_toast_message(timeout=5)
            assert "Заполните пустые поля" in toast

    @allure.id("2.4-2.7, 2.10-2.12")
    @allure.title("Валидация заголовка: валидные значения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    @pytest.mark.parametrize(
        "title",
        [
            "AutotestValidationTitle",      # 2.4 латиница
            "АвтотестВалидацияЗаголовка",  # 2.5 кириллица
            "1234567890",         # 2.6 цифры
            "!@#$%^&*()",         # 2.7 символы
            "A",                  # 2.10 один символ
            "A" * 100,            # 2.11 максимум 100
            "A" * 99,             # 2.12 максимум - 1
        ],
    )
    def test_create_news_title_validation(self, create_news_form, title):
        news_page = create_news_form
        with allure.step("Заполнить форму с проверяемым заголовком и сохранить"):
            title, _ = news_page.create_news(title=title)
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("2.8-2.9")
    @allure.title("Отправка пустого или пробельного заголовка")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
    @pytest.mark.parametrize(
        "title",
        [
            " ",  # 2.8 пробел
            "",   # 2.9 пустое поле
        ],
    )
    def test_create_news_title_empty(self, create_news_form, title):
        news_page = create_news_form
        with allure.step("Заполнить все поля, кроме валидного заголовка"):
            news_page.select_category("Объявление")
            if title:
                news_page.fill_title(title)
            news_page.select_today_date()
            news_page.select_current_time()
            news_page.fill_description("Описание автотеста")
        with allure.step("Сохранить с пустым или пробельным заголовком"):
            news_page.save_news()
        with allure.step("Проверить toast об ошибке"):
            toast = news_page.get_toast_message(timeout=5)
            assert "Заполните пустые поля" in toast

    @allure.id("2.25, 2.28")
    @allure.title("Валидация времени: ручной ввод (сегодня)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    @pytest.mark.parametrize(
        "time_options",
        [
            {"type": "keyboard", "offset": 0},  # 2.25 текущее
            {"type": "keyboard", "offset": 1},  # 2.28 +1 мин
        ],
        ids=["2.25_current", "2.28_plus_1min"],
    )
    def test_create_news_time_keyboard_today(self, create_news_form, time_options):
        news_page = create_news_form
        with allure.step("Создать новость с временем через клавиатуру"):
            title, _ = news_page.create_news(time=time_options)
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("2.29")
    @allure.title("При дате «Завтра» время раньше текущего на часах принимается")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    def test_create_news_time_before_now_with_tomorrow(self, create_news_form):
        news_page = create_news_form
        with allure.step("Создать новость: завтра + время раньше текущего на часах"):
            title, _ = news_page.create_news(
                date="tomorrow",
                time={"type": "keyboard", "offset": -60},
            )
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("2.30-2.33, 2.36-2.38")
    @allure.title("Валидация описания: валидные значения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    @pytest.mark.parametrize(
        "description",
        [
            "AutotestValidationDescription",  # 2.30 латиница
            "ОписаниеАвтотестаВалидация",     # 2.31 кириллица
            "1234567890",                     # 2.32 цифры
            "!@#$%^&*()",                     # 2.33 символы
            "A",                              # 2.36 один символ
            "A" * 1000,                       # 2.37 максимум 1000
            "A" * 999,                        # 2.38 максимум - 1
        ],
    )
    def test_create_news_description_validation(self, create_news_form, description):
        news_page = create_news_form
        with allure.step("Заполнить форму с проверяемым описанием и сохранить"):
            title, _ = news_page.create_news(description=description)
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("2.34-2.35")
    @allure.title("Отправка пустого или пробельного описания")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
    @pytest.mark.parametrize(
        "description",
        [
            " ",  # 2.34 пробел
            "",   # 2.35 пустое поле
        ],
    )
    def test_create_news_description_empty(self, create_news_form, description):
        news_page = create_news_form
        with allure.step("Заполнить все поля, кроме валидного описания"):
            news_page.select_category("Объявление")
            news_page.fill_title()
            news_page.select_today_date()
            news_page.select_current_time()
            if description:
                news_page.fill_description(description)
        with allure.step("Сохранить с пустым или пробельным описанием"):
            news_page.save_news()
        with allure.step("Проверить toast об ошибке"):
            toast = news_page.get_toast_message(timeout=5)
            assert "Заполните пустые поля" in toast