from datetime import datetime
import allure


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