from os import truncate
import sys
from PySide6 import QtWidgets
from PySide6.QtCore import *

from deepLUi import Ui_deepL

import deepl



class MainWindow(QtWidgets.QMainWindow, Ui_deepL):
    '''初期化メソッド（インスタンス変数の定義）'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self) # この中で必要なMainWindowの定数が宣言

        #self.translate(text)

        # ここから、ファイルツリー表示用のコード
        path = '.'
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath(path)
        self.model.setNameFilters(['*.txt']) # この設定だけだと、非該当の拡張子はグレー表示
        self.model.setNameFilterDisables(False) # 上記フィルターに該当しないファイルは非表示
        view = self.treeView
        view.setModel(self.model)
        view.setRootIndex(self.model.index(path))
        view.setColumnWidth(0,200)
        #view.setColumnWidth(2,48)
        view.hideColumn(1)# for removing Size Column
        #view.hideColumn(2)# for removing Type Column
        view.hideColumn(3)# for removing Date Modified Column
        #view.setRootIndex(self.model.index(path))
        view.setItemsExpandable(True)        


        # クリックしたファイルの内容を追加します。
        view.clicked.connect(self.getFileName)

        # ここで、編集して
        self.pushButton_translate.clicked.connect(lambda : self.translate(self.plainTextEdit_input.toPlainText(), self.comboBox_output_language.currentText()))
        #self.pushButton_translate.clicked.connect(self.translate)



    def translate(self, input_text, target_language_flag):
        '''
        target_langの種類、以下のサイトより転記
        https://www.deepl.com/ja/docs-api/translating-text/
        
        target_lang : The language into which the text should be translated. Options currently available:
        "BG" - Bulgarian
        "CS" - Czech
        "DA" - Danish
        "DE" - German
        "EL" - Greek
        "EN-GB" - English (British)
        "EN-US" - English (American)
        "EN" - English (unspecified variant for backward compatibility; please select EN-GB or EN-US instead)
        "ES" - Spanish
        "ET" - Estonian
        "FI" - Finnish
        "FR" - French
        "HU" - Hungarian
        "IT" - Italian
        "JA" - Japanese
        "LT" - Lithuanian
        "LV" - Latvian
        "NL" - Dutch
        "PL" - Polish
        "PT-PT" - Portuguese (all Portuguese varieties excluding Brazilian Portuguese)
        "PT-BR" - Portuguese (Brazilian)
        "PT" - Portuguese (unspecified variant for backward compatibility; please select PT-PT or PT-BR instead)
        "RO" - Romanian
        "RU" - Russian
        "SK" - Slovak
        "SL" - Slovenian
        "SV" - Swedish
        "ZH" - Chinese
        '''

        if target_language_flag == 'アメリカ英語':
            target_language='EN-US'
        elif target_language_flag == '日本語':
            target_language='JA'
        elif target_language_flag == 'イギリス英語':
            target_language='EN-GB'
        elif target_language_flag == 'ドイツ語':
            target_language='DE'
        else:
            pass
        
        auth_key = 'a1c00d90-9dde-652a-f8bb-0a28fe8a1943:fx'

        translator = deepl.Translator(auth_key) 
        result = translator.translate_text(input_text, target_lang=target_language) 
        output_text = result.text
        self.label_source_language.setText(result.detected_source_lang)
        #self.check_method(result)
        self.plainTextEdit_Output.setPlainText(output_text)


    def check_method(self, model):
        import inspect
        print(type(model))
        for method in inspect.getmembers(model):
            print(method)


    def is_str(self, v):
        return type(v) is str

    # クリックした際のメソッド    
    def getFileName(self, index):
        from PySide6.QtWidgets import QMessageBox
        import os
        filepath = []
        indexItem = self.model.index(index.row(), 0, index.parent())
        if os.path.isfile(self.model.filePath(indexItem)):
            filepath.insert(0,self.model.filePath(indexItem))
            myfile = open(filepath[0], 'r', encoding='UTF-8') # 入力は、UTF-8 Encodingである必要がある
            input_text = myfile.read()
            if self.is_str(input_text):
                pass
            else:
                print('入力ファイルは、文字列ではありません。')
            #QMessageBox.information(None, "Notice!", filepath[0] + "\n\n is Selected", QMessageBox.Yes)
        else:
            pass
            #QMessageBox.warning(None, "Notice!", "Select File!", QMessageBox.Yes)        
        #self.check_method(self.treeView)        
        self.plainTextEdit_input.setPlainText(input_text)

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == '__main__':
    main()