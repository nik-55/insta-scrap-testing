from selenium.webdriver.common.by import By
from ..bot_config import BotConfig
from .page.login import LoginPage

class ScrapePost(BotConfig):
    def __init__(self) -> None:
        super().__init__()
        self._baseURL = self._env['INSTA_BASE_URL']

    def login(self):
        self._open(self._baseURL)
        login_page = LoginPage(self)
        login_page.login()

    def getPosts(self,username):
        self.login()
        self._open(f'{self._baseURL}/{username}')
        posts=[]
        return posts