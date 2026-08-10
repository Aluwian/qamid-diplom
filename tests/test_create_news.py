from datetime import datetime
import allure
from pages.main_page import MainPage
from pages.news_page import NewsPage


@allure.epic("Мобильный хоспис")
@allure.feature("Создание новостей")
class TestCreateNews:
    @allure.id("2.2")
    @allure.title("Создание новости с валидными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Позитивные сценарии")
    def test_create_news_valid(self, authorized_driver):
        main_page = MainPage(authorized_driver)
        news_page = NewsPage(authorized_driver)
        title = f"Автотест_{datetime.now().strftime('%H%M%S')}"
        with allure.step("Открыть форму создания новости"):
            main_page.go_to_news()
            news_page.open_control_panel()
            news_page.open_create_news_form()
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
    def test_create_news_empty_form(self, authorized_driver):
        main_page = MainPage(authorized_driver)
        news_page = NewsPage(authorized_driver)
        with allure.step("Открыть форму создания новости"):
            main_page.go_to_news()
            news_page.open_control_panel()
            news_page.open_create_news_form()
        with allure.step("Кликнуть кнопку Сохранить без заполнения полей"):
            news_page.save_news()
        with allure.step("Проверить toast об ошибке"):
            toast = news_page.get_toast_message(timeout=5)
            assert "Заполните пустые поля" in toast