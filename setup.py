import undetected_chromedriver as uc

class Options:
    def __init__(self) -> None:
        self.headless_mode = False

        self.toggleUndetectableAI = True
        self.toggleGrammica = True
        self.toggleWritefull = True
        self.toggleHive = True
        self.toggleScribbr = True

        self.flagFinishedUndetectableAI = False
        self.flagFinishedGrammica = False
        self.flagFinishedWritefull = False
        self.flagFinishedHive = False
        self.flagFinishedScribbr = False

        self.results = dict()

        self.chromeOptions = uc.ChromeOptions()
        self.chromeOptions.add_argument('--ignore-ssl-errors=yes')
        self.chromeOptions.add_argument('--ignore-certificate-errors')
        self.chromeOptions.add_argument("--headless")
        if self.headless_mode:
            self.chromeOptions.add_argument("--headless")
        self.chromeOptions.add_argument('--log-level=3')
        self.chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
    
    def __str__(self) -> str:
        return str(self.__dict__)