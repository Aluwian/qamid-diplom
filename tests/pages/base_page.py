from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class BasePage:
    # Базовый класс с основными методами взаимодействия с UI элементами
    def __init__(self, driver):
        self.driver = driver

    # Метод поиска элементов
    def find_element(self, by, locator, timeout=10,
                     condition=expected_conditions.presence_of_element_located):
        return WebDriverWait(self.driver, timeout).until(
            condition((by, locator))
        )

    # Методы взаимодействия с элементами
    def click(self, by, value, timeout=10):
        # Клик по элементу
        element = self.find_element(
            by, value, timeout,
            condition=expected_conditions.element_to_be_clickable
        )
        # Перед кликом ожидаем полной загрузки кнопки чтобы она стала кликабельной
        element.click()

    def send_keys(self, by, value, input_text):
        # Ввод текста в поле
        element = self.find_element(by, value)
        # Очищаем от старого текста на случай, если поле заполнено
        element.clear()
        element.send_keys(input_text)

    def get_text(self, by, locator, timeout=10):
        # Метод возвращает текст(например для чтения флеш-сообщений)
        element = self.find_element(by, locator, timeout)
        return element.text

    def get_toast_message(self, timeout=10):
        # Отлов android.widget.Toast с сообщениями об ошибках
        toast_locator = (AppiumBy.XPATH, "//android.widget.Toast")
        wait = WebDriverWait(self.driver, timeout, poll_frequency=0.1)
        toast_element = wait.until(
            expected_conditions.presence_of_element_located(toast_locator)
        )
        return toast_element.text

    def tap_element_center(self, by, locator, times=1):
        # Кликает по центру указанного элемента несколько раз
        element = self.find_element(by, locator)
        rect = element.rect
        center_x = rect['x'] + rect['width'] // 2
        center_y = rect['y'] + rect['height'] // 2
        for _ in range(times):
            self.driver.tap([(center_x, center_y)])
