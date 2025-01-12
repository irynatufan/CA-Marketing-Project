from selenium import webdriver
from dotenv import load_dotenv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from threading import Thread
from BrowserStack import my_key
from faker import Faker

fake = Faker()

load_dotenv()
BROWSERSTACK_USERNAME = os.environ.get("BROWSERSTACK_USERNAME") or my_key.BROWSERSTACK_USERNAME
BROWSERSTACK_ACCESS_KEY = os.environ.get("BROWSERSTACK_ACCESS_KEY") or my_key.BROWSERSTACK_ACCESS_KEY
URL = os.environ.get("URL") or "https://hub.browserstack.com/wd/hub"
BUILD_NAME = "browserstack-Cross-Browser-test"

# Browser capabilities for cross-browser testing
capabilities = [
    {
        "browserName": "chrome",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "11",
        "buildName": "CrossBrowserTest",
        "sessionName": "Chrome Test - CA Marketing"
    },
    {
        "browserName": "firefox",
        "browserVersion": "latest",
        "os": "Windows",
        "osVersion": "11",
        "buildName": "CrossBrowserTest",
        "sessionName": "Firefox Test - CA Marketing"
    },
    {
        "browserName": "safari",
        "browserVersion": "latest",
        "os": "OS X",
        "osVersion": "Ventura",
        "buildName": "CrossBrowserTest",
        "sessionName": "Safari Test - CA Marketing"
    }
]

def get_browser_option(browser):
    switcher = {
        "chrome": ChromeOptions(),
        "firefox": FirefoxOptions(),
        "safari": SafariOptions(),
    }
    return switcher.get(browser, ChromeOptions())


def run_session(cap):
    bstack_options = {
        "osVersion": cap["osVersion"],
        "buildName": cap["buildName"],
        "sessionName": cap["sessionName"],
        "userName": BROWSERSTACK_USERNAME,
        "accessKey": BROWSERSTACK_ACCESS_KEY
    }
    if "os" in cap:
        bstack_options["os"] = cap["os"]
    options = get_browser_option(cap["browserName"].lower())
    if "browserVersion" in cap:
        options.browser_version = cap["browserVersion"]
    options.set_capability('bstack:options', bstack_options)
    driver = webdriver.Remote(
        command_executor=URL,
        options=options)

    try:
        # Step 1: Open the website
        driver.get("https://qasvus.wixsite.com/ca-marketing")
        driver.maximize_window()
        wait = WebDriverWait(driver, 10)

        # Step 2: Verify website title
        expected_title = "Home | CA Marketing"
        assert driver.title == expected_title, f"Title mismatch! Expected: {expected_title}, Got: {driver.title}"
        print("Website title verified successfully.")

        # Step 3: Click "Login"
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in']")))
        login_button.click()
        print("Clicked 'Log in'.")

        # Step 4: Click "Login" again
        second_login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in again']")))
        second_login_button.click()
        print("Clicked 'Log in' second time.")

        # Step 5: Click "Login with Email"
        login_with_email = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login with Email']")))
        login_with_email.click()
        print("Clicked 'Login with Email'.")

        # Step 6: Enter email and password
        email_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='email']")))
        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))

        email_field.send_keys("testuser@example.com")
        password_field.send_keys("TestPassword123")
        print("Entered email and password.")

        # Step 7: Click "I am not a robot" checkbox
        recaptcha_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='recaptcha-anchor']")))
        recaptcha_checkbox.click()
        print("Clicked 'I am not a robot' checkbox.")

        # Step 8: Click "Login" button
        final_login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
        final_login_button.click()
        print("Clicked 'Login' button.")

        time.sleep(5)  # Wait for navigation or success message

        # Verify login success (e.g., dashboard or welcome message)
        success_message = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[contains(text(),'Welcome')]")))
        assert success_message, "Login was unsuccessful."
        print("Login successful!")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        driver.quit()

# Run tests in parallel for all browsers
for cap in capabilities:
    Thread(target=run_session, args=(cap,)).start()

