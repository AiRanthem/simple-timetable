import time

from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait

from settings import DRIVER_FILE
from utils.ClassUtils import synchronized

import pickle
import os


class Extractor:
    """
    解析动态站点的工具类基类。
    如果要进行动态站点解析，请另开一个py文件并像 DesktopLinkExtractor 一样继承该类并实现解析方法。
    """
    timeout = 5
    _instance = None

    @synchronized
    def __new__(cls, *args, **kwargs):
        """
        单例模式
        """
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, headless=True, close_at_last=True) -> None:
        """
        以无头模式运行chrome
        """
        chrome_opt = ChromeOptions()
        self._close_at_last = close_at_last
        # prefs = {"profile.managed_default_content_settings.images": 2}
        # chrome_opt.add_experimental_option("prefs", prefs)
        if headless:
            chrome_opt.add_argument('headless')
            chrome_opt.add_argument('--disable-gpu')
        self._driver = Chrome(executable_path=DRIVER_FILE, chrome_options=chrome_opt)

    def __del__(self):
        """
        关闭浏览器
        """
        if self._close_at_last:
            self._driver.close()

    def wait_an_element_by_xpath(self, xpath):
        """阻塞获取元素"""
        try:
            element = WebDriverWait(self._driver, self.timeout).until(
                lambda driver: driver.find_element_by_xpath(xpath)
            )
            return element
        except Exception as e:
            print("ERROR:", e)
            return None


class SsfwExtractor(Extractor):
    _baseurl = "http://ssfw.xmu.edu.cn/cmstar"
    _logged_in = False

    def login(self, username, password):
        self._driver.get(self._baseurl + "/index.portal")
        self._driver.find_element_by_xpath('//input[@id="username"]').send_keys(username)
        self._driver.find_element_by_xpath('//input[@id="password"]').send_keys(password)
        self._driver.find_element_by_xpath('//*[@id="mid_2"]/div/table/tbody/tr[6]/td/input[2]').click()
        time.sleep(1)
        self._driver.find_element_by_xpath('//*[@id="mid_2"]/div/table/tbody/tr[7]/td/input[1]').click()
        self._logged_in = True

    def extract_timetable(self):
        if not self._logged_in:
            print("Please CALL function login first")
            return
        self.wait_an_element_by_xpath('//*[@id="pp1201_p3530"]/div/div/a').click()
        time.sleep(1)
        try:
            self.wait_an_element_by_xpath('//*[@id="pp1201_p3530_p3531"]/a/span').click()
        except ElementNotInteractableException as e:
            print(e)

        table = self.wait_an_element_by_xpath('//*[@id="queryFormf2609"]/tbody')
        rows = table.find_elements_by_xpath("tr")[1:]

        html_row = []
        for row in rows:

            cols = row.find_elements_by_xpath('td')[2:]
            html_col = []
            for col in cols:
                box = col.text
                html_col.append(box)
            html_row.append(html_col)

        return html_row

    def testFor(self):
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__), 'table.pickle'))
        with open(filename, 'rb') as f:
            table = pickle.load(f)
        return table


if __name__ == '__main__':
    """
    简单单元测试代码
    """
    # from scrapy_APP.config import USERNAME, PASSWORD
    # extractor = SsfwExtractor(False, False)
    # extractor.login(USERNAME, PASSWORD)
    # extractor.extract_timetable()


