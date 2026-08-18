from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import allure
import pytest
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.news_page import NewsPage


APPIUM_PORT = 4723
APPIUM_HOST = '127.0.0.1'
APP_PACKAGE = "ru.iteco.fmhandroid"


# 1. Создание драйвера с нужными настройками
def create_driver(no_reset=True):
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android"
    options.app_package = APP_PACKAGE
    options.app_activity = ".ui.AppActivity"
    options.no_reset = no_reset

    driver = webdriver.Remote(
        command_executor=f'http://{APPIUM_HOST}:{APPIUM_PORT}',
        options=options
    )
    return driver


# Делает скриншот в Allure, если тест упал
def make_screen(driver, name="failure"):
    try:
        png = driver.get_screenshot_as_png()
        allure.attach(
            png,
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception:
        pass


# Проверяет, упал ли тест (нужно для скриншота)
def check_test_failed(request):
    rep_call = getattr(request.node, "rep_call", None)
    return rep_call is not None and rep_call.failed


# 2. Базовый драйвер(для быстрого старта, сохраняется состояние)
@pytest.fixture(scope='function')
def android_driver(request):
    driver = create_driver(no_reset=True)
    yield driver
    if check_test_failed(request):
        make_screen(driver, request.node.name)
    driver.quit()


# 3. "Свежий" драйвер специально для тестов АВТОРИЗАЦИИ
@pytest.fixture(scope="function")
def fresh_driver(request):
    driver = create_driver(no_reset=False)
    yield driver
    if check_test_failed(request):
        make_screen(driver, request.node.name)
    driver.quit()


# 3. Драйвер с уже выполненной авторизацией (для CRUD тестов)
@pytest.fixture(scope="function")
def authorized_driver(android_driver):
    driver = android_driver

    driver.terminate_app(APP_PACKAGE)
    driver.activate_app(APP_PACKAGE)

    login_page = LoginPage(driver)
    try:
        login_page.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Новости")',
            timeout=5
        )
    except Exception:
        login_page.login(login="login2", password="password2")

    yield driver

    driver.terminate_app(APP_PACKAGE)
    driver.execute_script("mobile: clearApp", {"appId": APP_PACKAGE})


# Фикстура для перехода в режим создания новости - нужна для удаления дублирования
@pytest.fixture
def create_news_form(authorized_driver):
    main_page = MainPage(authorized_driver)
    news_page = NewsPage(authorized_driver)
    with allure.step("Открыть форму создания новости"):
        main_page.go_to_news()
        news_page.open_control_panel()
        news_page.open_create_news_form()
    return news_page


# Фикстура для перехода в режим редактирования новости
@pytest.fixture
def edit_news_form(authorized_driver):
    main_page = MainPage(authorized_driver)
    news_page = NewsPage(authorized_driver)
    with allure.step("Создать новость и открыть форму редактирования"):
        main_page.go_to_news()
        news_page.open_control_panel()
        news_page.open_create_news_form()
        title, description = news_page.create_news()
        news_page.open_edit_news_form(title)
    return news_page, title, description


# Создаёт новость и оставляет её в панели (для теста удаления)
@pytest.fixture
def news_on_control_panel(authorized_driver):
    main_page = MainPage(authorized_driver)
    news_page = NewsPage(authorized_driver)
    with allure.step("Создать новость в панели управления"):
        main_page.go_to_news()
        news_page.open_control_panel()
        news_page.open_create_news_form()
        title, description = news_page.create_news()
    return news_page, title, description


# Пишет результат теста. Без него фикстуры не знают: упал тест или нет
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
