from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QTextEdit, 
                           QPushButton, QFileDialog, QHBoxLayout)
from PyQt6.QtCore import Qt

class LogWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("日志窗口")
        self.setFixedSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # 创建文本编辑器用于显示日志
        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)  # 设置为只读
        layout.addWidget(self.log_text_edit)
        
        # 添加按钮
        button_layout = QHBoxLayout()
        clear_btn = QPushButton("清空日志")
        clear_btn.clicked.connect(self.clear_log)
        save_btn = QPushButton("保存日志")
        save_btn.clicked.connect(self.save_log)
        
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(save_btn)
        layout.addLayout(button_layout)
        
    def clear_log(self):
        """清空日志内容"""
        self.log_text_edit.clear()
        
    def save_log(self):
        """保存日志到文件"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存日志",
            "",
            "Text Files (*.txt);;All Files (*.*)"
        )
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.log_text_edit.toPlainText()) 