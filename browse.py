from typing import Any
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import logging
import logging.config
import time
from modules import Modules
from setup import Options

class Browse:
    def __init__(self, driver: uc.Chrome, textUnckecked: str, fileCur: str) -> None:
        self.driver = driver
        self.textUnckecked = textUnckecked
        self.fileCur = fileCur
        self.Options = Options()
        self.Options.loadCachedOptions()
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
                self.logger.info("Skipping Undetectable AI")
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
                while self.driver.find_element(By.XPATH, f'//*[contains(text(), "{x}")]/../button/*/*').value_of_css_property("Color") == "rgb(172, 178, 185)":
                    time.sleep(0.5)
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
    
    def doWritefull(self):
        try:
            self.logger.info("Checking Writefull")
            if not self.Options.toggleWritefull:
                self.logger.info("Skipping Writefull")
                return
            self.driver.get("https://x.writefull.com/gpt-detector")
            time.sleep(1)
            self.Wait.until(EC.presence_of_element_located((By.XPATH, '//*[@placeholder="Enter text here."]')))
            textbox = self.driver.find_element(By.XPATH, '//*[@placeholder="Enter text here."]')
            textbox.send_keys(self.textUnckecked)
            button = self.driver.find_element(By.XPATH, '//*[@class="inline-flex justify-center items-center rounded-md text-sm font-semibold py-3 px-4 text-white bg-slate-900 hover:bg-slate-800 text-base font-medium px-4 py-3"]')
            button.click()
            time.sleep(1)
            textUnprocessed = self.Modules.doWaitUntilText('//*[@class="text-2xl ml-4"]').text
            percentageAI = textUnprocessed.split("%", 1)[0]
            self.Options.results["Writefull"] = self.Modules.dataPercentageToWord(percentageAI)
        except Exception as error:
            self.logger.exception(f"Error of type {type(error)} occurred while checking Writefull")
            self.logger.debug(error)
        finally:
            self.Options.flagFinishedWritefull = True

    def doHive(self):
        try:
            self.logger.info("Checking Hive")
            if not self.Options.toggleHive:
                self.logger.info("Skipping Hive")
                return
            self.driver.get("https://hivemoderation.com/ai-generated-content-detection")
            time.sleep(1)
            self.Wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Edit")]/..')))
            self.Modules.doDeleteElement(self.driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[1]'))
            buttonEdit = self.driver.find_element(By.XPATH, '//*[contains(text(), "Edit")]/..')
            self.Modules.doScrollToElement(buttonEdit)
            buttonEdit.click()
            textbox = self.driver.find_element(By.XPATH, '//*[@id="input_area_only"]/textarea')
            textbox.send_keys(self.textUnckecked)
            button = self.driver.find_element(By.XPATH, '//*[contains(text(), "Submit")]/..')
            button.click()
            time.sleep(1)
            # self.driver.save_screenshot("screenshot.png")
            percentageAI = self.Modules.doWaitUntilText('//*[contains(text(), "The input is: ")]/../div/span').text
            self.Options.results["Hive"] = self.Modules.dataPercentageToWord(percentageAI)
        except Exception as error:
            self.logger.exception(f"Error of type {type(error)} occurred while checking Hive")
            self.logger.debug(error)
        finally:
            self.Options.flagFinishedHive = True
    
    def doScribbr(self):
        try:
            self.logger.info("Checking Scribbr")
            if not self.Options.toggleScribbr:
                self.logger.info("Skipping Scribbr")
                return
            self.driver.get("https://www.scribbr.com/ai-detector/")
            time.sleep(1)
            self.Wait.until(EC.presence_of_element_located((By.XPATH, '//*[@placeholder="Paste your text in here. For a good result, we recommend between 25 and 500 words."]')))
            time.sleep(1)
            textbox = self.driver.find_element(By.XPATH, '//*[@placeholder="Paste your text in here. For a good result, we recommend between 25 and 500 words."]')
            try:
                element = self.driver.find_element(By.XPATH, '//*[contains(text(), "Accept all & close")]')
                element.click()
            except:
                pass
            textbox.send_keys(self.textUnckecked)
            button = self.driver.find_element(By.XPATH, '//*[@id="aiDetectorButton"]')
            button.click()
            time.sleep(1)
            percentageAI = self.Modules.doWaitUntilText('//*[contains(text(), "Chance that your text is generated by AI")]/../span[1]').text
            self.Options.results["Scribbr"] = self.Modules.dataPercentageToWord(percentageAI)
        except Exception as error:
            self.logger.exception(f"Error of type {type(error)} occurred while checking Scribbr")
            self.logger.debug(error)
        finally:
            self.Options.flagFinishedScribbr = True

    def doTypeset(self):
        try:
            self.logger.info("Checking Typeset")
            if not self.Options.toggleTypeset:
                self.logger.info("Skipping Typeset")
                return
            self.driver.get("https://typeset.io/ai-detector")
            time.sleep(1)
            self.Wait.until(EC.presence_of_element_located((By.XPATH, '//button[@value="NON_SCIENTIFIC"]')))
            buttonNonScientific = self.driver.find_element(By.XPATH, '//button[@value="NON_SCIENTIFIC"]')
            buttonNonScientific.click()
            textbox = self.driver.find_element(By.XPATH, '//*[@aria-label="Rich Text Editor. Editing area: textEditor"]')
            textbox.send_keys(self.textUnckecked)
            time.sleep(1)
            button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Analyse")][1]')
            try:
                button.click()
            except:
                self.driver.execute_script("arguments[0].click()", button)
            time.sleep(1)
            percentageAI = self.Modules.doWaitUntilText('//h3[@class="my-2 text-2xl font-semibold"]').text
            time.sleep(1)
            self.Options.results["Typeset"] = self.Modules.dataPercentageToWord(self.driver.find_element(By.XPATH, '//h3[@class="my-2 text-2xl font-semibold"]').text)
        except Exception as error:
            self.logger.exception(f"Error of type {type(error)} occurred while checking Typeset")
            self.logger.debug(error)
        finally:
            self.Options.flagFinishedTypeset = True