import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import logging.config
import time
from PyQt6.QtCore import QCoreApplication, QThread
from PyPDF2 import PdfReader

from modules import Modules
from browse import Browse
from setup import Options
import getChromeVer

class Start:
    def __init__(self, Parent) -> None:
        self.options = Options()
        self.parent = Parent

        self.options.statesToOptions(self.parent.buttonStates)
        self.options.setCachedOptions()
        #TODO fix issujes


        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': True,
        })
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
    
    def begin(self, filesToCheck: list[str]):
        self.logger.info("Starting the program")

        if self.options.headless_mode:
            driver = uc.Chrome(options=self.options.chromeOptions, headless=True, version_main=int(getChromeVer.get_chrome_version().split(".")[0]))
        else: 
            driver = uc.Chrome(Options=self.options.chromeOptions)

        modules = Modules(driver)

        currentVer = modules.doGetLatestVersion()
        if not currentVer == self.options.version:
            print(f"!Please update the program to the latest version: {currentVer} at 'https://github.com/Nygosaki/AI-Writing-Detection'")

        time.sleep(1)
        
        for fileCur in filesToCheck:
            if fileCur.endswith('.pdf'):
                with open(fileCur, 'rb') as pdf_file:
                    reader = PdfReader(pdf_file)
                    textUnckecked = ''
                    for page in reader.pages:
                        textUnckecked += page.extract_text()
                    textUnckecked = textUnckecked.replace('\n', ' ')
            else:
                with open(fileCur, "r", encoding='utf-8') as check_file:
                    textUnckecked = check_file.read()
                    browse = Browse(driver, textUnckecked, fileCur)

            try:
                browse.doUndetectableAI()
                for k, v in {"GPTZERO": self.parent.ui.indicatorGptZero, "OPENAI": self.parent.ui.indicatorOpenAi,  "WRITER": self.parent.ui.indicatorWriter, "CROSSPLAG": self.parent.ui.indicatorCrossplag, "COPYLEAKS": self.parent.ui.indicatorCopyleaks, "SAPLING": self.parent.ui.indicatorSapling, "CONTENTATSCALE": self.parent.ui.indicatorContentAtScale, "ZEROGPT": self.parent.ui.indicatorZeroGpt}.items():
                    self.parent.ui.set_indicator_color(v, browse.Options.results[k])
                QCoreApplication.processEvents()
            except Exception as error:
                print(f"Error of type {type(error)} occurred while checking Undetectable AI")

            try:
                browse.doGrammica()
                self.parent.ui.set_indicator_color(self.parent.ui.indicatorGrammica, browse.Options.results["Grammica"])
                QCoreApplication.processEvents()
            except Exception as e:
                print(f"An error occurred while processing Grammica: {e}")

            try:
                browse.doWritefull()
                self.parent.ui.set_indicator_color(self.parent.ui.indicatorWritefull, browse.Options.results["Writefull"])
                QCoreApplication.processEvents()
            except Exception as e:
                print(f"An error occurred while processing Writefull: {e}")

            try:
                browse.doHive()
                self.parent.ui.set_indicator_color(self.parent.ui.indicatorHive, browse.Options.results["Hive"])
                QCoreApplication.processEvents()
            except Exception as e:
                print(f"An error occurred while processing Hive: {e}")

            try:
                browse.doScribbr()
                self.parent.ui.set_indicator_color(self.parent.ui.indicatorScribbr, browse.Options.results["Scribbr"])
                QCoreApplication.processEvents()
            except Exception as e:
                print(f"An error occurred while processing Scribbr: {e}")

            try:
                browse.doTypeset()
                self.parent.ui.set_indicator_color(self.parent.ui.indicatorTypeset, browse.Options.results["Typeset"])
                QCoreApplication.processEvents()
            except Exception as e:
                print(f"An error occurred while processing Typeset: {e}")
            
            self.options.results[f"{fileCur}"] = browse.Options.results
        print(self.options.results)
        self.parent.ui.plainTextEdit.setPlainText(str(self.options.results))
        driver.quit()

if __name__ == "__main__":
    m = Modules()
    filesToCheck = m.doGetPath()
    start = Start()
    start.begin(filesToCheck)

    exit()