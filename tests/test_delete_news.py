import allure


@allure.epic("Мобильный хоспис")
@allure.feature("Удаление новостей")
class TestDeleteNews:
    @allure.id("4.1")
    @allure.title("Удаление одной новости через кнопку")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Позитивные сценарии")
    def test_delete_one_news(self, news_on_control_panel):
        news_page, title, _ = news_on_control_panel
        with allure.step("Удалить новость и подтвердить в диалоге"):
            news_page.delete_news(title)
        with allure.step("Проверить, что новости нет в панели управления"):
            assert not news_page.is_news_in_control_panel(title, timeout=5)
