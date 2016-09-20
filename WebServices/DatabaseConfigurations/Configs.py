import configparser, os

class Config(object):
    def __init__(self,filename):
        self.config = configparser.ConfigParser()
        self.config.readfp(open(filename))

    def connStringUser(self):
        return self.config.get('postgres','user')

    def connStringDB(self):
        return self.config.get('postgres','dbname')

    def connStringPassword(self):
        return self.config.get('postgres','password')

    def connStringHost(self):
        return self.config.get('postgres','host')

