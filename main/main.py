# -*-coding:utf-8 -*-

"""
Created on 2024

@author: jysatuo
"""
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import sys
sys.path.append("..")
from ui.ai_playground_ui import *
from ui.login_ui import *
from ai_create import *
from ai.ai_cache import *
from ai.ai_transfer import ai_transfer
import requests
import re
import time
import function.global_var as global_var


def is_using_proxy():
    try:
        response = requests.get('http://google.com', timeout=1)
        # 如果响应成功，且不是预期的响应，则可能使用了代理
        if response.status_code != 404:
            os.environ["http_proxy"] = "http://localhost:7890"
            os.environ["https_proxy"] = "http://localhost:7890"
            os.environ['no_proxy'] = 'wx.qlogo.cn'   
            os.environ['no_proxy'] = 'timeus.top'  
            os.environ['no_proxy'] = '127.0.0.1:11434'
            os.environ['no_proxy'] = 'localhost:11434'            
            return True
        return False
    except requests.exceptions.ConnectionError:
        # 如果无法连接到服务，可能是代理问题
        return False
    except requests.exceptions.Timeout:
        # 如果请求超时，可能是网络问题而不是代理
        return False


class MainGui(QtWidgets.QMainWindow):
    
    def __init__(self,parent=None):
        super(QtWidgets.QMainWindow, self).__init__(parent)
        self.ui = Ui_LoginWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ai.ico')) # 设置图标
        self.ui.loginButton.clicked.connect(self.login)   
        self.ai_list = {}     
        global_var.init() #初始化全局变量
        global_var.set_value('conversation', {})         
        
    def entry(self):
        self.ui = Ui_ChatMainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('ai.ico')) # 设置图标
        self.center()
        self.to_ai = ""
        self.ui.sendButton.clicked.connect(self.send_message)
        self.ui.sendButton_2.clicked.connect(self.send_message)
        
        self.ui.pushButton_2.clicked.connect(self.role_gui) 
        self.ui.chatDisplay.setReadOnly(True)
        self.ui.chatDisplay.verticalScrollBar().setValue(self.ui.chatDisplay.verticalScrollBar().maximum())
        
        self.load_thread = loadThread()  
        self.load_thread.start() 
        
        item2 = QListWidgetItem(self.ui.settingList)
        item2.setText("AI角色")
        item2.setFont(QFont("SansSerif", 10, QFont.Bold))
        self.load_aiagent_thread = loadAiAgentThread(self.filepath)  
        self.load_aiagent_thread.start()  
        self.ui.settingList.itemDoubleClicked.connect(self.modify_ai)
        self.ui.settingList.setEditTriggers(QAbstractItemView.NoEditTriggers)  #不可编辑
       
        self.ui.settingList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.settingList.customContextMenuRequested.connect(self.show_custom_context_menu)       
        
        self.ui.comboBox.currentIndexChanged.connect(self.on_combobox_changed)
        self.ui.pushFileButton.clicked.connect(self.upload_file)
                
    def upload_file(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "选择文件", "", "All Files (*);")
        if file_path:
            file_extension = os.path.splitext(file_path)[1]
            image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
            if file_extension.lower() in image_extensions:
                self.upload_thread = uploadImageThread(file_path, "playground")
                self.upload_thread.start()  
            else:
                self.upload_thread = uploadFileThread(file_path, "playground")
                self.upload_thread.start()                     
        
    def on_combobox_changed(self, index):
        selected_option = self.ui.comboBox.itemText(index)
        if index == 4:
            self.ui.stackedWidget.setCurrentIndex(0)
        else:
            self.ui.stackedWidget.setCurrentIndex(1)
            
    def show_custom_context_menu2(self, pos):
        if not hasattr(self, "ai_takeover"):
            return
        index = self.ui.contactList.indexAt(pos)  
        row = index.row()
        wxid = self.mix_contacts[row-1]["wxid"]
        menu = QMenu()
        if wxid in self.ai_takeover:
            item0 = menu.addAction(QtGui.QIcon('ai.ico'), u"取消AI")   
            action = menu.exec_(self.ui.contactList.mapToGlobal(pos))              
            if action == item0:
                item = self.ui.contactList.item(row)
                new_text = self.mix_contacts[row-1]["nickname"]
                item.setText(new_text)
                self.ai_not_takeover_thread = aiNotTakeoverThread( self.filepath, self.mix_contacts[row-1]["wxid"])  
                self.ai_not_takeover_thread.start()            
        else:
            item1 = menu.addMenu(u"添加AI")  # 二级目录
            for n, ai in enumerate(self.ai_list):
                locals()[f'action_{n}'] = item1.addAction(QtGui.QIcon(ai["avatar"]),ai["name"])        
            action = menu.exec_(self.ui.contactList.mapToGlobal(pos))  
            for n, ai in enumerate(self.ai_list):
                    if action == locals()[f'action_{n}']:
                        item = self.ui.contactList.item(row)
                        new_text = f"{item.text()} √ {ai['name']} 接管"
                        item.setText(new_text)
                        self.ai_takeover_thread = aiTakeoverThread( self.filepath, self.mix_contacts[row-1]["wxid"], ai["msgid"])  
                        self.ai_takeover_thread.start()
        
    def show_custom_context_menu(self, pos):
        menu = QMenu()         
        index = self.ui.settingList.indexAt(pos)
        if re.search(rf"{self.ui.settingList.item(index.row()).text()}", self.to_ai):
            item0 = menu.addAction(QtGui.QIcon('ai.ico'), u"取消@") 
            item2 =""
        else:
            item2 = menu.addAction(QtGui.QIcon('ai.ico'), u"默认@")
            item0 = ""            
        item3 = menu.addAction(QtGui.QIcon('ai.ico'), u"@")   
        item1 = menu.addAction(QtGui.QIcon('ai.ico'), u"删除") 
        action = menu.exec_(self.ui.settingList.mapToGlobal(pos))
        if action == item1:
            index = self.ui.settingList.indexAt(pos)
            box = QMessageBox(QMessageBox.Question, '提示', '是否删除AI角色')
            yes = box.addButton('确认', QMessageBox.YesRole)
            no = box.addButton('取消', QMessageBox.NoRole)            
            box.setIcon(QMessageBox.Warning)
            box.setWindowIcon(QtGui.QIcon('ai.ico'))
            box.resize(240, 180)
            box.exec()             
            if box.clickedButton().text() == "确认":  
                if not hasattr(self, "ai_takeover"):
                    QMessageBox.information(self, '注意', '需等好友加载完成后进行操作！')    
                else:
                    self.thread = removeListRow(self.ui.settingList, index.row())
                    self.thread.text_signal.connect(self.input_text)   
                    self.thread.start() # 开启线程  
        elif action == item0:
            index = self.ui.settingList.indexAt(pos)
            n = index.row() - 1
            ai = self.ai_list[n]            
            self.to_ai = self.to_ai.replace(f"@{ai['name']} ", "")
            text = self.ui.inputEdit.toPlainText()
            text = text.replace(f"@{ai['name']} ", "")
            self.ui.inputEdit.setText(text)
        elif action == item2:
            index = self.ui.settingList.indexAt(pos)
            n = index.row() - 1
            ai = self.ai_list[n]
            self.to_ai = self.to_ai + f"@{ai['name']} "
            text = self.ui.inputEdit.toPlainText()
            self.ui.inputEdit.setText(text+ f"@{ai['name']} " )        
        elif action == item3:
            index = self.ui.settingList.indexAt(pos)
            n = index.row() - 1
            ai = self.ai_list[n]
            text = self.ui.inputEdit.toPlainText()
            self.ui.inputEdit.setText(text+ f"@{ai['name']} " )

    def center(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        size = self.geometry()
        newLeft = (screen.width() - size.width())/2
        newTop  = (screen.height() - size.height())/2
        self.move(int(newLeft), int(newTop))
        
    def modify_ai(self, item):
        n = self.ui.settingList.row(item)-1 # 获取点击的行号
        ai = self.ai_list[n]
        self.dialog_createrole2 = CreateRole(self.filepath, ai, n)
        self.dialog_createrole2.setWindowIcon(QtGui.QIcon('ai.ico')) # 设置图标        
        self.dialog_createrole2.setWindowTitle("AI角色编辑")              
        self.dialog_createrole2.setModal(True)  
        self.dialog_createrole2.refresh_signal.connect(self.refresh_changed)
        self.dialog_createrole2.show()   
    
    def refresh_changed(self, ai_role, msg, n):
        "AI角色有变动时刷新列表"
        self.refresh_role_thread = afterCreatAiAgentThread(ai_role, msg, n)
        self.refresh_role_thread.scroll_signal.connect(self.scroll_to_bottom)
        self.refresh_role_thread.start()
    
    def role_gui(self):
        self.dialog_createrole = CreateRole(self.filepath)
        self.dialog_createrole.setWindowIcon(QtGui.QIcon('ai.ico')) # 设置图标        
        self.dialog_createrole.setModal(True)     
        self.dialog_createrole.refresh_signal.connect(self.refresh_changed)        
        self.dialog_createrole.show()     
    
    def display_message(self, message:str="", align_right:bool=False, avatar_path:str=""):
        if align_right:
            message = f"<span>{message}</span><br>"
        else:
            if avatar_path:
                message = f"<span style=color:#00aa7f><img src='{avatar_path}' width=8 height=8></img>{message}</span><br>"
            else:
                message = f"<span style=color:#00aa7f>{message}</span><br>"
        self.ui.chatDisplay.append(message)
        
    def send_message(self):
        message = self.ui.inputEdit.toPlainText()
        self.display_message('You: ' + message, align_right=True)        
        self.ui.inputEdit.clear()   
        self.ui.inputEdit.setText(self.to_ai) # 加载默认的@
        self.ai_thread = aiThread(message) # 创建登入程序线程
        self.ai_thread.display_signal.connect(self.display_message)          
        self.ai_thread.start() # 开启线程             
    
    def login(self):
        # 登入微信
        telephone = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        self.login_thread = loginThread(telephone, password) 
        self.login_thread.login_signal.connect(self.entry)   
        self.login_thread.login_err_signal.connect(self.login_err)           
        self.login_thread.finished_signal.connect(self.login_finished)
        self.login_thread.start() 
        
    def login_err(self):
        box = QMessageBox(QMessageBox.Warning, '提示', '手机号或者密码错误')
        yes = box.addButton('确认', QMessageBox.YesRole)
        no = box.addButton('取消', QMessageBox.NoRole)  
        box.setIcon(QMessageBox.Warning)
        box.setWindowIcon(QtGui.QIcon('ai.ico'))
        box.resize(240, 180)
        box.exec()          
    
    def login_finished(self):
        pass
    
    def scroll_to_bottom(self):
        QTimer.singleShot(100, self.scroll_helper)

    def scroll_helper(self):
        self.ui.settingList.verticalScrollBar().setValue(self.ui.settingList.verticalScrollBar().maximum())
    
    def input_text(self, text):
        self.ui.inputEdit.setText(text) 
    
    
class removeListRow(QThread):
    """删除列表某行"""
    text_signal = pyqtSignal(str)
    reload_signal = pyqtSignal()
    
    def __init__(self, List, row):
        super(removeListRow, self).__init__()
        self.List = List
        self.row = row
        self.file = "config.conf"
        
    def run(self):
        item= myapp.ai_list[self.row-1]
        self.List.takeItem(self.row) 
        text = myapp.ui.inputEdit.toPlainText()
        text = text.replace(f"@{item['name']} ", "")
        self.text_signal.emit(text)
        myapp.to_ai = myapp.to_ai.replace(f"@{item['name']} ", "")
        del  myapp.ai_list[self.row-1]
        keys_to_remove = []
        for n, contact in enumerate(myapp.mix_contacts):
            wxid = contact["wxid"]
            msgid = myapp.ai_takeover.get(wxid)
            if msgid==item["msgid"]:
                itm = myapp.ui.contactList.item(n+1)
                itm.setText(contact["nickname"])   
                keys_to_remove.append(wxid)
        for key in keys_to_remove:
            myapp.ai_takeover.pop(key)
        
        filename = f"{myapp.filepath}/ai_takeover.conf"
        with open(filename, 'w') as file:
                json.dump( myapp.ai_takeover, file)        
        with open(myapp.filepath + self.file, "r" ) as f:
            file = f.read()
            old_data = json.loads(file)
            del old_data[self.row-1]    
        with open(myapp.filepath + self.file, "w") as f:                                            
            json.dump(old_data, f) 
        
            
class aiThread(QThread):
    """AI线程"""
    display_signal = pyqtSignal(str, bool, str)
    
    def __init__(self, message:str=""):
        super(aiThread,self).__init__()
        self.ui = myapp.ui
        self.message = message
        self.ai_reply = [] # @Ai的数量 

    def insert_char_at_position(self, original_string, char_to_insert, position):
        # 确保位置不会超出字符串的长度,字符串中插入头像
        if position > len(original_string):
            return original_string
        first_part = original_string[:position]
        second_part = original_string[position:]
        new_string = first_part + char_to_insert + second_part
        return new_string

    def common_subsequence_ratio(self, s1, s2):
        # 创建一个二维数组来存储子问题的解
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        # 填充dp数组
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i - 1] == s2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        # 返回公共子序列长度与较长字符串长度的比值
        return dp[m][n] / max(m, n)
    
    def match_name(self, text):
        new_string = text
        has_match = False
        name_pattern = r'(?<![\w.])([\u4e00-\u9fffA-Za-z0-9]+)(?![\w.])'
        # 使用re.finditer查找所有匹配的名字及其位置
        matches = re.finditer(name_pattern, text)     
        # 打印出所有找到的名字及其位置
        for match in reversed(list(matches)):
            name = match.group()
            start_index = match.start()
            for ai in self.ai_reply:
                match_degree = self.common_subsequence_ratio(ai['name'], name)
                if  match_degree >= 0.8:
                    new_string = self.insert_char_at_position(new_string, f"<img src='{ai['avatar']}' width=8 height=8></img>", start_index)
                    has_match = True
        return new_string, has_match 
    
    def update(self, kwargs):
        for key, value in kwargs.items():
            setattr(myapp, key, value)       
            
    def run(self):
        for ai in myapp.ai_list:
            if re.search(rf"@{ai['name']}\b", self.message):
                self.ai_reply.append(ai)
        for ai in self.ai_reply:
            myapp.messages_dict[ai["msgid"]].append({'content': self.message, 'role': 'user'})
            content, messages = ai_transfer(myapp, myapp.ui.comboBox.currentText(), myapp.messages_dict[ai["msgid"]], ai)
            myapp.messages_dict[ai["msgid"]] = messages
            ai_reply_temp = self.ai_reply
            for ai_temp in self.ai_reply:
                if ai_temp == ai:  # 跳过当前AI
                    continue
                myapp.messages_dict[ai_temp["msgid"]].append({'content':  f"下面是其他AI角色发布的文字，结合起来作为回答问题的基础，在对话结尾换行，换行符号为<br>，角色{ai['name']}说："+content, 'role': 'assistant'})    
            # 回复完后进行统一展示
            if ai == self.ai_reply[-1]:
                if len(self.ai_reply) == 1:
                    content, has_match = self.match_name(content)
                    if has_match:
                        self.display_signal.emit(content.replace("\n", "<br>"), False, "") 
                    else:
                        self.display_signal.emit(f"{ai['name']}："+content.replace("\n", "<br>"), False, ai["avatar"]) 
                else:                    
                    content, _ = self.match_name(content)
                    self.display_signal.emit(content.replace("\n", "<br>"), False, "") 
                              
        if not self.ai_reply:
            myapp.messages.append({'content': self.message, 'role': 'user'})
            content, messages = ai_transfer(myapp, myapp.ui.comboBox.currentText(), myapp.messages)
            myapp.messages = messages
            myapp.content = content
            self.display_signal.emit("AI：" + content.replace("\n", "<br>"), False, "")
            save_history(myapp.filepath, messages)  
        else:
            save_messages_dict(myapp.filepath, myapp.messages_dict) # 保存messages_list
                                          
                        
class afterCreatAiAgentThread(QThread):
    scroll_signal = pyqtSignal()
    
    def __init__(self, ai_role, msg, n):
        super(afterCreatAiAgentThread,self).__init__()
        self.ai_role = ai_role
        self.msg = msg
        self.n = n
    
    def run(self):
        if self.n != -1:
            item = myapp.ui.settingList.item(self.n+1)
            new_text = self.ai_role["name"]
            item.setText(new_text)  
            QIcon = QtGui.QIcon(self.ai_role["avatar"])
            item.setIcon(QIcon)
            myapp.ai_list[self.n] = self.ai_role
            myapp.messages_dict[self.ai_role["msgid"]] = self.msg            
        else:
            item = QListWidgetItem(self.ai_role["name"])
            QIcon = QtGui.QIcon(self.ai_role["avatar"])
            item.setIcon(QIcon)                       
            myapp.ui.settingList.addItem(item)   
            myapp.ai_list.append(self.ai_role)
            myapp.messages_dict[self.ai_role["msgid"]] = self.msg   
            self.scroll_signal.emit()

                  
class loadAiAgentThread(QThread):
    """加载AI角色线程"""
    
    def __init__(self, filepath):
        super(loadAiAgentThread,self).__init__()
        self.ui = myapp.ui  
        self.filepath = filepath
    
    def run(self):
        filename = f"{self.filepath}/config.conf"
        if os.path.isfile(filename):
            with open(filename, 'r') as file:
                array_str = file.read()
                if len(array_str):
                    array = json.loads(array_str)
                    self.ui.settingList.clear()
                    item2 = QListWidgetItem(self.ui.settingList)
                    item2.setText("AI角色")
                    item2.setFont(QFont("SansSerif", 10, QFont.Bold))                    
                    for itm in array:
                        item = QListWidgetItem(itm["name"])
                        QIcon = QtGui.QIcon(itm["avatar"])
                        item.setIcon(QIcon) # 设置图标                        
                        self.ui.settingList.addItem(item)      
                    myapp.ai_list = array
                    messages_dict = load_messages_dict(myapp.filepath, array)
                    myapp.messages_dict = messages_dict
              
                    
class loadThread(QThread):
    """加载微信数据线程"""
    
    def __init__(self):
        super(loadThread,self).__init__()
        self.ui = myapp.ui
        
    def run(self):
        # 导入模型
        filename = f"../ai/key.json"
        with open(filename, 'r') as file:
            dict_str = file.read()
            dict_ = json.loads(dict_str)
            myapp.models = dict_["MODELS"]
            myapp.key = dict_           
            for model in myapp.models:
                myapp.ui.comboBox.addItem(model)
            myapp.ui.comboBox.setCurrentIndex(0)  # 初始化为0
 
           
class loginThread(QThread):
    """登录程序线程"""
    login_signal = pyqtSignal()
    finished_signal = pyqtSignal()
    login_err_signal = pyqtSignal()
    
    def __init__(self, telephone, password):
        super(loginThread,self).__init__()
        self.telephone = telephone
        self.password = password
        self.ui = myapp.ui
        
    def run(self):
        loginStatus = False
        if self.telephone and self.password:
            self.ui.loginButton.setText("验证中")
            self.ui.loginButton.setEnabled(False)  
            loginStatus = True 
            #endpoint = "https://timeus.top/v1/user/login"
            #data = {"telephone": self.telephone, "verification_code": "", "password": self.password}
            #res = requests.post(endpoint, json=data)
            #if res.status_code == 200:
                #loginStatus = True 
                #self.ui.loginButton.setText("正在连接微信和加载数据，请稍等")
                #self.ui.loginButton.setEnabled(False)                 
        if not loginStatus:
            self.login_err_signal.emit() 
            self.ui.loginButton.setText("Login")
            self.ui.loginButton.setEnabled(True)               
            
        if loginStatus:     
            self.login_signal.emit()
            #导入json文件
            myapp.filepath = f"../file/history_messages/" 
            if not os.path.exists(myapp.filepath):
                os.makedirs(myapp.filepath)            
            myapp.messages = load_history(myapp.filepath)  # 导入ai历史数据
            self.finished_signal.emit()
                                           
  
 
if __name__ == "__main__":
    import multiprocessing
    multiprocessing.freeze_support()
    is_using_proxy()        
    # ----------------------------------------------
    QtWidgets.QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QtWidgets.QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  
    app = QtWidgets.QApplication(sys.argv)
    myapp = MainGui()
    myapp.show()
    sys.exit(app.exec_())
