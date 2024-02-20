import undetected_chromedriver as uc
import json

class Options:
    def __init__(self) -> None:
        self.headless_mode = False

        self.toggleUndetectableAI = True
        self.toggleGrammica = True
        self.toggleWritefull = True
        self.toggleHive = True
        self.toggleScribbr = True
        self.toggleTypeset = True

        self.flagFinishedUndetectableAI = False
        self.flagFinishedGrammica = False
        self.flagFinishedWritefull = False
        self.flagFinishedHive = False
        self.flagFinishedScribbr = False
        self.flagFinishedTypeset = False

        self.results = dict()

        self.version = "1.4.0"

        self.chromeOptions = uc.ChromeOptions()
        self.chromeOptions.add_argument('--ignore-ssl-errors=yes')
        self.chromeOptions.add_argument('--ignore-certificate-errors')
        self.chromeOptions.add_argument("--headless")
        if self.headless_mode:
            self.chromeOptions.add_argument("--headless")
        self.chromeOptions.add_argument('--log-level=3')
        self.chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
    
    def statesToOptions(self, states: list[bool]) -> None:
        self.toggleUndetectableAI = states[0]
        self.toggleGrammica = states[1]
        self.toggleWritefull = states[2]
        self.toggleHive = states[3]
        self.toggleScribbr = states[4]
        self.toggleTypeset = states[5]
    
    def loadCachedOptions(self) -> None:
        try:
            with open('options.json', 'r') as f:
                toggle_values = json.load(f)
                self.toggleUndetectableAI = toggle_values.get('toggleUndetectableAI', self.toggleUndetectableAI)
                self.toggleGrammica = toggle_values.get('toggleGrammica', self.toggleGrammica)
                self.toggleWritefull = toggle_values.get('toggleWritefull', self.toggleWritefull)
                self.toggleHive = toggle_values.get('toggleHive', self.toggleHive)
                self.toggleScribbr = toggle_values.get('toggleScribbr', self.toggleScribbr)
                self.toggleTypeset = toggle_values.get('toggleTypeset', self.toggleTypeset)
        except FileNotFoundError:
            pass  # File does not exist yet, so we'll just use the default values

    def setCachedOptions(self) -> None:
        toggle_values = {
            'toggleUndetectableAI': self.toggleUndetectableAI,
            'toggleGrammica': self.toggleGrammica,
            'toggleWritefull': self.toggleWritefull,
            'toggleHive': self.toggleHive,
            'toggleScribbr': self.toggleScribbr,
            'toggleTypeset': self.toggleTypeset,
        }
        with open('options.json', 'w') as f:
            json.dump(toggle_values, f)
    
    def __str__(self) -> str:
        return str(self.__dict__)