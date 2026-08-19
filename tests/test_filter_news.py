import allure


@allure.epic("Мобильный хоспис")
@allure.feature("Фильтрация новостей")
class TestFilterNews:
    @allure.id("6.1")
    @allure.title(
        "Выбор категории, которая назначена хотя бы одной новости"
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По категории")
    def test_filter_category_with_news(self, news_on_control_panel):
        news_page, title_ads, _ = news_on_control_panel
        with allure.step("Создать новость другой категории"):
            news_page.open_create_news_form()
            title_bday, _ = news_page.create_news(
                category="День рождения",
            )
        with allure.step("Отфильтровать по категории Объявление"):
            news_page.open_filter()
            news_page.select_filter_category("Объявление")
            news_page.apply_filter()
        with allure.step("Проверить свои новости в панели"):
            assert news_page.is_news_in_control_panel(title_ads)
            assert not news_page.is_news_in_control_panel(
                title_bday, timeout=5
            )

    @allure.id("6.2")
    @allure.title("Без выбора категории")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По категории")
    def test_filter_without_category(self, news_on_control_panel):
        news_page, title, _ = news_on_control_panel
        with allure.step("Открыть фильтр и применить без категории"):
            news_page.open_filter()
            news_page.apply_filter()
        with allure.step("Проверить, что новость осталась в панели"):
            assert news_page.is_news_in_control_panel(title)