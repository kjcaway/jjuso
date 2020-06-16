import re

def getMatchAddress(address):
    try:
        regex = r'(\w+[시,도]\s*)?(\w+[구,시,군]\s*)?(\w+[구,시]\s*)?(\w+[면,읍]\s*)?(\w+\d*\w*[동,리,로,길]\s*)?(\w+\d*\w*[번길]\s*)?(\w*\d+-?\d*)?'
        x = re.search(regex, address)
    except Exception as e:
        print(str(e))
        return ''
    else:
        return x.group()