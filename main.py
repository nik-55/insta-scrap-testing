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

# Opening the main.md file
main = open("main.md", "a", encoding='utf-8')


# Function to load more post without logged in user
def loadMorePostWithoutLogin(driver, number_of_more_loads):
    i = 1
    n = number_of_more_loads
    while i <= n:
        try:
            WebDriverWait(driver, timeout=15).until(
                lambda d: d.find_element(By.CSS_SELECTOR, "._aacl._aaco._aacw._aad3._aad6._aadb"))
            button = driver.find_element(
                by=By.CSS_SELECTOR, value="._aacl._aaco._aacw._aad3._aad6._aadb")
            driver.execute_script("arguments[0].click();", button)
            time.sleep(10)
            i += 1
        except:
            break


# Function to login to instagram
def login(driver, username, password):
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


# Function to load more post with logged in user
def loadMorePostWithLogin(driver):
    SCROLL_PAUSE_TIME = 7
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


# Without login upto 30 posts can be scrapped
# driver.get("https://instagram.com")
# login(driver, USERNAME, PASSWORD)


for url in urls:
    username_from_url = url.split(".com/")[1].replace("/", "")
    driver.get(url)
    loadMorePostWithoutLogin(driver, 2)
    # loadMorePostWithLogin(driver)
    WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "._aagv img"))
    images = driver.find_elements(by=By.CSS_SELECTOR, value="._aagv img")
    main.write(f"# {username_from_url}\n")
    for index, image in enumerate(images):
        caption = image.get_attribute("alt")
        src = image.get_attribute("src")
        main.write(f"{index+1}. `src`: {src} and `caption`: {caption}\n")
    main.write("\n\n\n")

driver.quit()
main.close()
