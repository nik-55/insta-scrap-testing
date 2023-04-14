from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from os import getenv as os_getenv
from dotenv import load_dotenv
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from requests import get as requests_get


class BotConfig(webdriver.Chrome):
    _env = {}
    __enable_proxy = False

    def __init__(self) -> None:
        self.__setEnvironmentVariable()
        service = self.__configService()
        options = self.__configOptions()
        capabilities = None
        if self.__enable_proxy:
            capabilities = self.__setCapabilities()
        super().__init__(
            service=service, options=options, desired_capabilities=capabilities
        )
        self.__configWait(15)

    def __configOptions(self, display_browser=False):
        options = Options()
        options.add_argument("start-maximized")
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
        self._env["USERNAME"] = os_getenv("USERNAME") or ""
        self._env["PASSWORD"] = os_getenv("PASSWORD") or ""
        self._env["INSTA_BASE_URL"] = os_getenv("INSTA_BASE_URL")

    def __setCapabilities(self):
        # Configure Proxy
        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        # Free Public Proxy
        proxy.http_proxy = "134.209.29.120:3128"
        capabilities = DesiredCapabilities.CHROME
        proxy.add_to_capabilities(capabilities=capabilities)
        response = requests_get(
            "http://ipinfo.io/json", proxies={"http": proxy.http_proxy}
        )
        print(f"using the proxy {response.text}")
        return capabilities

    def _quit(self):
        self.quit()

    def _open(self, url):
        self.get(url)
