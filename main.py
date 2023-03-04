from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

urls = ["https://www.instagram.com/mdgspace/",
        "https://www.instagram.com/sdslabs/"]
main = open("main.md", "a", encoding='utf-8')


def loadMorePost(driver, number_of_more_loads):
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


for url in urls:
    driver.get(url)
    # load more post otherwise only some post are loaded by default
    loadMorePost(driver, 3)
    WebDriverWait(driver, timeout=15).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "._aagv img"))
    images = driver.find_elements(by=By.CSS_SELECTOR, value="._aagv img")
    main.write(f"{url}\n")
    for image in images:
        caption = image.get_attribute("alt")
        src = image.get_attribute("src")
        main.write(f"src:{src} caption: {caption}\n")
    main.write("\n\n\n")

driver.quit()
main.close()
