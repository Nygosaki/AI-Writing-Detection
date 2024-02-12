import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging
import logging.config
import time

from modules import Modules
from browse import Browse
from setup import Options
import getChromeVer

Options = Options()
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting the program")
    if Options.headless_mode:
        driver = uc.Chrome(Options=Options.chromeOptions, headless=True, version_main=int(getChromeVer.get_chrome_version().split(".")[0]))
    else: 
        driver = uc.Chrome(Options=Options.chromeOptions)

    Modules = Modules(driver)

    time.sleep(1)
    filesToCheck = Modules.doGetPath()
    for fileCur in filesToCheck:
        logging.info(f"Currently checking: {fileCur}")
        with open (fileCur, "r", encoding='utf-8') as check_file:
            textUnckecked = check_file.read()
        logger.info(f"Checking {fileCur}")

        Browse = Browse(driver, textUnckecked, fileCur)

        Browse.doUndetectableAI()
        Browse.doGrammica()
        Browse.doWritefull()
        Browse.doHive()
        Browse.doScribbr()
        Options.results[f"{fileCur}"] = Browse.Options.results
    print(Options.results)
    driver.quit()