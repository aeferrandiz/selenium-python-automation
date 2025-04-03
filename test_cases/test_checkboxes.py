import pytest

from page_objects.landing_page import LandingPage
from page_objects.base_page import BasePage
from page_objects.checkbox_page import CheckboxesPage

@pytest.mark.checkboxes
class TestCheckboxes:
    def test_checkbox_interaction(self, driver):
        """Test interaction with checkboxes - selection, deselection and state verification"""
        # Go to webpage
        landing_page = LandingPage(driver)
        landing_page.open()
        
        # Click on Checkboxes link
        landing_page.click_checkboxes_testing_link()
        
        # Verify checkboxes page is loaded
        checkboxes_page = CheckboxesPage(driver)
        checkboxes_page.checkboxes_page_loaded_successfully()
        
        # Verify initial state (typically checkbox 1 is unchecked, checkbox 2 is checked)
        assert not checkboxes_page.is_checkbox_selected(1), "Checkbox 1 should be unchecked initially"
        assert checkboxes_page.is_checkbox_selected(2), "Checkbox 2 should be checked initially"
        
        # Select checkbox 1
        checkboxes_page.toggle_checkbox(1)
        
        # Verify checkbox 1 is now selected
        assert checkboxes_page.is_checkbox_selected(1), "Checkbox 1 should be checked after selection"
        
        # Deselect checkbox 2
        checkboxes_page.toggle_checkbox(2)
        
        # Verify checkbox 2 is now deselected
        assert not checkboxes_page.is_checkbox_selected(2), "Checkbox 2 should be unchecked after deselection"
        
        # Toggle both checkboxes back to original state
        checkboxes_page.toggle_checkbox(1)
        checkboxes_page.toggle_checkbox(2)
        
        # Verify checkboxes returned to initial state
        assert not checkboxes_page.is_checkbox_selected(1), "Checkbox 1 should be unchecked after toggling back"
        assert checkboxes_page.is_checkbox_selected(2), "Checkbox 2 should be checked after toggling back"

    def test_checkbox_state_after_page_refresh(self, driver):
        """Test if checkbox states persist after page refresh"""
        # Go to webpage
        landing_page = LandingPage(driver)
        landing_page.open()
        
        # Click on Checkboxes link
        landing_page.click_checkboxes_testing_link()
        
        # Verify checkboxes page is loaded
        checkboxes_page = CheckboxesPage(driver)
        checkboxes_page.checkboxes_page_loaded_successfully()
        
        # Record initial state
        initial_checkbox1_state = checkboxes_page.is_checkbox_selected(1)
        initial_checkbox2_state = checkboxes_page.is_checkbox_selected(2)
        
        # Change state of both checkboxes
        checkboxes_page.toggle_checkbox(1)
        checkboxes_page.toggle_checkbox(2)
        
        # Verify states changed
        assert checkboxes_page.is_checkbox_selected(1) != initial_checkbox1_state, "Checkbox 1 state should have changed"
        assert checkboxes_page.is_checkbox_selected(2) != initial_checkbox2_state, "Checkbox 2 state should have changed"
        
        # Refresh the page
        #driver.refresh()
        action = BasePage(driver)
        action._refresh_page()

        # Verify checkboxes page is loaded again
        checkboxes_page.checkboxes_page_loaded_successfully()
        
        # Check if states reset to default or persist after refresh
        # Note: On most sites, form states don't persist after refresh unless explicitly saved
        assert not checkboxes_page.is_checkbox_selected(1), "Checkbox 1 should reset to unchecked after page refresh"
        assert checkboxes_page.is_checkbox_selected(2), "Checkbox 2 should reset to checked after page refresh"
        