import pytest

from page_objects.drag_and_drop_page import DragAndDropPage
from page_objects.landing_page import LandingPage
from page_objects.base_page import BasePage


@pytest.mark.dragdrop
class TestDragAndDrop:
    def test_drag_and_drop_success(self, driver):
        # Go to webpage
        landing_page = LandingPage(driver)
        landing_page.open()

        # Click on Drag and Drop
        landing_page.click_drag_and_drop_testing_link()

        # Verify page is on Drag and Drop
        drag_and_drop_page = DragAndDropPage(driver)
        drag_and_drop_page.d_and_d_page_loaded_successfully()
        
        # Perform drag and drop
        drag_and_drop_page.drag_and_drop_js()
        
        # Verify elements switched places
        assert drag_and_drop_page.get_column_text("a") == "B", "Column A should contain 'A' after reverting drag and drop"
        assert drag_and_drop_page.get_column_text("b") == "A", "Column B should contain 'B' after reverting drag and drop"

    def test_drag_and_drop_reverse(self, driver):
         # Go to webpage
        landing_page = LandingPage(driver)
        landing_page.open()

        # Click on Drag and Drop
        landing_page.click_drag_and_drop_testing_link()

        # Verify page is on Drag and Drop
        drag_and_drop_page = DragAndDropPage(driver)
        drag_and_drop_page.d_and_d_page_loaded_successfully()
        
        # Perform drag and drop twice to revert
        drag_and_drop_page.drag_and_drop_js()
        drag_and_drop_page.drag_and_drop_js()
        
        # Verify elements are back to original position
        
        assert drag_and_drop_page.get_column_text("a") == "A", "Column A should contain 'A' after reverting drag and drop"
        assert drag_and_drop_page.get_column_text("b") == "B", "Column B should contain 'B' after reverting drag and drop"

    
    def test_drag_and_drop_with_page_resize(self, driver):
        """Test if drag and drop works after resizing browser window"""
        # Go to webpage
        landing_page = LandingPage(driver)
        landing_page.open()

        # Click on Drag and Drop
        landing_page.click_drag_and_drop_testing_link()

        # Verify page is on Drag and Drop
        drag_and_drop_page = DragAndDropPage(driver)
        drag_and_drop_page.d_and_d_page_loaded_successfully()
        
        # Resize browser window
        action = BasePage(driver)
        original_size = action.get_window_size()
        action.set_window_size(800, 600)
        
        # Perform drag and drop after resize
        drag_and_drop_page.drag_and_drop_js()
        
        # Verify elements switched places
        assert drag_and_drop_page.get_column_text("a") == "B", "Column A should contain 'A' after reverting drag and drop"
        assert drag_and_drop_page.get_column_text("b") == "A", "Column B should contain 'B' after reverting drag and drop"
        
        # Restore original window size
        action.set_window_size(original_size['width'], original_size['height'])
