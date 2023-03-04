from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

service = ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

urls = ["https://www.instagram.com/mdgspace/",
        "https://www.instagram.com/sdslabs/"]
main = open("main.md", "a", encoding='utf-8')

for url in urls:
    driver.get(url)
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
