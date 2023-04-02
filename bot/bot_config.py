from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from os import getenv as os_getenv
from dotenv import load_dotenv

class BotConfig(webdriver.Chrome):
    _env = {}
    def __init__(self) -> None:
        self.__setEnvironmentVariable()
        service = self.__configService()
        options = self.__configOptions()
        super().__init__(service=service,options=options)
        self.__configWait(15)

    def __configOptions(self, display_browser=False):
        options = Options()
        options.add_argument('start-maximized')
        if not display_browser:
            options.add_argument("--headless=new")
        return options
    
    def __configService(self):
        service = ChromeService(executable_path=ChromeDriverManager().install())
        return service
    
    def __configWait(self, time_to_wait):
        # time_to_wait in seconds
        self.implicitly_wait(time_to_wait)

    def __setEnvironmentVariable(self):
        load_dotenv(override=True)
        self._env['USERNAME'] = os_getenv('USERNAME') or ""
        self._env['PASSWORD'] = os_getenv('PASSWORD') or ""
        self._env['INSTA_BASE_URL'] = os_getenv("INSTA_BASE_URL") 


    def _quit(self):
        self.quit()
    
    def _open(self, url):
        self.get(url)
