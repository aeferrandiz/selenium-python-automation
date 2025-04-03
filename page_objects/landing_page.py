from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base_page import BasePage


class LandingPage(BasePage):
    __url = "https://the-internet.herokuapp.com/"
    __url_ab_page = "abtest"
    __url_d_and_d_page = "drag_and_drop"
    __url_checkbox_page = "checkboxes"
    __url_file_upload = "upload"
    __ab_testing_link = (By.XPATH, "//a[contains(., 'A/B Testing')]")
    __d_and_d_testing_link = (By.XPATH, "//a[contains(., 'Drag and Drop')]")
    __checkbox_testing_link = (By.XPATH, "//a[contains(., 'Checkboxes')]")
    __file_upload_testing_link = (By.XPATH, "//a[contains(., 'File Upload')]")
    __add_remove_link = (By.XPATH, "//a[contains(., 'Add/Remove Elements')]")
    __home_page_header = (By.XPATH, "//a[contains(., 'Welcome to the-internet')]")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def open(self):
        super().open_url(self.__url)

    def click_ab_testing_link(self):
        super()._click(self.__ab_testing_link)
        super()._wait_until_url_contains(self.__url_ab_page)

    def click_drag_and_drop_testing_link(self):
        super()._click(self.__d_and_d_testing_link)
        super()._wait_until_url_contains(self.__url_d_and_d_page)

    def click_checkboxes_testing_link(self):
        super()._click(self.__checkbox_testing_link)
        super()._wait_until_url_contains(self.__url_checkbox_page)

    def click_file_upload_testing_link(self):
        super()._click(self.__file_upload_testing_link)
        super()._wait_until_url_contains(self.__url_file_upload)

    def click_add_remove_link(self):
        super()._click(self.__ab_testing_link)
        super()._wait_until_element_is_not_visible(self.__home_page_header)