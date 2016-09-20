import requests
from dicttoxml import dicttoxml
import os
import xml.etree.ElementTree as ET
import os.path, time
import datetime
from time import mktime
import datetime

services_url = 'http://localhost:8089/'
class SILPCache:
    def __init__(self, cache):
        self.cache = cache

    def putContent(self, folder, content):
        response = requests.get(content)
        contentName = content.replace("/", "_")
        contentName = contentName.replace(":", "_")
        if not os.path.exists('cache'):
            os.makedirs('cache')
        XMLdata = dicttoxml(response.json())
        f = open(folder + '/' + contentName, "w")
        f.write(XMLdata.decode("utf-8"))
        f.close()
        f = open(folder + '/' + contentName, "r")
        fileC = f.read()
        f.close()
        return fileC


    def getContent(self, content, level):
        level = level * 3600
        contentName = content.replace("/", "_")
        contentName = contentName.replace(":", "_")
        if (os.path.isfile('C:/tmp/cache/' + contentName)):
            fileDate = datetime.datetime.fromtimestamp(
                mktime(time.strptime(time.ctime(os.path.getmtime('C:/tmp/cache/' + contentName)))))
            difference = datetime.datetime.now() - fileDate
            if (difference.seconds <= level):
                return open('C:/tmp/cache/' + contentName, "r").read()
            else:
                result = self.putContent('C:/tmp/cache', content)
                return result
        else:
            result = self.putContent('C:/tmp/cache', content)
            return result


    def putImage(self, folder, content):
        response = requests.get(services_url+'/getimage/' + content)

        newFileByteArray = bytearray(response.content)
        f = open(folder + content, "wb")
        f.write(newFileByteArray)
        f.close()


    def getImage(self, content):
        if not os.path.exists('C:/tmp/cache/members'):
            os.makedirs('app/members')
        xmlImages = ET.fromstring(content)
        for imageId in xmlImages.findall('item'):
            fileName = imageId.find('user_image').text
            if (not (os.path.isfile('C:/tmp/cache/members/' + fileName))):
                self.putImage('C:/tmp/cache/members/', fileName)
