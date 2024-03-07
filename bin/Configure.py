import configparser
class Configure():
    def __init__(self,uid) -> None:
        self.config = configparser.ConfigParser()
        self.uid = uid
        self.path = '../configs/'+ self.uid + ".ini"

        self.templetePath = ''
        self.audioPath = ''

        self.screenIndex = None
        self.startx = None
        self.starty = None
        self.endx = None
        self.endy = None

        self.interval = '2000'
    
    def setTempletePath(self,templetePath):
        self.templetePath = templetePath

    def setAudioPath(self,audioPath):
        self.audioPath =  audioPath

    def setScreenIndex(self,screenIndex):
        self.screenIndex = screenIndex

    def setScreenArea(self,position):
        self.startx = position['startx']
        self.starty = position['starty']
        self.endx = position['endx']
        self.endy = position['endy']
    
    def setInterval(self,interval):
        self.interval = interval

    def readconfig(self):
        try:
            self.config.read(self.path, encoding="utf-8")
        except:
            print('failure: openconfig')
            return

        try:
            section = 'watcher'+str(self.uid)
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
            section = 'watcher'+str(self.uid)
            with open(self.config_path):
                pass
        except:
            print('failure: writeconfig')
            return