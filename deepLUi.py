# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'deepLUi.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QMainWindow, QMenuBar,
    QPlainTextEdit, QPushButton, QSizePolicy, QSpacerItem,
    QStatusBar, QTreeView, QVBoxLayout, QWidget)

class Ui_deepL(object):
    def setupUi(self, deepL):
        if not deepL.objectName():
            deepL.setObjectName(u"deepL")
        deepL.resize(1726, 1211)
        font = QFont()
        font.setPointSize(16)
        deepL.setFont(font)
        self.centralwidget = QWidget(deepL)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QSize(120, 0))
        self.label.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout.addWidget(self.label)

        self.label_source_language = QLabel(self.centralwidget)
        self.label_source_language.setObjectName(u"label_source_language")
        sizePolicy.setHeightForWidth(self.label_source_language.sizePolicy().hasHeightForWidth())
        self.label_source_language.setSizePolicy(sizePolicy)
        self.label_source_language.setMinimumSize(QSize(100, 0))
        self.label_source_language.setMaximumSize(QSize(100, 16777215))
        self.label_source_language.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.label_source_language)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.plainTextEdit_input = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_input.setObjectName(u"plainTextEdit_input")

        self.verticalLayout.addWidget(self.plainTextEdit_input)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(120, 0))
        self.label_2.setMaximumSize(QSize(120, 16777215))

        self.horizontalLayout_2.addWidget(self.label_2)

        self.comboBox_output_language = QComboBox(self.centralwidget)
        self.comboBox_output_language.addItem("")
        self.comboBox_output_language.addItem("")
        self.comboBox_output_language.addItem("")
        self.comboBox_output_language.addItem("")
        self.comboBox_output_language.setObjectName(u"comboBox_output_language")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_output_language.sizePolicy().hasHeightForWidth())
        self.comboBox_output_language.setSizePolicy(sizePolicy1)
        self.comboBox_output_language.setMinimumSize(QSize(130, 0))
        self.comboBox_output_language.setMaximumSize(QSize(130, 16777215))

        self.horizontalLayout_2.addWidget(self.comboBox_output_language)

        self.pushButton_translate = QPushButton(self.centralwidget)
        self.pushButton_translate.setObjectName(u"pushButton_translate")
        self.pushButton_translate.setMinimumSize(QSize(150, 0))
        self.pushButton_translate.setMaximumSize(QSize(150, 16777215))

        self.horizontalLayout_2.addWidget(self.pushButton_translate)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.plainTextEdit_Output = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_Output.setObjectName(u"plainTextEdit_Output")
        self.plainTextEdit_Output.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.plainTextEdit_Output)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)

        self.treeView = QTreeView(self.centralwidget)
        self.treeView.setObjectName(u"treeView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.treeView.sizePolicy().hasHeightForWidth())
        self.treeView.setSizePolicy(sizePolicy2)
        self.treeView.setMinimumSize(QSize(350, 0))
        self.treeView.setMaximumSize(QSize(350, 16777215))

        self.horizontalLayout_4.addWidget(self.treeView)


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.pushButton_quit = QPushButton(self.centralwidget)
        self.pushButton_quit.setObjectName(u"pushButton_quit")

        self.horizontalLayout_3.addWidget(self.pushButton_quit)


        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        deepL.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(deepL)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1726, 24))
        deepL.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(deepL)
        self.statusbar.setObjectName(u"statusbar")
        deepL.setStatusBar(self.statusbar)

        self.retranslateUi(deepL)
        self.pushButton_quit.clicked.connect(deepL.close)

        QMetaObject.connectSlotsByName(deepL)
    # setupUi

    def retranslateUi(self, deepL):
        deepL.setWindowTitle(QCoreApplication.translate("deepL", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("deepL", u"\u539f\u6587", None))
        self.label_source_language.setText(QCoreApplication.translate("deepL", u"\u5165\u529b\u8a00\u8a9e", None))
        self.label_2.setText(QCoreApplication.translate("deepL", u"DeepL\u7ffb\u8a33\u6587", None))
        self.comboBox_output_language.setItemText(0, QCoreApplication.translate("deepL", u"\u30a2\u30e1\u30ea\u30ab\u82f1\u8a9e", None))
        self.comboBox_output_language.setItemText(1, QCoreApplication.translate("deepL", u"\u65e5\u672c\u8a9e", None))
        self.comboBox_output_language.setItemText(2, QCoreApplication.translate("deepL", u"\u30a4\u30ae\u30ea\u30b9\u82f1\u8a9e", None))
        self.comboBox_output_language.setItemText(3, QCoreApplication.translate("deepL", u"\u30c9\u30a4\u30c4\u8a9e", None))

        self.pushButton_translate.setText(QCoreApplication.translate("deepL", u"Translate", None))
        self.pushButton_quit.setText(QCoreApplication.translate("deepL", u"Quit", None))
    # retranslateUi

