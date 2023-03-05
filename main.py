from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
from dotenv import dotenv_values

# Config the env variables
config = dotenv_values(".env")
USERNAME = config['USERNAME']
PASSWORD = config['PASSWORD']

# Initialising driver
service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Different Public insta account urls
urls = ["https://www.instagram.com/mdgspace/",
        "https://www.instagram.com/sdslabs/"]

# Opening the insta_post.md file
insta_post = open("insta_post.md", "a", encoding='utf-8')


# show more posts without logged in user
def show_more_posts_without_login(driver):
    try:
        WebDriverWait(driver, timeout=15).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "._aacl._aaco._aacw._aad3._aad6._aadb"))
        button = driver.find_element(
            by=By.CSS_SELECTOR, value="._aacl._aaco._aacw._aad3._aad6._aadb")
        driver.execute_script("arguments[0].click();", button)
        time.sleep(10)
    except:
        return


# Load Posts without logged in user
def load_posts_without_login(driver, url, show_more_post):
    driver.get(url)
    if show_more_post:
        show_more_posts_without_login(driver)
    WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "._aagv img"))
    images = driver.find_elements(by=By.CSS_SELECTOR, value="._aagv img")
    for index, image in enumerate(images):
        caption = image.get_attribute("alt")
        src = image.get_attribute("src")
        insta_post.write(f"{index+1}. `src`: {src} and `caption`: {caption}\n")


# Login to instagram
def login(driver, username, password):
    driver.get("https://instagram.com")
    WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "._aa4b._add6._ac4d"))
    inputs = driver.find_elements(
        by=By.CSS_SELECTOR, value="._aa4b._add6._ac4d")
    inputs[0].send_keys(username)
    inputs[1].send_keys(password)
    WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abcm"))
    btns = driver.find_elements(
        by=By.CSS_SELECTOR, value="._ab8w._ab94._ab99._ab9f._ab9m._ab9p._abcm")
    btns[3].click()
    time.sleep(10)


status_logged_in = False


# show more posts with logged in user
def show_more_posts_with_login(driver):
    SCROLL_PAUSE_TIME = 5
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Load posts with logged in user
def load_posts_with_login(driver, url):
    global status_logged_in
    if not status_logged_in:
        login(driver, USERNAME, PASSWORD)
        status_logged_in = True
    driver.get(url)
    show_more_posts_with_login(driver)
    WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "._aagv img"))
    images = driver.find_elements(by=By.CSS_SELECTOR, value="._aagv img")
    for index, image in enumerate(images):
        driver.execute_script("arguments[0].click();", image)
        WebDriverWait(driver, timeout=5).until(
            lambda d: d.find_element(By.CSS_SELECTOR, "._aacl._aaco._aacu._aacx._aad7._aade"))
        caption = (driver.find_element(
            by=By.CSS_SELECTOR, value="._aacl._aaco._aacu._aacx._aad7._aade")).text
        src = image.get_attribute("src")
        close_btn = driver.find_element(
            by=By.CSS_SELECTOR, value="svg.x1lliihq.x1n2onr6")
        close_btn.click()
        insta_post.write(f"{index+1}. `src`: {src} and `caption`: {caption}\n")


# Scrape the different accounts
for url in urls:
    username_from_url = url.split(".com/")[1].replace("/", "")
    insta_post.write(f"# {username_from_url}\n")
    load_posts_without_login(driver, url, True)
    # load_posts_with_login(driver, url)
    insta_post.write("\n\n\n")


driver.quit()
insta_post.close()
