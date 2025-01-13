import unittest
import Helpers as HP
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from faker import Faker
fake = Faker()


class EdgeSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))

    def test_ca_marketing_Edge(self):
        driver = self.driver
        driver.get("https://qasvus.wixsite.com/ca-marketing/")
        self.driver.maximize_window()
        HP.delay1_3()

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        HP.delay1_5()

        # Filling in form
        driver.find_element(By.ID, "input_comp-ldls1eyf").send_keys(fake.email())
        driver.find_element(By.XPATH, "//button[contains(.,'Submit')]").click()
        HP.delay1_5()

        # Navigate to the webpage with CAPTCHA
        driver.get("https://qasvus.wixsite.com/ca-marketing/")

    def tearDown(self):
        self.driver.quit()


class FirefoxSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

    def test_ca_wordpress_firefox(self):
        driver = self.driver
        driver.get("https://qasvus.wixsite.com/ca-marketing/")
        self.driver.maximize_window()
        HP.delay1_3()

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        HP.delay1_5()

        # Filling in form
        driver.find_element(By.ID, "input_comp-ldls1eyf").send_keys(fake.email())
        driver.find_element(By.XPATH, "//button[contains(.,'Submit')]").click()
        HP.delay1_5()

        # Navigate to the webpage with CAPTCHA
        driver.get("https://qasvus.wixsite.com/ca-marketing/")

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
