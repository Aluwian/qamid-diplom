import allure
from pages.main_page import MainPage
from pages.news_page import NewsPage


@allure.epic("Мобильный хоспис")
@allure.feature("Навигация")
class TestNavigation:
    @allure.id("9.1")
    @allure.title("Переход на экран Главная")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Меню")
    def test_go_to_main(self, authorized_driver):
        main_page = MainPage(authorized_driver)
        with allure.step("Открыть раздел Новости"):
            main_page.go_to_news()
        with allure.step("Через меню открыть Главная"):
            main_page.go_to_main()
        with allure.step("Проверить экран Главная"):
            all_news = main_page.find_element(*main_page.ALL_NEWS_TEXT)
            assert all_news.is_displayed()

    @allure.id("9.2")
    @allure.title("Переход в раздел Новости")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Меню")
    def test_go_to_news(self, authorized_driver):
        main_page = MainPage(authorized_driver)
        news_page = NewsPage(authorized_driver)
        with allure.step("Через меню открыть Новости"):
            main_page.go_to_news()
        with allure.step("Проверить экран Новости (карандаш)"):
            pencil = news_page.find_element(*news_page.EDIT_NEWS_BUTTON)
            assert pencil.is_displayed()

    @allure.id("9.3")
    @allure.title("Переход на страницу О приложении")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Меню")
    def test_go_to_about(self, authorized_driver):
        main_page = MainPage(authorized_driver)
        with allure.step("Через меню открыть О приложении"):
            main_page.go_to_about()
        with allure.step("Проверить экран О приложении"):
            version = main_page.find_element(*main_page.ABOUT_VERSION)
            assert version.is_displayed()

    @allure.id("9.6")
    @allure.title("Работа системной кнопки Назад")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Системная навигация")
    def test_system_back(self, authorized_driver):
        main_page = MainPage(authorized_driver)
        with allure.step("Открыть раздел Новости"):
            main_page.go_to_news()
        with allure.step("Нажать системную кнопку Назад"):
            main_page.go_back()
        with allure.step("Проверить возврат на Главная"):
            all_news = main_page.find_element(*main_page.ALL_NEWS_TEXT)
            assert all_news.is_displayed()

    @allure.id("9.7")
    @allure.title("Проверка отображения страницы Цитаты")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Цитаты")
    def test_go_to_quotes(self, authorized_driver):
        main_page = MainPage(authorized_driver)
        with allure.step("Открыть Цитаты кнопкой бабочки"):
            main_page.go_to_quotes()
        with allure.step("Проверить заголовок страницы Цитаты"):
            title = main_page.find_element(*main_page.QUOTES_TITLE)
            assert title.is_displayed()
