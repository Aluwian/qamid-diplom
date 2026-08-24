import allure


@allure.epic("Мобильный хоспис")
@allure.feature("Сортировка новостей")
class TestSortNews:
    @allure.id("7.3")
    @allure.title(
        "Клик по кнопке сортировки - сортировка по дате (ASC)"
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления")
    def test_sort_date_asc(self, news_on_control_panel):
        news_page, title_today, _ = news_on_control_panel
        with allure.step("Создать новость на завтра"):
            news_page.open_create_news_form()
            title_tomorrow, _ = news_page.create_news(date="tomorrow")
        with allure.step("Отфильтровать период сегодня–завтра"):
            news_page.open_filter()
            news_page.select_filter_date(
                start="today", end="tomorrow"
            )
            news_page.apply_filter()
        with allure.step("Кликнуть по кнопке сортировки"):
            news_page.sort_news()
        with allure.step(
                "Проверить порядок: сначала сегодня, потом завтра"
        ):
            order = news_page.get_titles_order(
                [title_today, title_tomorrow]
            )
            assert order == [title_today, title_tomorrow]

    @allure.id("7.4")
    @allure.title(
        "Повторный клик по кнопке сортировки - "
        "сортировка по дате в обратном порядке (DESC)"
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Панель управления")
    def test_sort_date_desc(self, news_on_control_panel):
        news_page, title_today, _ = news_on_control_panel
        with allure.step("Создать новость на завтра"):
            news_page.open_create_news_form()
            title_tomorrow, _ = news_page.create_news(date="tomorrow")
        with allure.step("Отфильтровать период сегодня–завтра"):
            news_page.open_filter()
            news_page.select_filter_date(
                start="today", end="tomorrow"
            )
            news_page.apply_filter()
        with allure.step("Кликнуть по кнопке сортировки дважды"):
            news_page.sort_news()
            news_page.sort_news()
        with allure.step(
                "Проверить порядок: сначала завтра, потом сегодня"
        ):
            order = news_page.get_titles_order(
                [title_today, title_tomorrow]
            )
            assert order == [title_tomorrow, title_today]
