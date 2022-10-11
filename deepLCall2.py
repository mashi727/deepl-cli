import sys
from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6 import QtCore

from deepLUi2 import Ui_deepL
import pyperclip
import deepl

class MainWindow(QtWidgets.QMainWindow, Ui_deepL):
    '''初期化メソッド（インスタンス変数の定義）'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self) # この中で必要なMainWindowの定数が宣言
        self.initUI()
        #self.translate(text)
        self.pushButton_clear.clicked.connect(self.clearText)

    def initUI(self):
        # ...
        #self.text_box = QtWidgets.QTextEdit(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.plainTextEdit_input.installEventFilter(self)
        # ...

    def clearText(self):
        self.plainTextEdit_input.clear()
        self.statusBar().showMessage("")

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress and obj is self.plainTextEdit_input:
            if (event.modifiers() == Qt.ShiftModifier and event.key() == Qt.Key_Return) and self.plainTextEdit_input.hasFocus():
                self.translate(self.plainTextEdit_input.toPlainText())
                return True
        return False

        #self.pushButton_translate.clicked.connect()

    def translate(self, input_text):
        apikey_path = './.deepl_apikey'
        with open(apikey_path) as f:
            API_KEY = f.readlines()[0].rstrip()
        auth_key = API_KEY
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(input_text, target_lang='JA')
        pyperclip.copy(result.text)
        self.statusBar().showMessage("Ready to paste!")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()