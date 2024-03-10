import configparser
import os
class Configure():
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.path = 'config.ini'
        self.readConfig()
    
    def readConfig(self):
        if os.path.exists(self.path):
            self.config.read(self.path, encoding="utf-8")
        else:
            with open(self.path,'w',encoding='utf-8') as f:
                f.write('')
            print('Failure: open config')

    def addUid(self,uid):
        self.config.add_section(uid)
        self.save()
    
    def removeUid(self,uid):
        self.config.remove_section(uid)
        self.save()

    def save(self):
        try:
            with open(self.path,'w',encoding='utf-8') as f:
                self.config.write(f)
        except:
            print('Failure: writeconfig')
            return