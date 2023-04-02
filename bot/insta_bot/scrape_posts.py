from selenium.webdriver.common.by import By
from ..bot_config import BotConfig
from .page.login import LoginPage
from .page.profile import ProfilePage
import time

class ScrapePost(BotConfig):
    def __init__(self) -> None:
        super().__init__()
        self._baseURL = self._env['INSTA_BASE_URL']

    def login(self):
        self._open(self._baseURL)
        login_page = LoginPage(self)
        login_page.login()
        time.sleep(5)

    def getPosts(self,username):
        self.login()
        self._open(f'{self._baseURL}/{username}')
        time.sleep(5)
        profile_page = ProfilePage(self)
        posts = profile_page.getPosts()
        return posts