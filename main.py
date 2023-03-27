load_time = 10 # How many seconds does your computer take to generate the result with each tool? Increase this if you are getting "unavaible" on most of the tools. YOu can find the exact time by enabling debug mode and timing it with your phone.
debug_mode = False # Is debug mode enabled?


# ---------------------DO NOT CHANGE ANYTHING BELLOW HERE-------------------------
# --------------------------------------------------------------------------------
# -------------------------------IMPORTS------------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import undetected_chromedriver as uc
import time
if debug_mode:
    import logging
    import logging.config
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
    })


# ------------------------------General Setup-------------------------------------
#TODO token handling 
# Opens file to be checked
with open ("to check.txt", "r", encoding='utf-8') as check_file:
    text_to_check = check_file.read()
results = dict()
print("\nThis is the text that you have provided in 'to check.txt' which we will be checking.\n")
print(text_to_check)

# Sets up debug mode
if debug_mode:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)


# ----------------------------Selenium Setup-------------------------------------
"""service = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=service)"""
# Sets up the driver
driver = uc.Chrome
# Sets up the options
options = Options()
if debug_mode == False:
    options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--log-level=3')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome(options=options)
# Defines Selenium Misc Options
wait = WebDriverWait(driver, load_time)
actions = ActionChains(driver)


# -----------------------------Define Functions-----------------------------------
class element_is_visible(object):
    # checks if the CSS property visible is enabled
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            element = self.locator
            return element.value_of_css_property("visibility") == "visible"
        except StaleElementReferenceException:
            return False

def wait_until_element_text(element_xpath):
    # Waits until a certain element appears & has text, and then returns that element
    if debug_mode:
        logger.info(f"Started waiting for {element_xpath}")
    wait.until(EC.presence_of_element_located((By.XPATH, element_xpath)))
    element = driver.find_element(By.XPATH, element_xpath)
    wait.until(EC.visibility_of(element))
    wait.until(element_is_visible(element))
    while element.text == "":
        time.sleep(0.5)
    if debug_mode:
        logger.info(f"Finished Waiting for {element_xpath}")
    return element

def use_tool(box_xpath, button_xpath):
    # Inputs text & presses button
    box = driver.find_element(by=By.XPATH, value=box_xpath)
    box.send_keys(text_to_check)
    time.sleep(1)
    button = driver.find_element(by=By.XPATH, value=button_xpath)
    try:
        wait.until(EC.element_to_be_clickable(button))
    except:
        pass
    driver.execute_script("arguments[0].scrollIntoView();", button)
    button.click()

def human_to_ai_percentage(human_percentage):
    ai_percentage = 100 - int(human_percentage)
    return ai_percentage
# --------------------------Checks Text with Tools that don't have a API--------------------


# https://grammica.com/ai-detector
try:
    driver.get("https://grammica.com/ai-detector")
    grammica_box = driver.find_element(by=By.XPATH, value='//*[@id="text"]')
    grammica_box.send_keys(text_to_check)
    grammica_ai_percentage = wait_until_element_text('//*[@id="fake-percentage"]').text
    results["Grammica AI Detector"] = f"{grammica_ai_percentage} probability of AI Written"
    if grammica_ai_percentage == "":
        results["Grammica AI Detector"] = "unavaible"
        if debug_mode:
            logger.warning("Grammica AI Detector Unavaible")
except:
    results["Grammica AI Detector"] = "unavaible/error"
    if debug_mode:
        logger.exception("Grammica AI Detector Exception")

try:
    characters = driver.find_element(by=By.XPATH, value='//*[@id="edited_characters"]').text
    words = driver.find_element(by=By.XPATH, value='//*[@id="edited_words"]').text
    sentences = driver.find_element(by=By.XPATH, value='//*[@id="edited_sentence"]').text
    characters_int = int(characters)
    words_int = int(words)
    sentences_int = int(sentences)
    print(f"|\n| Total Characters: {characters} | Total Words: {words} | Total Sentences: {sentences} |\n|")
except:
    print(f"|\n| Total Characters: ERROR | Total Words: ERROR | Total Sentences: ERROR |\n|")
    if debug_mode:
        logger.exception("Word Counter Exception")
print("----------------------------------------------------------------------------")
print(results)


# https://aiwritingcheck.org/
if words_int > 100 and words_int < 400:
    try:
        driver.get("https://aiwritingcheck.org/")
        use_tool('//*[@id="js-textBox"]', '//*[@id="js-submitButton"]')
        time.sleep(load_time)
        if driver.find_element(by=By.XPATH, value='//*[@id="js-human"]/h3/div/b').is_displayed():
            results["AI Writing Check"] = "Written by Human"
        elif driver.find_element(by=By.XPATH, value='//*[@id="js-ai"]/h3/div/b').is_displayed():
            results["AI Writing Check"] = "Written by AI"
        else:
            results["AI Writing Check"] = "unavaible"
            if debug_mode:
                logger.warning("AI Writing Check Unavaible")
    except:
        results["AI Writing Check"] = "unavaible/error"
        if debug_mode:
            logger.exception("AI Writing Check Exception")
    print("----------------------------------------------------------------------------")
    print(results)
else:
    print("----------------------------------------------------------------------------")
    print("AI Writing Check by Quill.org & CommonLit was skipped due to character limits.")


# https://writer.com/ai-content-detector/
if characters_int < 1500:
    try:
        driver.get("https://writer.com/ai-content-detector/")
        use_tool('//*[@placeholder="Paste text or write here"]', '//*[@class="dc-btn-gradient ai-content-detector-submit"]')
        writedetector_human_written = wait_until_element_text('//*[@id="ai-percentage"]').text
        if writedetector_human_written == "":
            results["WRITER AI Detector"] = "unavaible"
            if debug_mode:
                logger.warning("WRITER AI Detecotr Unavaible")
        else:
            writedetector_ai_written = human_to_ai_percentage(writedetector_human_written)
            results["WRITER AI Detector"] = f"{writedetector_ai_written}% probability of AI written"
    except:
        results["WRITER AI Detector"] = "unavaible/error"
        if debug_mode:
            logger.exception("WRITER AI Detector Exception")
    print("----------------------------------------------------------------------------")
    print(results)
else:
    print("----------------------------------------------------------------------------")
    print("WRITER AI Content Detector was skipped due to character limits.")


# https://www.zerogpt.com/
try:
    driver.get("https://www.zerogpt.com/")
    use_tool('//*[@id="textArea"]', '//*[@class="scoreButton"]')
    zerogpt_result = wait_until_element_text('//*[@class="result-container margin-v-15"]/div/span').text
    if zerogpt_result == "":
        results["ZeroGPT"] = "unavaible"
        if debug_mode:
            logger.warning("ZeroGPT Unavaible")
    else:
        results["ZeroGPT"] = zerogpt_result
except:
    results["ZeroGPT"] = "unavaible/error"
    if debug_mode:
        logger.exception("ZeroGPT Exception")
print("----------------------------------------------------------------------------")
print(results)

# https://contentatscale.ai/ai-content-detector/
if characters_int < 25000:
    try:
        driver.get("https://contentatscale.ai/ai-content-detector/")
        try:
            use_tool('//*[@name="content"]', '//*[@class="site-btn-secondry-lg check-ai-score"]')
        except:
            logger.warning("Could not use Selenium Click ContentAtScale")
            driver.execute_script('arguments[0].click();', driver.find_element(by=By.XPATH, value='//*[@class="site-btn-secondry-lg check-ai-score"]'))
            pass
        contentatscale_result = wait_until_element_text('//*[@class="text-center score-message"]').text
        if contentatscale_result == "":
            results["ContentAtScale AI Detector"] = "unavaible"
        else:
            results["ContentAtScale AI Detector"] = contentatscale_result
    except:
        results["ContentAtScale AI Detector"] = "unavaible/error"
        if debug_mode:
            logger.exception("ContentAtScale AI Detector Exception")
    print("----------------------------------------------------------------------------")
    print(results)
else:
    print("----------------------------------------------------------------------------")
    print("ContentAtScale AI Detector was skipped due to character limit.")

# https://x.writefull.com/gpt-detector
try:
    driver.get("https://x.writefull.com/gpt-detector")
    use_tool('//*[@placeholder="Enter text here."]', '//*[@class="inline-flex justify-center items-center rounded-md text-sm font-semibold py-3 px-4 text-white bg-slate-900 hover:bg-slate-800 text-base font-medium px-4 py-3"]')
    writefull_result = wait_until_element_text('//*[@class="text-2xl ml-4"]').text
    if writefull_result == "":
        results["WriteFull"] = "unavaible"
        if debug_mode:
            logger.warning("Writefull Unavaible")
    else:
        results["WriteFull"] = writefull_result
except:
    results["WriteFull"] = "unavaible/error"
    if debug_mode:
        logger.exception("WriteFull Exception")
print("----------------------------------------------------------------------------")
print(results)

# https://hivemoderation.com/ai-generated-content-detection
if characters_int > 750 and characters_int < 8192:
    try:
        driver.get("https://hivemoderation.com/ai-generated-content-detection")
        time.sleep(2)
        hivemoderation_clear_button = driver.find_element(by=By.XPATH, value='//*[@class="MuiButtonBase-root MuiButton-root jss66 jss396 jss68 jss214 MuiButton-text"]')
        try:
            wait.until(EC.element_to_be_clickable(hivemoderation_clear_button))
        except:
            pass
        driver.execute_script("arguments[0].scrollIntoView();", hivemoderation_clear_button)
        hivemoderation_clear_button.click()
        use_tool('//*[@class="jss211"]', '//*[@class="MuiButtonBase-root MuiButton-root jss66 jss242 jss69 MuiButton-text"]')
        hivemoderation_result = wait_until_element_text('//*[@class="MuiTypography-root jss379 MuiTypography-subtitle1"]/span').text
        if hivemoderation_result == "":
            results["HiveModeration"] = "unavaible"
            if debug_mode:
                logger.warning("HiveModeration Unavaible")
        else:
            results["HiveModeration"] = hivemoderation_result
    except:
        results["HiveModeration"] = "unavaible/error"
        if debug_mode:
            logger.exception("HiveModeration")
    print("----------------------------------------------------------------------------")
    print(results)
else:
    print("----------------------------------------------------------------------------")
    print("HiveModeration Text AI-Generated Content Detection tool was skipped due to character limit")

input()