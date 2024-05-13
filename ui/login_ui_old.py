# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(324, 121)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.usernameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.usernameEdit.setStyleSheet("#usernameEdit {\n"
"    border: 1px solid #ccc; /* 设置边框样式 */\n"
"    border-radius: 5px; /* 设置边框圆角 */\n"
"    padding: 5px; /* 设置内边距 */\n"
"    font-size: 14px; /* 设置字体大小 */\n"
"}\n"
"\n"
"#usernameEdit:focus {\n"
"    border: 2px solid rgb(20,196,188); /* 输入框获取焦点时的边框样式 */\n"
"}\n"
"")
        self.usernameEdit.setObjectName("usernameEdit")
        self.verticalLayout.addWidget(self.usernameEdit)
        self.passwordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.passwordEdit.setStyleSheet("#passwordEdit {\n"
"    border: 1px solid #ccc; /* 设置边框样式 */\n"
"    border-radius: 5px; /* 设置边框圆角 */\n"
"    padding: 5px; /* 设置内边距 */\n"
"    font-size: 14px; /* 设置字体大小 */\n"
"}\n"
"\n"
"#passwordEdit:focus {\n"
"    border: 2px solid rgb(20,196,188); /* 输入框获取焦点时的边框样式 */\n"
"}\n"
"")
        self.passwordEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordEdit.setObjectName("passwordEdit")
        self.verticalLayout.addWidget(self.passwordEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.loginButton = QtWidgets.QPushButton(self.centralwidget)
        self.loginButton.setStyleSheet("#loginButton {\n"
"    background-color: rgb(20,196,188);\n"
"    color: white; \n"
"    border: 2px solid rgb(20,196,188);\n"
"    border-radius: 5px; \n"
"    padding: 5px 10px; \n"
"    font-size: 14px; \n"
"}\n"
"\n"
"#loginButton:hover {\n"
"    background-color:  rgb(22,218,208);\n"
"}\n"
"\n"
"#loginButton:pressed {\n"
"    background-color: rgb(17,171,164);\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    font: 25 14pt \'微软雅黑\';\n"
"    color: rgb(255,255,255);\n"
"    background-color: rgb(20,196,188);\n"
"    border:none;\n"
"    border-radius:10px;\n"
"}\n"
"QPushButton:hover\n"
"{\n"
"    background-color: rgb(22,218,208);\n"
"}\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: rgb(17,171,164);\n"
"}")
        self.loginButton.setObjectName("loginButton")
        self.verticalLayout_3.addWidget(self.loginButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("LoginWindow", "授权码："))
        self.label_2.setText(_translate("LoginWindow", "API Key："))
        self.usernameEdit.setPlaceholderText(_translate("LoginWindow", "请从管理员中获取授权码进行绑定"))
        self.loginButton.setText(_translate("LoginWindow", "Login"))
        LoginWindow.setWindowTitle(_translate("LoginWindow", "微信AI智能伙伴"))
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())

