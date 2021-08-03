from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from typing import List, Dict

from utils import LoadPageMixin, split_by_comma


class Company:

    def __init__(self, name):
        self.name: str = name
        self.locations = {'Адрес': '', 'Юридический адрес': '', 'Фактический адрес': '', 'Почтовый адрес': ''}
        self.phone_numbers = []
        self.fax = None
        self.emails = []
        self.website = None
        self.services = None

    def print_data(self):
        print('Name:', self.name)
        print('Locations:', str(self.locations))
        print('Phone numbers:', str(self.phone_numbers))
        print('Fax:', self.fax)
        print('Emails:', str(self.emails))
        print('Website:', self.website)
        print('Services:', str(self.services))


class CompaniesParser(LoadPageMixin):

    def __init__(self):
        self.companies = []
        self._driver = webdriver.Chrome('res/chromedriver.exe')
        self._action = ActionChains(self._driver)
        self._action.reset_actions()

    def parse(self, url: str) -> None:
        self.load_page(url)
        company_links = [x.get_attribute('href') for x in self._driver.find_elements_by_xpath(
            "//div[contains(@class,'cart-company-lg__title')]/a")]

        for link in company_links:
            self.load_page(link)
            company = Company(self._driver.find_element_by_xpath('//h1').text)

            info_items = self._driver.find_elements_by_xpath(
                "//div[@class='company-main-info']//div[@class='company-sidebar__item']")
            for item in info_items:
                try:
                    item_type = item.find_element_by_xpath("span[@class='company-sidebar__label']").text
                    item_value = item.find_element_by_xpath("div[@class='company-sidebar__data']").text
                except NoSuchElementException:
                    continue

                item_type_lower = str(item_type).lower()
                if 'адрес' in item_type_lower:
                    company.locations[item_type] = item_value
                elif 'phone' in item_type_lower or 'телефон' in item_type_lower:
                    company.phone_numbers += split_by_comma(item_value)
                elif 'fax' in item_type_lower or 'факс' in item_type_lower:
                    company.fax = item_value
                elif 'mail' in item_type_lower:
                    company.emails += split_by_comma(item_value)
                elif 'сайт' in item_type_lower:
                    company.website = item_value
                elif item_type == 'Торговые марки':
                    pass
                else:
                    raise Exception(f'Unknown type: {item_type}')

            company.services = self._driver.find_element_by_xpath(
                "//div[@class='company-main-info']/div[contains(@class,'hide_text')]").text

            self.companies.append(company)

            company.print_data()
            print()

    def close_driver(self):
        self._driver.close()
