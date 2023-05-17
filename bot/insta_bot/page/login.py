from selenium.webdriver.common.by import By


class LoginPage:
    def __init__(self, driver) -> None:
        self.driver = driver

    def __username(self):
        return self.driver.find_element(
            by=By.XPATH, value='//input[@aria-label="Phone number, username, or email"]'
        )

    def __password(self):
        return self.driver.find_element(
            by=By.XPATH, value='//input[@aria-label="Password"]'
        )

    def _login_btn(self):
        return self.driver.find_element(
            by=By.XPATH, value='//button[contains(.,"Log in")]'
        )

    def login(self):
        self.__username().send_keys(self.driver._env["USERNAME"])
        self.__password().send_keys(self.driver._env["PASSWORD"])
        self._login_btn().click()
