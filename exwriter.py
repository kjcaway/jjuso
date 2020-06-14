import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QDesktopWidget, QPushButton, QFileDialog, QInputDialog
from common.excelo import Excelo
from api.juso import Juso


class ExcelWriterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fileName = None
        self.sheetName = None
        self.column = None

    def initUI(self):
        self.lbl1 = QLabel('엑셀 파일을 하나 선택해서 주소지를 갱신해보세요 !')

        self.btn1 = QPushButton('선택하기')
        self.btn1.setCheckable(True)

        self.infoLbl1 = QLabel('대상 엑셀 파일 경로 : ')
        self.infoLbl2 = QLabel('대상 시트명 : ')
        self.infoVal1 = QLineEdit()
        self.infoVal2 = QLineEdit()
        self.infoVal1.setReadOnly(True)
        self.infoVal2.setReadOnly(True)
        self.btn2 = QPushButton('만들기')

        self.btn1.clicked.connect(self.openFileDlg)
        self.btn2.clicked.connect(self.execute)

        self.resultLbl1 = QLabel('')

        hbox = QHBoxLayout()
        hbox.addWidget(self.lbl1)
        hbox.addWidget(self.btn1)
        hbox.addStretch(1)

        hboxInfo = QHBoxLayout()
        hboxInfo.addWidget(self.infoLbl1)
        hboxInfo.addWidget(self.infoVal1)
        hboxInfo.addWidget(self.infoLbl2)
        hboxInfo.addWidget(self.infoVal2)
        hboxInfo.addWidget(self.btn2)
        hboxInfo.addStretch(1)

        hboxResult = QHBoxLayout()
        hboxResult.addWidget(self.resultLbl1)
        hboxResult.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addLayout(hboxInfo)
        vbox.addLayout(hboxResult)
        vbox.addStretch(3)

        self.setLayout(vbox)
        self.setWindowTitle('JJuSoEx')
        self.resize(800, 450)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openFileDlg(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"파일 선택", "","Excel Files (*.xlsx)", options=options)
        if fileName:
            self.fileName = fileName
            self.infoVal1.setText(self.fileName)

            ex = Excelo(fileName)
            
            self.showSheetNameDlg(ex.getSheetList())

    def showSheetNameDlg(self, sheetList):
        items = sheetList
        item, ok = QInputDialog.getItem(self, "시트선택", "대상 시트를 선택하세요.", items, 0, False)
        if ok and item:
            self.sheetName= str(item)
            self.infoVal2.setText(self.sheetName)

    def execute(self):
        try:
            print("Target File : " + str(self.fileName))
            print("Target Sheet : " + str(self.sheetName))

            ex = Excelo(self.fileName)
            ex.setSheet(self.sheetName)

            maxColumn = ex.getMaxColumn()
            columnList = list()
            for i in range(maxColumn):
                columnList.append(chr(65+i))

            column, ok = QInputDialog.getItem(self, "컬럼선택", "대상 컬럼를 선택하세요.", columnList, 0, False)
            if ok and column:
                self.column= str(column)
            
            addrList = ex.getAddressList(self.column)

            juso = Juso()
            new = Excelo()

            dataRow = ['기존주소', '도로명', '지번']
            new.ws.append(dataRow)

            for idx, addr in enumerate(addrList):
                json = juso.getAddressForExcel(addr.value)
                print('row: '+ str(idx) + '---result: ' + str(json))
                dataRow = []
                dataRow.append(addr.value)
                dataRow.append(json['road'] if json is not None else "NoResult")
                dataRow.append(json['jibun'] if json is not None else "NoResult")

                new.ws.append(dataRow)
            
            new.save()
        except Exception as e:
            self.resultLbl1.setText("실패!!!" + str(e))
        else:
            self.resultLbl1.setText("성공!!!")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExcelWriterApp()
    sys.exit(app.exec_())