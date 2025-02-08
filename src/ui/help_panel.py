from PyQt6.QtWidgets import (QDialog, QWidget, QVBoxLayout, QLabel, 
                           QScrollArea, QFrame, QPushButton)
from PyQt6.QtCore import Qt

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # 设置窗口标题和大小
        self.setWindowTitle("帮助")
        self.setFixedSize(400, 500)
        
        # 创建主布局
        layout = QVBoxLayout(self)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        layout.addWidget(scroll)
        
        # 创建内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        scroll.setWidget(content_widget)
        
        # 设置样式
        content_widget.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
            }
        """)
        
        # 添加帮助内容
        titles = [
            ("数据上传", "点击'上传训练数据'按钮，选择包含训练图片的文件夹。支持jpg和png格式。"),
            ("参数设置", "在训练参数面板中设置批次大小、学习率和训练轮数等参数。"),
            ("开始训练", "上传数据后，点击'开始训练'按钮开始训练过程。训练过程中可以查看进度。"),
            ("数据预览", "右侧面板显示已上传的训练图片预览。"),
        ]
        
        for title, desc in titles:
            # 添加标题
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    font-weight: bold;
                    color: #333333;
                    padding: 10px 5px;
                }
            """)
            content_layout.addWidget(title_label)
            
            # 添加描述
            desc_label = QLabel(desc)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("""
                QLabel {
                    color: #666666;
                    padding: 0px 5px 15px 5px;
                }
            """)
            content_layout.addWidget(desc_label)
        
        # 添加弹性空间
        content_layout.addStretch()
        
        # 添加关闭按钮
        close_button = QPushButton("关闭")
        close_button.setFixedWidth(100)
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        # 创建按钮布局并添加到主布局
        button_layout = QVBoxLayout()
        button_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(button_layout) 