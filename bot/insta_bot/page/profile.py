from selenium.webdriver.common.by import By

class ProfilePage:
    def __init__(self, driver) -> None:
        self.driver = driver

    def __imgs(self):
        return self.driver.find_elements(by=By.XPATH, value='//article[1]//img')
    
    # This may break 
    def __no_of_posts(self):
        return self.driver.find_element(by=By.XPATH, value='//header[1]//section[1]//ul[1]//li[1]/span/span')
    
    def __next_post(self):
        return self.driver.find_element(by=By.XPATH, value='//*[local-name() = "svg"][@aria-label="Next"]')
    
    # This may break
    def __content(self):
        img = self.driver.find_element(by=By.XPATH, value='//article[@role="presentation"][1]//img')
        src = img.get_attribute("src")
        caption_element = self.driver.find_element(by=By.XPATH, value='//article[@role="presentation"][1]//h1')
        caption = caption_element.text
        return {'src':src, 'caption':caption}

    # This may break
    def getPosts(self):
        try:
            posts = []
            no_of_posts = self.__no_of_posts().text
            imgs = self.__imgs()
            self.driver.execute_script("arguments[0].click();", imgs[0])
            count = 0
            while True:
                count = count+1
                post = self.__content()
                post['id'] = count
                posts.append(post)
                if count < int(no_of_posts):
                    next = self.__next_post()
                    next.click()
                else:
                    break
            return posts
        except:
            print("Expected break point: page/profile.py getPosts")
            self.driver._quit()