from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from page_objects.base_page import BasePage


class FileUploadPage(BasePage):
    """Page Object for the File Upload page /upload"""
    
    # URL of the page
    __url = "https://the-internet.herokuapp.com/upload"
    
    # Locators
    __file_input = (By.ID, "file-upload")
    __upload_button = (By.ID, "file-submit")
    __success_message = (By.TAG_NAME, "h3")
    __error_message = (By.TAG_NAME, "h1")
    __uploaded_filename = (By.ID, "uploaded-files")
    __page_header = (By.CSS_SELECTOR, "h3")
    
    def __init__(self, driver):
        """Initialize the page with the driver"""
        super().__init__(driver)
    
    @property
    def current_url(self) -> str:
        return self._driver.current_url
    
    def open(self):
        """Navigate directly to the file upload page"""
        self.open_url(self.__url)
        return self
    
    def verify_page_loaded(self):
        """Verify that the file upload page has loaded correctly"""
        self._wait_until_element_is_visible(self.__page_header)
        header_text = self._find(self.__page_header).text
        assert "File Uploader" in header_text, f"Expected 'File Uploader' in header, but got '{header_text}'"
        return self
    
    def upload_file(self, file_path):
        """Upload a file and click the upload button
        
        Args:
            file_path: The path to the file to upload
        """
        # Wait for the file input to be present
        self._wait_until_element_is_visible(self.__file_input)
        
        # Send the file path to the file input
        file_input = self._find(self.__file_input)
        file_input.send_keys(file_path)
        
        # Click the upload button
        self.click_upload_button()
        
        return self
    
    def click_upload_button(self):
        """Click the upload button"""
        self._click(self.__upload_button)
        
        # Wait for the response (either success or error)
        try:
            self._wait_until_element_is_visible(self.__success_message)
        except TimeoutException:
            print("Timeout waiting for response after clicking upload button")
        
        return self
    
    def get_success_message(self):
        """Get the success message after uploading a file
        
        Returns:
            str: The text of the success message
        """
        try:
            self._wait_until_element_is_visible(self.__success_message)
            return self._find(self.__success_message).text
        except TimeoutException:
            print("Timeout waiting for success message")
            return ""
    
    def get_error_message(self):
        """Get the error message when upload fails
        
        Returns:
            str: The text of the error message
        """
        # Uses the same locator as success message but expects different text
        try:
            self._wait_until_element_is_visible(self.__error_message)
            return self._find(self.__error_message).text
        except TimeoutException:
            print("Timeout waiting for error message")
            return ""
    
    def get_uploaded_filename(self):
        """Get the name of the successfully uploaded file
        
        Returns:
            str: The name of the uploaded file
        """
        try:
            self._wait_until_element_is_visible(self.__uploaded_filename)
            return self._find(self.__uploaded_filename).text
        except TimeoutException:
            print("Timeout waiting for uploaded filename")
            return ""