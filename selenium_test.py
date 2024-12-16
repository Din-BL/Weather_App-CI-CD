from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import unittest
import time
import os


class WeatherAppTests(unittest.TestCase):

    def setUp(self):
        # Set up ChromeDriver for headless environment
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode
        # Required for running as root
        chrome_options.add_argument("--no-sandbox")
        # Overcome limited resource problems
        chrome_options.add_argument("--disable-dev-shm-usage")
        # Disable GPU acceleration
        chrome_options.add_argument("--disable-gpu")
        # Ensure consistent resolution
        chrome_options.add_argument("--window-size=1920x1080")

        # Path to ChromeDriver
        chrome_driver_path = "/usr/local/bin/chromedriver"
        if not os.path.exists(chrome_driver_path):
            raise FileNotFoundError(
                "ChromeDriver not found. Ensure it is installed in /usr/local/bin.")

        # Initialize WebDriver
        self.driver = webdriver.Chrome(service=Service(
            chrome_driver_path), options=chrome_options)
        # Ensure the app is accessible
        self.driver.get('http://localhost:5000')

    def test_positive_location_response(self):
        """Test a valid location and verify temperature display."""
        search_box = self.driver.find_element(By.ID, 'location')
        search_box.clear()
        search_box.send_keys('New York')
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)  # Allow time for page to load

        # Verify that temperature is displayed
        temp_element = self.driver.find_element(
            By.XPATH, '//h2[contains(text(),"°")]')
        self.assertTrue(temp_element.is_displayed(
        ), "Temperature element should be displayed for valid location.")

    def test_negative_location_response(self):
        """Test an invalid location and verify error handling."""
        search_box = self.driver.find_element(By.ID, 'location')
        search_box.clear()
        search_box.send_keys('InvalidCityName')
        search_box.send_keys(Keys.RETURN)
        time.sleep(1)  # Allow time for page to load

        # Verify that error button is displayed
        error_button = self.driver.find_element(
            By.XPATH, '//button[text()="Go Home"]')
        self.assertTrue(error_button.is_displayed(),
                        "Error button should be displayed for invalid location.")

    def tearDown(self):
        # Quit the WebDriver
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
