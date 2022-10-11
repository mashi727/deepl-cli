# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'deepLUi2.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QMenuBar, QPlainTextEdit, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QVBoxLayout,
    QWidget)

class Ui_deepL(object):
    def setupUi(self, deepL):
        if not deepL.objectName():
            deepL.setObjectName(u"deepL")
        deepL.resize(542, 700)
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
        self.label.setMinimumSize(QSize(500, 0))
        self.label.setMaximumSize(QSize(500, 16777215))
        font1 = QFont()
        font1.setPointSize(20)
        self.label.setFont(font1)

        self.horizontalLayout.addWidget(self.label)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.plainTextEdit_input = QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_input.setObjectName(u"plainTextEdit_input")
        self.plainTextEdit_input.setFont(font1)

        self.verticalLayout.addWidget(self.plainTextEdit_input)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.pushButton_clear = QPushButton(self.centralwidget)
        self.pushButton_clear.setObjectName(u"pushButton_clear")
        self.pushButton_clear.setFont(font1)

        self.horizontalLayout_2.addWidget(self.pushButton_clear)

        self.pushButton_quit = QPushButton(self.centralwidget)
        self.pushButton_quit.setObjectName(u"pushButton_quit")
        self.pushButton_quit.setFont(font1)

        self.horizontalLayout_2.addWidget(self.pushButton_quit)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)


        self.horizontalLayout_4.addLayout(self.verticalLayout_3)


        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)

        deepL.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(deepL)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 542, 24))
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
        self.label.setText(QCoreApplication.translate("deepL", u"Shift + Return\u3067\u8a33\u6587\u3092\u30af\u30ea\u30c3\u30d7\u30dc\u30fc\u30c9\u306b\u30b3\u30d4\u30fc", None))
        self.pushButton_clear.setText(QCoreApplication.translate("deepL", u"Clear", None))
        self.pushButton_quit.setText(QCoreApplication.translate("deepL", u"Quit", None))
    # retranslateUi

