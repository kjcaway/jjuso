from openpyxl import load_workbook

class Excelo:
    wb = None
    ws = None

    def __init__(self, filePath, sheetName):
        self.wb = load_workbook(filePath, data_only=True)
        self.ws = self.wb[sheetName]

    def testLoad(self):
        print(self.ws['A1'].value)