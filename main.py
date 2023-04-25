# ---------------------------GENERAL CONFIG--------------------------------------
load_time = 10 # How many seconds does your computer take to load webpages? Increase this if you are getting "unavaible" on most of the tools. YOu can find the exact time by enabling debug mode and timing it with your phone.
generation_time = 4  # How many seconds to wait for results to generate in tools where we don't have a way of telling when it has finished generating?
debug_mode = True # Is debug mode enabled?
headless_mode = False # If enabled, you won't see the browser window. This would allow you to do other things while the text is being proccesed. It breakes some tools (as mentioned in the README)

# ------------------------ON/OFF SWITCHES FOR TOOLS-------------------------------
grammica_enabled = True  # DO NOT DISABLE - Used for character limit measurements. If disabled, will break everything
aiwritingcheck_enabled = True  # Slows down program significantly.
writer_enabled = True
zerogpt_enabled = True
contentatscale_enabled = True  # Will get disabled automatically if headless mode is enabled due to not functioning in headless.
writefull_enabled = True
hivemoderation_enabled = False  # Will get disabled automatically if headless mode is enabled due to not functioning in headless. Implemented anti-botting class randomisation. No way to select the button.
copyleaks_enabled = False  # Implemented anti-botting measures via cloudflare, chance of being able to use it is very low
crossplag_enabled = True  # Slows down program significantly. Has a request limit. You can send x ammount of requests per x minuetes.

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
import os
import glob
if debug_mode:
    import logging
    import logging.config
    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': True,
    })

# --------------------------Input Files Handling----------------------------------
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
    for i in files_to_check:
        print(i)
        
# ------------------------------General Setup-------------------------------------
#TODO token handling 
results = dict()
# Sets up debug mode
if debug_mode:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

if headless_mode:
    hivemoderation_enabled = False
    contentatscale_enabled = False

# ----------------------------Selenium Setup-------------------------------------
"""service = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=service)"""
# Sets up the driver
driver = uc.Chrome
# Sets up the options
options = Options()
if headless_mode:
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
    time.sleep(0.2)
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
for i in files_to_check:
    print(f"Currently checking: {i}")
    with open (i, "r", encoding='utf-8') as check_file:
        text_to_check = check_file.read()
    results[f"{i}"] = dict()

    # https://grammica.com/ai-detector
    if grammica_enabled:
        try:
            driver.get("https://grammica.com/ai-detector")
            grammica_box = driver.find_element(by=By.XPATH, value='//*[@id="text"]')
            grammica_box.send_keys(text_to_check)
            grammica_ai_percentage = wait_until_element_text('//*[@id="fake-percentage"]').text
            results[f"{i}"]["Grammica AI Detector"] = f"{grammica_ai_percentage} probability of AI Written"
            if grammica_ai_percentage == "":
                results[f"{i}"]["Grammica AI Detector"] = "unavaible"
                if debug_mode:
                    logger.warning("Grammica AI Detector Unavaible")
        except:
            results[f"{i}"]["Grammica AI Detector"] = "unavaible/error"
            if debug_mode:
                logger.exception("Grammica AI Detector Exception")
    else:
        print("----------------------------------------------------------------------------")
        print("Grammica AI Detector has been disabled. This will have severe impact on the function of the script. Chance of full errors high.")

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
    print(results[f"{i}"])


    # https://aiwritingcheck.org/
    if aiwritingcheck_enabled:
        if words_int > 100 and words_int < 400:
            try:
                driver.get("https://aiwritingcheck.org/")
                use_tool('//*[@id="js-textBox"]', '//*[@id="js-submitButton"]')
                time.sleep(generation_time)
                if driver.find_element(by=By.XPATH, value='//*[@id="js-human"]/h3/div/b').is_displayed():
                    results[f"{i}"]["AI Writing Check"] = "Written by Human"
                elif driver.find_element(by=By.XPATH, value='//*[@id="js-ai"]/h3/div/b').is_displayed():
                    results[f"{i}"]["AI Writing Check"] = "Written by AI"
                else:
                    results[f"{i}"]["AI Writing Check"] = "unavaible"
                    if debug_mode:
                        logger.warning("AI Writing Check Unavaible")
            except:
                results[f"{i}"]["AI Writing Check"] = "unavaible/error"
                if debug_mode:
                    logger.exception("AI Writing Check Exception")
            print("----------------------------------------------------------------------------")
            print(results[f"{i}"])
        else:
            print("----------------------------------------------------------------------------")
            print("AI Writing Check by Quill.org & CommonLit was skipped due to character limits.")
    else:
        print("----------------------------------------------------------------------------")
        print("AI Writing Check by Quill.org & CommonLit has been disabled.")


    # https://writer.com/ai-content-detector/
    if writer_enabled:
        if characters_int < 1500:
            try:
                driver.get("https://writer.com/ai-content-detector/")
                use_tool('//*[@placeholder="Paste text or write here"]', '//*[@class="dc-btn-gradient ai-content-detector-submit"]')
                writedetector_human_written = wait_until_element_text('//*[@id="ai-percentage"]').text
                if writedetector_human_written == "":
                    results[f"{i}"]["WRITER AI Detector"] = "unavaible"
                    if debug_mode:
                        logger.warning("WRITER AI Detecotr Unavaible")
                else:
                    writedetector_ai_written = human_to_ai_percentage(writedetector_human_written)
                    results[f"{i}"]["WRITER AI Detector"] = f"{writedetector_ai_written}% probability of AI written"
            except:
                results[f"{i}"]["WRITER AI Detector"] = "unavaible/error"
                if debug_mode:
                    logger.exception("WRITER AI Detector Exception")
            print("----------------------------------------------------------------------------")
            print(results[f"{i}"])
        else:
            print("----------------------------------------------------------------------------")
            print("WRITER AI Content Detector was skipped due to character limits.")
    else:
        print("----------------------------------------------------------------------------")
        print("WRITER AI Content Detector has been disabled.")


    # https://www.zerogpt.com/
    if zerogpt_enabled:
        try:
            driver.get("https://www.zerogpt.com/")
            use_tool('//*[@id="textArea"]', '//*[@class="scoreButton"]')
            zerogpt_result = wait_until_element_text('//*[@class="result-container margin-v-15"]/div/span').text
            if zerogpt_result == "":
                results[f"{i}"]["ZeroGPT"] = "unavaible"
                if debug_mode:
                    logger.warning("ZeroGPT Unavaible")
            else:
                results[f"{i}"]["ZeroGPT"] = zerogpt_result
        except:
            results[f"{i}"]["ZeroGPT"] = "unavaible/error"
            if debug_mode:
                logger.exception("ZeroGPT Exception")
        print("----------------------------------------------------------------------------")
        print(results[f"{i}"])
    else:
        print("----------------------------------------------------------------------------")
        print("ZeroGPT has been disabled.")

    # https://contentatscale.ai/ai-content-detector/
    if contentatscale_enabled:
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
                    results[f"{i}"]["ContentAtScale AI Detector"] = "unavaible"
                else:
                    results[f"{i}"]["ContentAtScale AI Detector"] = contentatscale_result
            except:
                results[f"{i}"]["ContentAtScale AI Detector"] = "unavaible/error"
                if debug_mode:
                    logger.exception("ContentAtScale AI Detector Exception")
            print("----------------------------------------------------------------------------")
            print(results[f"{i}"])
        else:
            print("----------------------------------------------------------------------------")
            print("ContentAtScale AI Detector was skipped due to character limit.")
    else:
        print("----------------------------------------------------------------------------")
        print("ContentAtScale AI Detector has been disabled. This may be due to manual deactivation, or because you enabled headless mode.")

    # https://x.writefull.com/gpt-detector
    if writefull_enabled:
        try:
            driver.get("https://x.writefull.com/gpt-detector")
            use_tool('//*[@placeholder="Enter text here."]', '//*[@class="inline-flex justify-center items-center rounded-md text-sm font-semibold py-3 px-4 text-white bg-slate-900 hover:bg-slate-800 text-base font-medium px-4 py-3"]')
            writefull_result = wait_until_element_text('//*[@class="text-2xl ml-4"]').text
            if writefull_result == "":
                results[f"{i}"]["WriteFull"] = "unavaible"
                if debug_mode:
                    logger.warning("Writefull Unavaible")
            else:
                results[f"{i}"]["WriteFull"] = writefull_result
        except:
            results[f"{i}"]["WriteFull"] = "unavaible/error"
            if debug_mode:
                logger.exception("WriteFull Exception")
        print("----------------------------------------------------------------------------")
        print(results[f"{i}"])
    else:
        print("----------------------------------------------------------------------------")
        print("WriteFull GPT-Detector has been disabled.")
    
    # https://hivemoderation.com/ai-generated-content-detection
    if hivemoderation_enabled:
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
                    results[f"{i}"]["HiveModeration"] = "unavaible"
                    if debug_mode:
                        logger.warning("HiveModeration Unavaible")
                else:
                    results[f"{i}"]["HiveModeration"] = hivemoderation_result
            except:
                results[f"{i}"]["HiveModeration"] = "unavaible/error"
                if debug_mode:
                    logger.exception("HiveModeration")
            print("----------------------------------------------------------------------------")
            print(results[f"{i}"])
        else:
            print("----------------------------------------------------------------------------")
            print("HiveModeration Text AI-Generated Content Detection tool was skipped due to character limit")
    else:
        print("----------------------------------------------------------------------------")
        print("HiveModeration Text AI-Generated Content Detection tool has been disabled. This may be due to manual deactivation, or because you enabled headless mode.")

    # https://copyleaks.com/ai-content-detector
    if copyleaks_enabled:
        if characters_int > 150:
            try:
                driver.get("https://copyleaks.com/ai-content-detector")
                time.sleep(1)
                driver.switch_to.frame(driver.find_element(by=By.XPATH, value='//*[@id="ai-content-detector"]'))
                use_tool('//*[@placeholder="Enter text here..."]', '//*[@class="mat-focus-indicator mat-raised-button mat-button-base mat-primary ng-star-inserted"]')
                wait_until_element_text('//*[@class="hover-note ng-tns-c280-0 ng-star-inserted"]')
                copyleaks_result = driver.find_element(by=By.XPATH, value='//*[@class="scan-text-editor scan-text-editor-result ng-tns-c280-0 ng-star-inserted"]/span').get_attribute("cl-scan-probability")
                driver.switch_to.default_content()
                if copyleaks_result == "":
                    results[f"{i}"]["Copyleaks"] = "unavaible"
                    if debug_mode:
                        logger.warning("Copyleaks Unavaible")
                else:
                    results[f"{i}"]["Copyleaks"] = f"{copyleaks_result}% probability of AI Written"
            except:
                results[f"{i}"]["Copyleaks"] = "unavaible/error"
                if debug_mode:
                    logger.exception("Copyleaks Exception")
            print("----------------------------------------------------------------------------")
            print(results[f"{i}"])
        else:
            print("----------------------------------------------------------------------------")
            print("Copyleaks AI Content Detector was skipped due to character limit")
    else:
        print("----------------------------------------------------------------------------")
        print("Copyleaks AI Content Detector has been disabled.")

    # https://crossplag.com/ai-content-detector/
    if crossplag_enabled:
        try:
            driver.get("https://crossplag.com/ai-content-detector/")
            use_tool('//*[@placeholder="Paste or write some text here"]', '//*[@id="checkButtonAIGen"]')
            time.sleep(generation_time)
            crossplag_result = driver.find_element(by=By.XPATH, value='//*[@class="pointer"]/span').text
            if crossplag_result == "":
                results[f"{i}"]["Crossplag"] = "unavaible"
                if debug_mode:
                    logger.warning("Crossplag Unavaible")
            else:
                results[f"{i}"]["Crossplag"] = f"{crossplag_result} probability of AI written"
        except:
            results[f"{i}"]["Crossplag"] = "unavaible/error"
            if debug_mode:
                logger.exception("Crossplag Exception")
        print("----------------------------------------------------------------------------")
        print(results[f"{i}"])
    else:
        print("----------------------------------------------------------------------------")
        print("Crossplag AI Content Detector has been disabled.")

print("")
print("")
print("----------------------------------------------------------------------------")
print("")
print("")

for i in results:
    print("----------------------------------------------------------------------------")
    print(i)
    print(results[i])
input()