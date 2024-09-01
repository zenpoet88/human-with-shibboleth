

# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=relative-beyond-top-level
# pylint: disable=unused-argument
# pylint: disable=bare-except
# pylint: disable=too-many-return-statements

from time import sleep
import random

from faker import Faker
from faker.providers import person

# from soupsieve import select

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from ..utility.base_workflow import BaseWorkflow
from ..utility.webdriver_helper import WebDriverHelper

WORKFLOW_NAME = 'Moodle'
WORKFLOW_DESCRIPTION = 'Interact with Moodle'

DEFAULT_INPUT_WAIT_TIME = 2
MIN_WAIT_TIME = 2 # Minimum amount of time to wait after searching, in seconds
MAX_WAIT_TIME = 5 # Maximum amount of time to wait after searching, in seconds

def load():
    driver = WebDriverHelper()
    return MoodleBrowse(driver=driver)

class MoodleBrowse(BaseWorkflow):

    def __init__(self, driver, input_wait_time=DEFAULT_INPUT_WAIT_TIME):
        super().__init__(name=WORKFLOW_NAME, description=WORKFLOW_DESCRIPTION, driver=driver)
        self.username='jdh'
        self.password='jdhpass'
        self.user_roles = ['admin']
        self.first_time = True
        self.adminname='admin'
        self.adminpass='adminPass!1'
        self.fake = Faker()
        self.fake.add_provider(person)


    def action(self, extra=None):
        self.get_creds(extra)
        err = self.shib_sign_in()
        err = err or self.moodle_workflow()

        if err or random.random() < 0.2:
            print("... Decided to log out")
            sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
            print("... Stopping browser to force logout")
            self.driver.stop_browser() # restart browser for security!
        else:
            print("... Decided not to log out of moodle")
        print("Completed moodle workflow")

    # PRIVATE

    def get_creds(self, extra=None):
        self.user_roles = []

        i = 0
        while i < len(extra):
            if extra[i] == "passfile":
                with open(extra[i+1], encoding="utf-8") as file:
                    self.username = file.readline().strip()
                    self.password = file.readline().strip()
                i += 2
            elif extra[i] == "user_roles":
                self.user_roles=extra[i+1].split(',')
                i += 2
            else:
                i += 1


    def shib_sign_in(self) -> bool:
        # Navigate to moodle
        self.driver.driver.get('https://service.castle.os/moodle/auth/shibboleth/index.php')
        sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))


        try:
            print(f"... Trying to enter username '{self.username}'")

            search_element = self.driver.driver.find_element(By.ID, 'username') # username
            if search_element is None:
                print("... Could not find username field")
                return True

            search_element.send_keys(self.username)
            sleep(1)
            print(f"... Trying to enter password '{self.password}'")

            search_element = self.driver.driver.find_element(By.ID, 'password') # password
            if search_element is None:
                print("... Could not find username field")
                return True

            search_element.send_keys(self.password)

            sleep(1)
            print("... Trying to click login")

            sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
            search_element = self.driver.driver.find_element(By.TAG_NAME, 'button') # login button
            if search_element is None:
                print("... Could not find login button")
                return True

            ActionChains(self.driver.driver).move_to_element(
                    search_element).click(search_element).perform()

            sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
        except:
            print("... No login fields present, assuming we're already logged in")

        print("... Checking that Moodle Dashboard loaded")


        search_str1 = f"Hi, {self.username}"
        search_element1 = self.driver.driver.find_elements(By.XPATH,
                f"//*[contains(text(),'{search_str1}')]")
        search_str2 = "Dashboard"
        search_element2 = self.driver.driver.find_elements(By.XPATH,
                f"//h1[contains(text(),'{search_str2}')]")
        if len(search_element1) == 0 and len(search_element2) == 0:
            print("... Could not find Moodle Dashboard text element")
            return True

        if len(search_element1) == 0:
            search_element=search_element2[0]
        else:
            search_element=search_element1[0]

        if not search_str1 in search_element.text and not search_str2 in search_element.text:
            print(f"... Login failed with: {search_str1} "
                    f"and {search_str2} not in {search_element.text}")
            return True
        print(f"... Login successful with: {search_element.text}")
        return False


    def enrol_in_course(self) -> bool:
        self.driver.driver.get('https://service.castle.os/moodle/?redirect=0')
        sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))

        err = self.find_text_and_click('Special Topics: AI-Powered Cybersecurity')
        err = err or self.find_text_and_click('Enrol me in this course')
        err = err or self.find_id_and_click('id_submitbutton')

        return err

    def moodle_workflow(self) -> bool:
        self.driver.driver.get('https://service.castle.os/moodle/my/courses.php')
        sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))

        search_str = "not enrolled in any course"
        search_elements = self.driver.driver.find_elements(By.XPATH,
                f"//*[contains(text(),'{search_str}')]")

        err = False
        if len(search_elements) != 0:
            print("... Enrolling in a course")
            err = self.enrol_in_course()
        else:
            print("... already enrolled in a course!")

        err = err or self.browse_course()
        return err


    def browse_course(self) -> bool:
        err = False
        err = err or self.find_link_and_click(
                'https://service.castle.os/moodle/course/view.php?id=2')
        sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
        # go straight to course
        # print(f"Current url is {self.driver.driver.current_url}")
        #self.driver.driver.get('https://service.castle.os/moodle/course/view.php?id=2')
        #sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))

        pages_to_view = random.randint(1,3)

        for _ in range(pages_to_view):
            week_choice = random.randint(0,4)
            match week_choice:
                case 0: # Announcements
                    err = err or self.find_text_and_click('Announcements')
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
                    print("... Going back to courses page")
                    self.driver.driver.back()
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
                case 1: # Week 1
                    err = err or self.find_text_and_click('cgc talk')
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
                    err = err or self.browse_moodle_pdf()
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
                    print("... Going back to courses page")
                    self.driver.driver.back()
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
                case 2: # Week 2
                    err = err or self.find_text_and_click('RAMPART slides', link_type='a')
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
                case 3: # Week 3
                    err = err or self.find_text_and_click('week 3 lecture')
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
                    err = err or self.browse_moodle_pdf()
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
                    print("... Going back to courses page")
                    self.driver.driver.back()
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
                case 4: # Week 4
                    err = err or self.find_text_and_click('caldera slides', link_type='a')
                    sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))

        return err

    def browse_moodle_pdf(self):
        err = False
        if False:
            sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
            viewer = self.driver.driver.find_element(By.XPATH, "//html/body/embed")
            for _ in range(random.randint(0,14)):

                choice = random.randint(0,2)
                choice = 0
                match choice:
                    case 0:
                        print("... Trying page down key")
                        viewer.send_keys(Keys.PAGE_DOWN)
                        self.driver.driver.execute_script("window.scrollTo(0,250)")
                        sleep(10)
                    case 1:
                        print("... Trying page up key")
                        viewer.send_keys(Keys.PAGE_UP)
                    case 2:
                        print("... Trying home key")
                        viewer.send_keys(Keys.HOME)
                    case 3:
                        print("... Trying end key")
                        viewer.send_keys(Keys.END)
        sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
        return err


    def find_link_and_click(self, to_find: str, link_type:str = 'a' ) -> bool:

        print(f"... Trying to find link to {to_find}")
        search_element = self.driver.driver.find_element(By.XPATH,
                f"//{link_type}[contains(@href,'{to_find}')]")

        if search_element is None:
            print(f"... Could not find link to {to_find}.")
            return True

        text = search_element.text
        print(f"... Clicking {text}.")
        ActionChains(self.driver.driver).move_to_element(
                search_element).click(search_element).perform()
        print(f"... Successful click of {text}.")

        return False

    def find_text_and_click(self, to_find: str, link_type:str = '*' ) -> bool:

        print(f"... Trying to click {to_find}")
        search_element = self.driver.driver.find_element(By.XPATH,
                f"//{link_type}[contains(text(),'{to_find}')]")

        if search_element is None or not to_find in search_element.text:
            print(f"... Could not find {to_find}.")
            return True

        text = search_element.text
        print(f"... Clicking {text}.")
        ActionChains(self.driver.driver).move_to_element(
                search_element).click(search_element).perform()
        print(f"... Successful click of {text}.")

        return False


    def find_id_and_click(self, to_find: str) -> bool:
        search_element = self.driver.driver.find_element(By.ID, to_find)

        if search_element is None:
            print(f"### Could not find button id='{to_find}'")
            return True

        sleep(random.randrange(MIN_WAIT_TIME, MAX_WAIT_TIME))
        print(f"... Trying to click button id={to_find}")
        ActionChains(self.driver.driver).move_to_element(
                search_element).click(search_element).perform()

        return False
