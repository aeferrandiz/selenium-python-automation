import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains

from page_objects.base_page import BasePage


class DragAndDropPage(BasePage):
    __url = "https://the-internet.herokuapp.com/drag_and_drop"
    __d_and_d_test_header = (By.TAG_NAME, "h3")
    __column_a = (By.ID, "column-a")
    __column_b = (By.ID, "column-b")

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    @property
    def current_url(self) -> str:
        return super()._driver.current_url
    
    def open(self):
        """Navigate directly to the drag_and_drop page"""
        self.open_url(self.__url)
        return self
    
    def d_and_d_page_loaded_successfully(self):
        assert super().is_displayed(self.__d_and_d_test_header), "The header is not displayed"

    def drag_and_drop_elements(self):
        """
        Original Method using ActionChains (Warning: May not be compatible with some browsers)
        """
        source = self._find(self.__column_a)
        target = self._find(self.__column_b)
        ActionChains(self._driver).drag_and_drop(source, target).perform()
    
    def drag_and_drop_js(self):
        """
        Implement drag and drop method using JavaScript (Stack Overflow solution: https://stackoverflow.com/questions/60077655/unable-to-perform-drag-and-drop-with-selenium-python)
        """
        # JavaScript helper to solve issue with Drag and Drop
        js_drag_and_drop = """
        function createEvent(typeOfEvent) {
            var event = document.createEvent("CustomEvent");
            event.initCustomEvent(typeOfEvent, true, true, null);
            event.dataTransfer = {
                data: {},
                setData: function(key, value) {
                    this.data[key] = value;
                },
                getData: function(key) {
                    return this.data[key];
                }
            };
            return event;
        }

        function dispatchEvent(element, event, transferData) {
            if (transferData !== undefined) {
                event.dataTransfer = transferData;
            }
            if (element.dispatchEvent) {
                element.dispatchEvent(event);
            } else if (element.fireEvent) {
                element.fireEvent("on" + event.type, event);
            }
        }

        function simulateHTML5DragAndDrop(element, destination) {
            var dragStartEvent = createEvent('dragstart');
            dispatchEvent(element, dragStartEvent);
            var dropEvent = createEvent('drop');
            dispatchEvent(destination, dropEvent, dragStartEvent.dataTransfer);
            var dragEndEvent = createEvent('dragend');
            dispatchEvent(element, dragEndEvent, dropEvent.dataTransfer);
        }

        var source = arguments[0];
        var destination = arguments[1];
        simulateHTML5DragAndDrop(source, destination);
        """
        
        source = self._find(self.__column_a)
        target = self._find(self.__column_b)
        
        # Execute the JS script to perform drag and drop
        self._driver.execute_script(js_drag_and_drop, source, target)
        
        # Wait a moment for the action to complete.
        time.sleep(1)

    def get_column_text(self, column: str) -> str:
        column_mapping = {"a": self.__column_a, "b": self.__column_b}
        if column.lower() not in column_mapping:
            raise ValueError("Column must be 'a' or 'b'")
        return self._driver.find_element(*column_mapping[column.lower()]).text