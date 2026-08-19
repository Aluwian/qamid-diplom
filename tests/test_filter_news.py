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

    @allure.id("6.4")
    @allure.title("Обе даты корректны")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По дате")
    def test_filter_date_valid_period(self, news_on_control_panel):
        news_page, title, _ = news_on_control_panel
        with allure.step("Задать период сегодня–сегодня и фильтровать"):
            news_page.open_filter()
            news_page.select_filter_date(start="today", end="today")
            news_page.apply_filter()
        with allure.step("Проверить свою новость в панели"):
            assert news_page.is_news_in_control_panel(title)

    @allure.id("6.5")
    @allure.title("Заполнена только начальная дата")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По дате")
    def test_filter_date_start_only(self, news_on_control_panel):
        news_page, _, _ = news_on_control_panel
        with allure.step("Заполнить только Start и фильтровать"):
            news_page.open_filter()
            news_page.select_filter_date(start="today")
            news_page.apply_filter()
        with allure.step("Проверить диалог об ошибке периода"):
            message = news_page.get_alert_message()
            assert "Неверно указан период" in message

    @allure.id("6.6")
    @allure.title("Заполнена только конечная дата")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По дате")
    def test_filter_date_end_only(self, news_on_control_panel):
        news_page, _, _ = news_on_control_panel
        with allure.step("Заполнить только End и фильтровать"):
            news_page.open_filter()
            news_page.select_filter_date(end="today")
            news_page.apply_filter()
        with allure.step("Проверить диалог об ошибке периода"):
            message = news_page.get_alert_message()
            assert "Неверно указан период" in message

    @allure.id("6.7")
    @allure.title("Конечная дата раньше начальной")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По дате")
    def test_filter_date_end_before_start(self, news_on_control_panel):
        news_page, _, _ = news_on_control_panel
        with allure.step("Задать период завтра–сегодня и фильтровать"):
            news_page.open_filter()
            news_page.select_filter_date(start="tomorrow", end="today")
            news_page.apply_filter()
        with allure.step("Проверить, что список пуст"):
            assert news_page.is_control_panel_empty()

    @allure.id("6.8")
    @allure.title("Выбор периода без новостей")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По дате")
    def test_filter_date_period_without_news(self, news_on_control_panel):
        news_page, _, _ = news_on_control_panel
        with allure.step("Задать день в следующем месяце и фильтровать"):
            news_page.open_filter()
            news_page.select_filter_empty_period()
            news_page.apply_filter()
        with allure.step("Проверить, что список пуст"):
            assert news_page.is_control_panel_empty()

    @allure.id("6.9")
    @allure.title("Выбор статуса Активна")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По статусу")
    def test_filter_status_active(self, news_on_control_panel):
        news_page, title_active, _ = news_on_control_panel
        with allure.step("Создать неактивную новость"):
            news_page.open_create_news_form()
            title_inactive, _ = news_page.create_news()
            news_page.open_edit_news_form(title_inactive)
            news_page.update_news(active=False)
        with allure.step("Оставить только статус Активна и фильтровать"):
            news_page.open_filter()
            news_page.set_filter_status(active=True, inactive=False)
            news_page.apply_filter()
        with allure.step("Проверить свои новости в панели"):
            assert news_page.is_news_in_control_panel(title_active)
            assert not news_page.is_news_in_control_panel(
                title_inactive, timeout=5
            )

    @allure.id("6.10")
    @allure.title("Выбор статуса Не активна")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По статусу")
    def test_filter_status_inactive(self, news_on_control_panel):
        news_page, title_active, _ = news_on_control_panel
        with allure.step("Создать неактивную новость"):
            news_page.open_create_news_form()
            title_inactive, _ = news_page.create_news()
            news_page.open_edit_news_form(title_inactive)
            news_page.update_news(active=False)
        with allure.step("Оставить только статус Не активна и фильтровать"):
            news_page.open_filter()
            news_page.set_filter_status(active=False, inactive=True)
            news_page.apply_filter()
        with allure.step("Проверить свои новости в панели"):
            assert news_page.is_news_in_control_panel(title_inactive)
            assert not news_page.is_news_in_control_panel(
                title_active, timeout=5
            )

    @allure.id("6.11")
    @allure.title("Выбор обоих статусов")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления. По статусу")
    def test_filter_status_both(self, news_on_control_panel):
        news_page, title_active, _ = news_on_control_panel
        with allure.step("Создать неактивную новость"):
            news_page.open_create_news_form()
            title_inactive, _ = news_page.create_news()
            news_page.open_edit_news_form(title_inactive)
            news_page.update_news(active=False)
        with allure.step("Оставить оба статуса и фильтровать"):
            news_page.open_filter()
            news_page.set_filter_status(active=True, inactive=True)
            news_page.apply_filter()
        with allure.step("Проверить, что обе новости в панели"):
            assert news_page.is_news_in_control_panel(title_active)
            assert news_page.is_news_in_control_panel(title_inactive)
