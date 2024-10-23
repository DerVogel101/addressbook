# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mode_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_ModeChooseDialog(object):
    def setupUi(self, ModeChooseDialog):
        if not ModeChooseDialog.objectName():
            ModeChooseDialog.setObjectName(u"ModeChooseDialog")
        ModeChooseDialog.resize(360, 130)
        ModeChooseDialog.setSizeGripEnabled(True)
        self.verticalLayout = QVBoxLayout(ModeChooseDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(15, 25, 15, 15)
        self.label_mode_choose = QLabel(ModeChooseDialog)
        self.label_mode_choose.setObjectName(u"label_mode_choose")
        self.label_mode_choose.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label_mode_choose)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.mode_choose_button_layout = QHBoxLayout()
        self.mode_choose_button_layout.setObjectName(u"mode_choose_button_layout")
        self.button_choose_csv = QPushButton(ModeChooseDialog)
        self.button_choose_csv.setObjectName(u"button_choose_csv")
        self.button_choose_csv.setAutoDefault(False)
        self.button_choose_csv.setFlat(False)

        self.mode_choose_button_layout.addWidget(self.button_choose_csv)

        self.horizontalSpacer = QSpacerItem(25, 14, QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum)

        self.mode_choose_button_layout.addItem(self.horizontalSpacer)

        self.button_choose_sql = QPushButton(ModeChooseDialog)
        self.button_choose_sql.setObjectName(u"button_choose_sql")

        self.mode_choose_button_layout.addWidget(self.button_choose_sql)


        self.verticalLayout.addLayout(self.mode_choose_button_layout)


        self.retranslateUi(ModeChooseDialog)

        self.button_choose_sql.setDefault(True)


        QMetaObject.connectSlotsByName(ModeChooseDialog)
    # setupUi

    def retranslateUi(self, ModeChooseDialog):
        ModeChooseDialog.setWindowTitle(QCoreApplication.translate("ModeChooseDialog", u"Addressbook - Modus w\u00e4hlen", None))
        self.label_mode_choose.setText(QCoreApplication.translate("ModeChooseDialog", u"Welche Version soll benutzt werden?", None))
        self.button_choose_csv.setText(QCoreApplication.translate("ModeChooseDialog", u"CSV", None))
        self.button_choose_sql.setText(QCoreApplication.translate("ModeChooseDialog", u"SQLite", None))
    # retranslateUi

