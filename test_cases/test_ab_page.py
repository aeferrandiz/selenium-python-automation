import pytest

from page_objects.ab_testing_page import AbTestingPage
from page_objects.elemental_selenium_page import elementalSeleniumPage
from page_objects.landing_page import LandingPage


@pytest.mark.smoke
class TestAbPage:
    def test_login_to_ab_link(self, driver):
        # Go to webpage
        landing_page = LandingPage(driver)
        landing_page.open()

        # Click on A/B Testing
        landing_page.click_ab_testing_link()

        # Verify page is on A/B Testing
        ab_testing_page = AbTestingPage(driver)
        ab_testing_page.ab_landing_page_loaded_successfully()

        # Click and land on Elemental Selenium
        elemental_selenium = elementalSeleniumPage(driver)
        elemental_selenium.elemental_landing_page()

    def test_multiple_login_to_ab_link(self, driver):
        # Go to webpage
        landing_page = LandingPage(driver)
        landing_page.open()

        for run_count in range(6):
            # Click on A/B Testing
            landing_page.click_ab_testing_link()
            print('The amount of times running: $run_count')

            # Verify page is on A/B Testing
            ab_testing_page = AbTestingPage(driver)
            ab_testing_page.ab_landing_page_loaded_successfully()

            # Click back
            driver.back()
            