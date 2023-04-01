from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from os import getenv as os_getenv
from dotenv import load_dotenv

class BotConfig(webdriver.Chrome):
    __env = {}
    def __init__(self) -> None:
        self.__setEnvironmentVariable()
        service = self.__configService()
        options = self.__configOptions(True)
        super().__init__(service=service,options=options)
        self.__configWait(5)
        self._open('https://github.com/mdgspace')

    def __configOptions(self, display_browser):
        options = Options()
        options.add_argument('start-maximized')
        if display_browser:
            options.add_argument("--headless")
        return options
    
    def __configService(self):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        return service
    
    def __configWait(self, time_to_wait):
        # time_to_wait in seconds
        self.implicitly_wait(time_to_wait)

    def __setEnvironmentVariable(self):
        load_dotenv(override=True)
        self.__env['USERNAME'] = os_getenv('USERNAME') or ""
        self.__env['PASSWORD'] = os_getenv('PASSWORD') or ""

    def _quit(self):
        self.quit()
    
    def _open(self, url):
        self.get(url)
