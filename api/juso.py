import requests
import json

class Juso:
    confmKey = 'apiKey'
    keyword = ''
    currentPage = 1
    countPerPage = 10
    resultType = 'json'
    url = 'http://www.juso.go.kr/addrlink/addrLinkApiJsonp.do'
    
    def __init__(self, keyword):
        self.keyword = keyword

    def getAddress(self):
        datas = {
            "confmKey" : self.confmKey,
            "currentPage" : self.currentPage,
            "countPerPage" : self.countPerPage,
            "resultType" : self.resultType,
            "keyword" : self.keyword
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.url, headers=headers, data=datas)

        print(response.status_code)
        response = response.text
        response = response.lstrip('\(')
        response = response.rstrip('\)')

        return json.loads(response)