import configparser
class Configure():
    def __init__(self,index) -> None:
        self.config = configparser.ConfigParser()
        self.config_path = "localalert.ini"
        self.widgetIndex = index

        self.templetePath = ''

        self.audioPath = ''

        self.screenIndex = None
        self.startx = None
        self.starty = None
        self.endx = None
        self.endy = None

        self.interval = '2000'

    def setIndex(self,idx):
        self.widgetIndex = idx
        self.writeconfig()

    def readconfig(self):
        try:
            self.config.read(self.config_path, encoding="utf-8")
        except:
            print('failure: openconfig')
            return

        try:
            section = 'watcher'+str(self.widgetIndex)
            self.templetePath = self.config.get(section,'templetePath')
            self.audioPath = self.config.get(section,'audioPath')
            self.startx = self.config.getint(section,'startx')
            self.starty = self.config.getint(section,'starty')
            self.endx = self.config.getint(section,'endx')
            self.endy = self.config.getint(section,'endy')
            self.interval = self.config.getint(section,'interval')
        except:
            print('failure: readconfig')
            pass
    def writeconfig(self):
        try:
            section = 'watcher'+str(self.widgetIndex)
            with open(self.config_path):
                
        except:
            print('failure: writeconfig')
            return