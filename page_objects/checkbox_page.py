from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base_page import BasePage


class CheckboxesPage(BasePage):
    __url = "https://the-internet.herokuapp.com/checkboxes"
    __checkboxes_test_header = (By.TAG_NAME, "h3")
    __checkboxes = (By.CSS_SELECTOR, "input[type='checkbox']")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @property
    def current_url(self) -> str:
        return self._driver.current_url

    def open(self):
        """Navigate directly to the checkboxes page"""
        self.open_url(self.__url)
        return self

    def checkboxes_page_loaded_successfully(self):
        """Verify that the checkboxes page is loaded correctly"""
        assert self.is_displayed(self.__checkboxes_test_header), "The header is not displayed"
        return self

    def get_checkbox(self, checkbox_number):
        """Get a specific checkbox element (1 or 2)"""
        # Adjust index since checkbox_number is 1-based but list is 0-based
        index = checkbox_number - 1
        
        # Ensure the checkboxes are visible before trying to access them
        self._wait_until_element_is_visible(self.__checkboxes)
        
        # We need to get all checkboxes manually since BasePage doesn't have a find_elements method
        checkboxes = self._driver.find_elements(*self.__checkboxes)
        
        if index < 0 or index >= len(checkboxes):
            raise ValueError(f"Checkbox number {checkbox_number} is out of range. Only {len(checkboxes)} checkboxes available.")
            
        return checkboxes[index]
    
    def is_checkbox_selected(self, checkbox_number):
        """Check if a specific checkbox is selected"""
        checkbox = self.get_checkbox(checkbox_number)
        return checkbox.is_selected()
    
    def toggle_checkbox(self, checkbox_number):
        """Toggle the state of a specific checkbox"""
        checkbox = self.get_checkbox(checkbox_number)
        checkbox.click()
        return self
    
    def select_checkbox(self, checkbox_number):
        """Select a specific checkbox if it's not already selected"""
        if not self.is_checkbox_selected(checkbox_number):
            self.toggle_checkbox(checkbox_number)
        return self
    
    def deselect_checkbox(self, checkbox_number):
        """Deselect a specific checkbox if it's currently selected"""
        if self.is_checkbox_selected(checkbox_number):
            self.toggle_checkbox(checkbox_number)
        return self
    
    def get_all_checkboxes_state(self):
        """Get the selection state of all checkboxes as a list of booleans"""
        # Ensure the checkboxes are visible
        self._wait_until_element_is_visible(self.__checkboxes)
        
        # Get all checkboxes
        checkboxes = self._driver.find_elements(*self.__checkboxes)
        return [checkbox.is_selected() for checkbox in checkboxes]
