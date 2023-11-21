import configparser
class Configure():
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config_path = "localalert.ini"
        self.readconfig()
    
    def readconfig(self):
        try:
            self.config.read(self.config_path, encoding="utf-8")
        except:
            print('failure: readconfig')
            return

        try:
            self.exittype = self.config.getint('exit','exit')
        except:
            print('config: error in exit type')
            pass
    def writeconfig(self,type):
        if type == 'exit':
            self.config.set('exit','exit',str(self.exittype))
            self.config.write(open("localalert.ini", "w"))