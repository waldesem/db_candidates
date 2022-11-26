from PySide2 import QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class WindowUi(object):

    def setup_ui(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(968, 772)
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_2 = QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)

        self.checkBox = QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(u"checkBox")

        self.gridLayout.addWidget(self.checkBox, 1, 2, 1, 1)

        self.tableView = QTableView(self.centralwidget)
        self.tableView.setObjectName(u"tableView")

        self.gridLayout.addWidget(self.tableView, 3, 0, 1, 3)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.gridLayout.addWidget(self.pushButton_3, 4, 0, 1, 1)

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.gridLayout.addWidget(self.pushButton_4, 4, 1, 1, 1)

        self.pushButton_5 = QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.gridLayout.addWidget(self.pushButton_5, 4, 2, 1, 1)

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")

        self.gridLayout.addWidget(self.textBrowser, 6, 0, 1, 3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 3)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 3)

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 968, 27))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())

        self.retranslate(main_window)

        QMetaObject.connectSlotsByName(main_window)

    def retranslate(self, main_window):
        main_window.setWindowTitle(
            QCoreApplication.translate("main_window", u"\u0411\u0430\u0437\u0430 \u0434\u0430\u043d\u043d\u044b\u0445",
                                       None))
        self.label.setText(QCoreApplication.translate("main_window",
                                                      u"\u0424\u0430\u043c\u0438\u043b\u0438\u044f \u0418\u043c\u044f "
                                                      u"\u041e\u0442\u0447\u0435\u0441\u0442\u0432\u043e",
                                                      None))
        self.pushButton_2.setText(QCoreApplication.translate("main_window", u"\u041f\u043e\u0438\u0441\u043a", None))
        self.label_2.setText(QCoreApplication.translate("main_window",
                                                        u"\u0414\u0430\u0442\u0430 "
                                                        u"\u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f",
                                                        None))
        self.checkBox.setText(
            QCoreApplication.translate("main_window", u"\u0412\u043a\u043b\u044e\u0447\u0438\u0442\u044c", None))
        self.pushButton_3.setText(
            QCoreApplication.translate("main_window", u"\u0412\u044b\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        self.pushButton_4.setText(
            QCoreApplication.translate("main_window", u"\u0418\u0437\u043c\u0435\u043d\u0438\u0442\u044c", None))
        self.pushButton_5.setText(
            QCoreApplication.translate("main_window", u"\u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", None))
        self.label_4.setText(QCoreApplication.translate("main_window",
                                                        u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 "
                                                        u"\u043f\u043e\u0438\u0441\u043a\u0430",
                                                        None))
        self.label_5.setText(
            QCoreApplication.translate("main_window", u"\u041f\u0440\u043e\u0441\u043c\u043e\u0442\u0440", None))
        self.menu.setTitle(
            QCoreApplication.translate("main_window", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = WindowUi()
    widget = QWidget()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
