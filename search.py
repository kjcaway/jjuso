import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QDesktopWidget, QPushButton, QTextBrowser
from api.juso import Juso

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.keyword = ''

    def initUI(self):
        self.lbl1 = QLabel('주소를 입력하세요.(도로명 또는 지번주소)')
        self.te = QLineEdit()

        self.te.textChanged[str].connect(self.onKeywordChange)

        self.btn1 = QPushButton('Search')
        self.btn1.setCheckable(True)

        self.btn1.clicked.connect(self.onSearch)

        self.lbl2 = QLabel('결과 : ')

        self.tb1 = QTextBrowser()
        self.tb2 = QTextBrowser()

        hbox = QHBoxLayout()
        hbox.addWidget(self.tb1)
        hbox.addWidget(self.tb2)


        vbox = QVBoxLayout()
        vbox.addWidget(self.lbl1)
        vbox.addWidget(self.te)
        vbox.addWidget(self.btn1)
        vbox.addWidget(self.lbl2)
        vbox.addLayout(hbox)
        vbox.addStretch()

        self.setLayout(vbox)
        self.setWindowTitle('JJuSo')
        self.resize(800, 450)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onKeywordChange(self, text):
        self.keyword = text

    def onSearch(self):
        print(self.keyword)
        
        x = Juso(self.keyword)
        res = x.getAddress()
        
        totalCount = res['results']['common']['totalCount']
        subText = " 중 10개만 표시" if int(totalCount) > 0 else ""
        self.lbl2.setText('결과 : 총 ' + totalCount + ' 건' + subText)
        address_list = res['results']['juso']
        self.gridAddressList(address_list)

    def gridAddressList(self, adlist):
        roadAddrTxt = '<도로명주소>'
        jibunAddrTxt = '<지번주소>'
        if adlist is not None:
            for addr in adlist:
                roadAddrTxt = roadAddrTxt + '\n' + addr['roadAddr']
                jibunAddrTxt = jibunAddrTxt + '\n' + addr['jibunAddr']

        self.tb1.setText(roadAddrTxt)
        self.tb2.setText(jibunAddrTxt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SearchApp()
    sys.exit(app.exec_())