import sys
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QLabel, QLineEdit, QPushButton

class MyDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("QGridLayout 自适应")
        self.resize(400, 200)

        # 创建网格布局
        layout = QGridLayout()

        # 标签 + 输入框
        layout.addWidget(QLabel("用户名:"), 0, 0)
        self.username = QLineEdit()
        layout.addWidget(self.username, 0, 1)

        layout.addWidget(QLabel("密码:"), 1, 0)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password, 1, 1)

        # 按钮
        self.ok_button = QPushButton("登录")
        layout.addWidget(self.ok_button, 2, 0, 1, 2)  # 按钮跨两列

        # 设置布局
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = MyDialog()
    dialog.exec()
