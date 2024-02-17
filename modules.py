import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import logging.config
import time
import os
import glob
import requests
import re

class Modules:
    def __init__(self, driver=False) -> None:
        self.driver = driver
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
        })
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.Wait = WebDriverWait(driver, 30)

    def dataMatchColourPercentage(self, element) -> str:
        match element.value_of_css_property("Color"):
            case "rgb(0, 207, 131)":
                return "Human"
            case "rgb(250, 181, 21)":
                return "Unsure"
            case "rgb(255, 0, 0)":
                return "AI"
    def dataPercentageToWord(self, percentage) -> str:
        try:
            percentage = int(float(percentage))
        except:
            percentage = int(float(percentage.strip("%")))
        if percentage > 70:
            return "AI"
        elif percentage < 30:
            return "Human"
        else:
            return "Unsure"

    def dataHumanToAI(self, human_percentage) -> int:
        try:
            human_percentage = int(float(human_percentage))
        except:
            human_percentage = int(float(human_percentage.strip("%")))
        ai_percentage = 100 - int(float(human_percentage))
        return ai_percentage

    def doGetPath(self) -> list[str]:
        check_path = input("Please provide the path of the .txt file, or a folder containing txt files that you would like to check\n")
        if os.path.exists(check_path) == False:
            print("The path you provided does not exist")
            exit()
        if os.path.isfile(check_path):
            files_to_check = [check_path]
            print(f"The file that is going to be checked is: {files_to_check}")
        elif os.path.isdir(check_path):
            files_to_check = glob.glob(f"{check_path}\\*.txt")
            print("The files that are going to be checked are:")
            for fileCur in files_to_check:
                print(fileCur)
        return files_to_check
        
    def doDeleteElement(self, element: uc.webelement.WebElement):
        self.driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)
    
    def doWaitUntilText(self, xpath: str) -> uc.webelement.WebElement:
        self.Wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = self.driver.find_element(By.XPATH, xpath)
        self.Wait.until(EC.visibility_of(element))
        while element.text == "":
            time.sleep(0.5)
        return element
    
    def doScrollToElement(self, element: uc.webelement.WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        scroll_element_into_middle = """
        var viewPortHeight = Math.max(document.documentElement.clientHeight, window.innerHeight || 0);
        var elementTop = arguments[0].getBoundingClientRect().top;
        window.scrollBy(0, elementTop-(viewPortHeight/2));
        """
        self.driver.execute_script(scroll_element_into_middle, element)
        time.sleep(0.5)

    def doGetLatestVersion(self):
        url = f"https://api.github.com/repos/Nygosaki/AI-Writing-Detection/commits"
        response = requests.get(url)
        response.raise_for_status()  # Raise exception if invalid response
        commits = response.json()

        if commits:
            latest_commit = commits[0]
            message = latest_commit['commit']['message']

            # Search for version string in commit message
            match = re.search(r"Version: (\d+\.\d+\.\d+)", message)
            if match:
                return match.group(1)

        return None