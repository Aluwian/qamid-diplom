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
        title = f"Автотест_{datetime.now().strftime('%H%M%S')}"
        with allure.step("Заполнить форму и сохранить"):
            news_page.create_news(
                category="Объявление",
                title=title,
                description="Описание автотеста",
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

