import requests
import json
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

class Juso:
    confmKey = os.getenv('JUSO_API_KEY')
    keyword = None
    currentPage = 1
    countPerPage = 10
    resultType = 'json'
    url = 'http://www.juso.go.kr/addrlink/addrLinkApiJsonp.do'
    
    def __init__(self, keyword=None):
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

    def getAddressForExcel(self, keyword):
        if len(keyword) > 14:
            datas = {
                "confmKey" : self.confmKey,
                "currentPage" : self.currentPage,
                "countPerPage" : self.countPerPage,
                "resultType" : self.resultType,
                "keyword" : keyword
            }
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = requests.post(self.url, headers=headers, data=datas)

            response = response.text
            response = response.lstrip('\(')
            response = response.rstrip('\)')
            res = json.loads(response)

            totalCount = res['results']['common']['totalCount']
            if int(totalCount) is 1:
                roadAddr = res['results']['juso'][0]['roadAddr']
                jibunAddr = res['results']['juso'][0]['jibunAddr']
                return {
                    "road" : roadAddr,
                    "jibun" : jibunAddr
                }
            else:
                return None
        else:
            return None
