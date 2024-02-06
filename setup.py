import undetected_chromedriver as uc

class Options:
    def __init__(self) -> None:
        headless_mode = False

        self.toggleUndetectableAI = False
        self.toggleGrammica = True

        self.flagFinishedUndetectableAI = False
        self.flagFinishedGrammica = False

        self.results = dict()

        self.chromeOptions = uc.ChromeOptions()
        self.chromeOptions.add_argument('--ignore-ssl-errors=yes')
        self.chromeOptions.add_argument('--ignore-certificate-errors')
        if headless_mode:
            self.chromeOptions.add_argument("--headless")
        self.chromeOptions.add_argument('--log-level=3')
        self.chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
    
    def __str__(self) -> str:
        return str(self.__dict__)