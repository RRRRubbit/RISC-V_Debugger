from PyQt5.QtCore import Qt, QRect, QRegularExpression
from PyQt5.QtGui import QColor, QPainter, QTextCursor, QTextCharFormat
from PyQt5.QtWidgets import QApplication, QMainWindow, QPlainTextEdit, QVBoxLayout, QWidget


class CodeEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # 重新设置行号区域的宽度
        self.lineNumberArea.setGeometry(QRect(0, 0, self.lineNumberAreaWidth(), self.height()))


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(event.rect(), QColor(240, 240, 240))  # 背景颜色
        painter.setPen(QColor(120, 120, 120))  # 行号的颜色

        block = self.editor.firstVisibleBlock()  # 获取文本框中第一个可见的块
        blockNumber = block.blockNumber()  # 获取块的行号
        top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()  # 获取该行的顶部位置
        bottom = top + self.editor.blockBoundingGeometry(block).height()  # 获取该行的底部位置

        while block.isValid():
            if top > event.rect().bottom():
                break
            if bottom >= event.rect().top():
                lineNumber = str(blockNumber + 1)  # 行号从 1 开始
                painter.drawText(0, int(top), self.width(), self.fontMetrics().height(), Qt.AlignRight, lineNumber)  # 绘制行号
            block = block.next()  # 移动到下一个块
            top = bottom
            bottom = top + self.editor.blockBoundingGeometry(block).height()
            blockNumber += 1


class CodeEditorWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.editor = CodeEditor()
        self.setCentralWidget(self.editor)

        # 为编辑器创建一个行号区域
        self.lineNumberArea = LineNumberArea(self.editor)
        self.editor.lineNumberArea = self.lineNumberArea

        # 布局管理
        layout = QVBoxLayout()
        layout.addWidget(self.editor)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setGeometry(100, 100, 800, 600)
        self.show()

    def loadCode(self, filename):
        with open(filename, 'r') as file:
            content = file.read()
            self.editor.setPlainText(content)  # 加载代码


if __name__ == "__main__":
    app = QApplication([])

    window = CodeEditorWidget()
    window.loadCode('/home/sun/下载/demo_setup_sun/main.asm')  # 替换为实际文件路径

    app.exec_()
