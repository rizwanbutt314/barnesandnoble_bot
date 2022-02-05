import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

os.environ['WDM_LOG_LEVEL'] = '0'

BASE_URL = "https://www.barnesandnoble.com/h/books/browse"
EMAIL = "test@test.com"
SOCK_PROXY_HOST = "127.0.0.1"
SOCK_PROXY_PORT = "9050"


class Elements:

    MY_ACCOUNT_BTN = (
        By.XPATH, '//nav[@data-nav="mainNav"]//a[@id="navbarDropdown" and contains(text(), "My Account")]')
    SINGIN_BTN = (
        By.XPATH, '//nav[@data-nav="mainNav"]//a[contains(text(), "Sign In")]')

    SINGIN_IFRAME = (By.XPATH, '//iframe[@title="Sign in or Create an Account"]')
    SIGNIN_MODAL_TITLE = (
        By.XPATH, '//div[contains(@class, "modal-sign-in")]//h2[text()="Sign in or Create an Account"]')
    FORGOT_PASSWORD_BTN = (
        By.XPATH, '//div[contains(@class, "modal-sign-in")]//a[@id="loginForgotPassword"]')

    FORGOT_PASSWORD_IFRAME = (By.XPATH, '//iframe[@title="Password Assistance"]')
    FORGOT_PASSWORD_MODAL_TITLE = (
        By.XPATH, '//div[contains(@class, "modal-sign-in")]//h2[text()="Password Assistant"]')
    EMAIL_INPUT = (
        By.XPATH, '//form[@id="forgotPasswordForm"]//input[@id="email"]')
    RESET_PASSWORD_BTN = (
        By.XPATH, '//form[@id="forgotPasswordForm"]//button[@id="resetPwSubmit"]')

    ALERT_MSG = (
        By.XPATH, '//div[contains(@class, "modal-sign-in")]//aside[@id="passwordAssistantErr"]//em')


class Driver():

    def __init__(self, use_tor_sock_proxy=False):
        # Chrome options
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-logging')
        # Tor Sock Proxy
        if use_tor_sock_proxy:
            options.add_argument(f'--proxy-server=socks5://{SOCK_PROXY_HOST}:{SOCK_PROXY_PORT}')

        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), options=options)
        self.driver.maximize_window()

    def get(self, url):
        self.driver.get(url)

    def wait_for_element(self, elem, timeout=40):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(elem))

    def move_to_element(self, elem):
        self.wait_for_element(elem)
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element(*elem)).perform()

    def click(self, elem):
        self.wait_for_element(elem)
        self.move_to_element(elem)
        self.driver.find_element(*elem).click()

    def enter_text(self, elem, txt):
        self.wait_for_element(elem)
        self.move_to_element(elem)
        self.driver.find_element(*elem).send_keys(txt)

    def get_text(self, elem):
        self.wait_for_element(elem, timeout=15)
        return self.driver.find_element(*elem).text

    def switch_to_iframe(self, elem):
        self.wait_for_element(elem)
        self.driver.switch_to.frame(self.driver.find_element(*elem))

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()
