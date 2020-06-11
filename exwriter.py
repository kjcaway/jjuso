import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QDesktopWidget, QPushButton, QFileDialog
from common.excelo import Excelo

class ExcelWriterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.sheetName = 'Sheet1'

    def initUI(self):
        self.lbl1 = QLabel('엑셀 파일을 하나 선택해서 주소지를 갱신해보세요 !')

        self.btn1 = QPushButton('선택하기')
        self.btn1.setCheckable(True)

        self.btn1.clicked.connect(self.openFileDlg)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.lbl1)
        hbox.addWidget(self.btn1)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(4)

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
            print("Target File: " + fileName)

            ex = Excelo(fileName, self.sheetName)
            ex.testLoad()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ExcelWriterApp()
    sys.exit(app.exec_())