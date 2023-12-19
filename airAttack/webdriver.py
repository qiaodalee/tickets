from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class WebDriver:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        chrome_options.add_argument("--enable-logging")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        serice = Service(executable_path='./chromedriver-win64/chromedriver.exe')
        self.driver = webdriver.Chrome(
            service=serice, 
            options=chrome_options)
        self.log = None

    def open(self, url):
        self.driver.get(url)
        return self.load_page(60, '//button[@data-e2e-test-id="search"]')

    def quit(self):
        self.driver.close()

    def load_page(self, interval, expected_conditions):
        wait = WebDriverWait(self.driver, interval)
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, expected_conditions)))
            return None
        except Exception as error: 
            return error
    
    def get_logs(self):
        return self.driver.get_log("performance")
    
    def find(self, by, path):
        try:
            return self.driver.find_element(by, path)
        except Exception as error:
            return None
        
    def click_event(self, by, path):
        try:
            element = self.find(by, path)
            element.click()
            return None
        except Exception as error:
            return error

    def input_event(self, by, path, input):
        input_element = self.find(by, path)   
        for i in range(8): 
            input_element.send_keys(Keys.BACK_SPACE)
        for date in input:
            input_element.send_keys(date)
        input_element.send_keys(Keys.ENTER)
        return
    
    def scroll_page(self, scroll_script):
        self.driver.execute_script(scroll_script)
        return

    def refreshPage(self):
        self.driver.refresh()

    def element_hidden(self, script):
        self.driver.execute_script(script)
