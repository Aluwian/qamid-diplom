from datetime import datetime
import allure
import pytest


@allure.epic("Мобильный хоспис")
@allure.feature("Редактирование новостей")
class TestUpdateNews:
    @allure.id("3.2")
    @allure.title("Редактирование новости с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Позитивные сценарии")
    def test_update_news_valid(self, edit_news_form):
        news_page, _, _ = edit_news_form
        with allure.step("Изменить заголовок и сохранить"):
            new_title, _ = news_page.update_news(
                title=f"Редакт_{datetime.now().strftime('%H%M%S')}",
            )
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(new_title)

    @allure.id("3.1")
    @allure.title("Отправка пустой формы")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
    def test_update_news_empty_form(self, edit_news_form):
        news_page, _, _ = edit_news_form
        with allure.step("Очистить все обязательные поля"):
            news_page.clear_field(*news_page.CATEGORY_FIELD)
            news_page.clear_field(*news_page.TITLE_FIELD)
            news_page.clear_field(*news_page.DATE_FIELD)
            news_page.clear_field(*news_page.TIME_FIELD)
            news_page.clear_field(*news_page.DESCRIPTION_FIELD)
        with allure.step("Кликнуть Сохранить"):
            news_page.save_news()
        with allure.step("Проверить toast об ошибке"):
            toast = news_page.get_toast_message(timeout=5)
            assert "Заполните пустые поля" in toast

    @allure.id("3.3")
    @allure.title("Сохранение формы без выбора категории")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
    def test_update_news_without_category(self, edit_news_form):
        news_page, _, _ = edit_news_form
        with allure.step("Очистить поле Категория"):
            news_page.clear_field(*news_page.CATEGORY_FIELD)
        with allure.step("Кликнуть Сохранить"):
            news_page.save_news()
        with allure.step("Проверить toast об ошибке"):
            toast = news_page.get_toast_message(timeout=5)
            assert "Заполните пустые поля" in toast

    @allure.id("3.4-3.7, 3.10-3.12")
    @allure.title("Валидация заголовка: валидные значения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    @pytest.mark.parametrize(
        "title",
        [
            "AutotestUpdateTitle",           # 3.4 латиница
            "АвтотестРедактированиеЗаголовка",  # 3.5 кириллица
            "9876543210",                    # 3.6 цифры
            "!@#$%^&*()",                    # 3.7 символы
            "B",                             # 3.10 один символ
            "B" * 100,                       # 3.11 максимум 100
            "B" * 99,                        # 3.12 максимум - 1
        ],
    )
    def test_update_news_title_validation(self, edit_news_form, title):
        news_page, _, _ = edit_news_form
        with allure.step("Изменить заголовок на проверяемое значение и сохранить"):
            title, _ = news_page.update_news(title=title)
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("3.8-3.9")
    @allure.title("Отправка пустого или пробельного заголовка")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
    @pytest.mark.parametrize(
        "title",
        [
            " ",  # 3.8 пробел
            "",   # 3.9 пустое поле
        ],
    )
    def test_update_news_title_empty(self, edit_news_form, title):
        news_page, _, _ = edit_news_form
        with allure.step("Очистить заголовок; при пробеле ввести пробел"):
            if title:
                news_page.fill_title(title)
            else:
                news_page.clear_field(*news_page.TITLE_FIELD)
        with allure.step("Сохранить с пустым или пробельным заголовком"):
            news_page.save_news()
        with allure.step("Проверить toast об ошибке"):
            toast = news_page.get_toast_message(timeout=5)
            assert "Заполните пустые поля" in toast

    @allure.id("3.26, 3.29")
    @allure.title("Валидация времени: ручной ввод (сегодня)")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    @pytest.mark.parametrize(
        "time_options",
        [
            {"type": "keyboard", "offset": 0},  # 3.26 текущее
            {"type": "keyboard", "offset": 1},  # 3.29 +1 мин
        ],
        ids=["3.26_current", "3.29_plus_1min"],
    )
    def test_update_news_time_keyboard_today(self, edit_news_form, time_options):
        news_page, title, _ = edit_news_form
        with allure.step("Изменить время через клавиатуру и сохранить"):
            news_page.update_news(time=time_options)
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("3.30")
    @allure.title("При дате «Завтра» время раньше текущего на часах принимается")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    def test_update_news_time_before_now_with_tomorrow(self, edit_news_form):
        news_page, title, _ = edit_news_form
        with allure.step("Изменить дату на завтра и время раньше текущего"):
            news_page.update_news(
                date="tomorrow",
                time={"type": "keyboard", "offset": -60},
            )
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("3.31-3.34, 3.37-3.39")
    @allure.title("Валидация описания: валидные значения")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    @pytest.mark.parametrize(
        "description",
        [
            "AutotestUpdateDescription",   # 3.31 латиница
            "ОписаниеАвтотестаРедакт",     # 3.32 кириллица
            "9876543210",                  # 3.33 цифры
            "!@#$%^&*()",                  # 3.34 символы
            "B",                           # 3.37 один символ
            "B" * 1000,                    # 3.38 максимум 1000
            "B" * 999,                     # 3.39 максимум - 1
        ],
    )
    def test_update_news_description_validation(self, edit_news_form, description):
        news_page, title, _ = edit_news_form
        with allure.step("Изменить описание на проверяемое значение и сохранить"):
            news_page.update_news(description=description)
        with allure.step("Проверить новость в панели управления"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("3.35-3.36")
    @allure.title("Отправка пустого или пробельного описания")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Негативные сценарии")
    @pytest.mark.parametrize(
        "description",
        [
            " ",  # 3.35 пробел
            "",   # 3.36 пустое поле
        ],
    )
    def test_update_news_description_empty(self, edit_news_form, description):
        news_page, _, _ = edit_news_form
        with allure.step("Очистить описание; при пробеле ввести пробел"):
            if description:
                news_page.fill_description(description)
            else:
                news_page.clear_field(*news_page.DESCRIPTION_FIELD)
        with allure.step("Сохранить с пустым или пробельным описанием"):
            news_page.save_news()
        with allure.step("Проверить toast об ошибке"):
            toast = news_page.get_toast_message(timeout=5)
            assert "Заполните пустые поля" in toast

    @allure.id("3.43")
    @allure.title("Перевод новости в статус Не активна")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    def test_update_news_status_inactive(self, edit_news_form):
        news_page, title, _ = edit_news_form
        with allure.step("Выключить переключатель и сохранить"):
            news_page.update_news(active=False)
        with allure.step("Проверить статус в панели управления"):
            assert news_page.get_news_status(title).casefold() == "не активна"

    @allure.id("3.42")
    @allure.title("Перевод новости в статус Активна")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Позитивные сценарии")
    def test_update_news_status_active(self, edit_news_form):
        news_page, title, _ = edit_news_form
        with allure.step("Сначала перевести в Не активна"):
            news_page.update_news(active=False)
        with allure.step("Снова открыть редактирование"):
            news_page.open_edit_news_form(title)
        with allure.step("Включить переключатель и сохранить"):
            news_page.update_news(active=True)
        with allure.step("Проверить статус в панели управления"):
            assert news_page.get_news_status(title).casefold() == "активна"