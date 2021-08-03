import random
import time

from selenium.common.exceptions import TimeoutException, MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


def split_by_comma(s: str) -> list:
    s = s.replace(' ', '')
    return s.split(',')


class LoadPageMixin:
    _action: ActionChains
    _driver: WebDriver

    PAGE_LOAD_TIMEOUT = 180

    def load_page(self, url):
        self._driver.get(url)
        self._page_is_load_successfully()
        print('Page loading completed.')

    def page_has_loaded(self, driver: WebDriver) -> bool:
        time.sleep(1)
        self.__move_cursor()
        page_state = driver.execute_script('return document.readyState;')
        return page_state == 'complete'

    def _page_is_load_successfully(self):
        try:
            wait = WebDriverWait(self._driver, self.PAGE_LOAD_TIMEOUT)
            wait.until(self.page_has_loaded)
        except TimeoutException:
            raise Exception(f'Page loading error: Page load timed-out')

        return True

    def __move_cursor(self):
        try:
            x, y = self.__calculate_coordinates()
            self._action.move_by_offset(x, y)
            self._action.perform()
        except MoveTargetOutOfBoundsException:
            self._action = ActionChains(self._driver)
            self._action.reset_actions()
        except Exception as e:
            print(f'Move cursor error: {e}')

    @staticmethod
    def __calculate_coordinates():
        return random.randint(1, 1000), random.randint(1, 1000)
