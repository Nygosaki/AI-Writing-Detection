from typing import Any
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import logging
import logging.config
import time
import os
import glob
import sys
from modules import Modules
from setup import Options

class Browse:
    def __init__(self, driver: uc.Chrome, textUnckecked: str, fileCur: str) -> None:
        self.driver = driver
        self.textUnckecked = textUnckecked
        self.fileCur = fileCur
        self.Options = Options()
        self.Modules = Modules(driver)
        self.Wait = WebDriverWait(driver, 30)

        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
        })
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        pass
     
    def doUndetectableAI(self):
        try:
            self.logger.info("Checking Undetectable AI")
            if not self.Options.toggleUndetectableAI:
                return
            self.driver.get('https://undetectable.ai/')
            time.sleep(1)
            self.Wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="paste"]')))
            textbox = self.driver.find_element(By.XPATH, '//*[@id="paste"]')
            textbox.send_keys(self.textUnckecked)
            time.sleep(1)
            banner = self.driver.find_element(By.XPATH, '//*[@id="topBanner"]')
            self.Modules.doDeleteElement(banner)
            menu = self.driver.find_element(By.XPATH, '//*[contains(text(), "UNDETECTABLE AI")]/../../../..')
            self.Modules.doDeleteElement(menu)
            try:
                element = self.driver.find_element(By.XPATH, '//*[contains(text(), "Skip")]')
                element.click()
            except:
                pass
            button = self.driver.find_element(By.XPATH, '//*[@id="bCheckForAi"]')
            ActionChains(self.driver).scroll_to_element(button).perform()
            button.click()
            time.sleep(2)
            for x in ["GPTZERO", "OPENAI", "WRITER", "CROSSPLAG", "COPYLEAKS", "SAPLING", "CONTENTATSCALE", "ZEROGPT"]:
                self.Options.results[x] = self.Modules.dataMatchColourPercentage(self.driver.find_element(By.XPATH, f'//*[contains(text(), "{x}")]/../button/*/*'))
        except Exception as error:
            self.logger.exception(f"Error of type {type(error)} occurred while checking Undetectable AI")
            self.logger.debug(error)
        finally:
            self.Options.flagFinishedUndetectableAI = True

    def doGrammica(self):
        try:
            self.logger.info("Checking Grammica")
            if not self.Options.toggleGrammica:
                self.logger.info("Skipping Grammica")
                return
            self.driver.get("https://grammica.com/ai-detector")
            time.sleep(1)
            try:
                element = self.driver.find_element(By.XPATH, '//*[@aria-label="Consent"]')
                element.click()
            except:
                pass
            self.Wait.until(EC.presence_of_element_located((By.XPATH, '//*[@oninput="countText()"]')))
            textbox = self.driver.find_element(By.XPATH, '//*[@oninput="countText()"]')
            textbox.send_keys(self.textUnckecked)
            time.sleep(1)
            percentageAI = self.Modules.doWaitUntilText('//*[@id="fake-percentage"]').text
            self.Options.results["Grammica"] = self.Modules.dataPercentageToWord(percentageAI)
        except Exception as error:
            self.logger.exception(f"Error of type {type(error)} occurred while checking Grammica")
            self.logger.debug(error)
        finally:
            self.Options.flagFinishedGrammica = True