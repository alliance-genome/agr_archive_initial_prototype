from selenium import webdriver


class Browser(object):

    base_url = 'http://localhost:5000'
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)

    def close(self):
        self.driver.quit()

    def visit(self, location=''):
        url = self.base_url + location
        self.driver.get(url)

    def find_by_id(self, selector):
        return self.driver.find_element_by_id(selector)

    def find_all_by_class(self, selector):
        return self.driver.find_elements_by_class_name(selector)

    def find_by_link_text(self, selector):
        return self.driver.find_element_by_link_text(selector)
