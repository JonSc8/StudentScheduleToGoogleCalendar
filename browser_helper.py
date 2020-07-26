from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from course import Course

ID_FIELD = "input[name=u_id]"
PASSWORD_FIELD = "input[name=u_pw]"

class BrowserHelper:

    def __init__(self, url):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=self.chrome_options())
        self.driver.get(url)
    
    def chrome_options(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--profile-directory=Default')

        return chrome_options

    def login(self, username, password):
        print("Logging in to SSOL")
        id_field = self.driver.find_element_by_css_selector(ID_FIELD)
        password_field = self.driver.find_element_by_css_selector(PASSWORD_FIELD)

        id_field.send_keys(username)
        password_field.send_keys(password)

        self.driver.find_element_by_name("submit").click()

    def get_student_schedule(self):
        print("Getting student schedule")
        self.driver.find_element_by_partial_link_text("Student Schedule").click()

        schedule_table = self.driver.find_element_by_xpath("//*[@id=\"Content\"]/table[1]/tbody")
        return schedule_table
        
        
        

