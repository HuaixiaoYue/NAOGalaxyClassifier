from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                           QLabel, QLineEdit, QPushButton, 
                           QListWidget, QMessageBox)
from PyQt6.QtCore import Qt
from pathlib import Path
from utils.dataset_config import DatasetConfig

class DatasetConfigDialog(QDialog):
    def __init__(self, project_path: Path, parent=None):
        super().__init__(parent)
        self.dataset_config = DatasetConfig(project_path)
        self.setup_ui()
        self.load_config()
    
    def setup_ui(self):
        self.setWindowTitle("数据集配置")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # 类别列表
        layout.addWidget(QLabel("类别列表:"))
        self.class_list = QListWidget()
        layout.addWidget(self.class_list)
        
        # 添加类别
        add_layout = QHBoxLayout()
        self.class_input = QLineEdit()
        self.class_input.setPlaceholderText("输入类别名称")
        add_layout.addWidget(self.class_input)
        
        add_btn = QPushButton("添加")
        add_btn.clicked.connect(self.add_class)
        add_layout.addWidget(add_btn)
        
        layout.addLayout(add_layout)
        
        # 删除类别按钮
        delete_btn = QPushButton("删除所选类别")
        delete_btn.clicked.connect(self.delete_class)
        layout.addWidget(delete_btn)
        
        # 确定取消按钮
        button_layout = QHBoxLayout()
        save_btn = QPushButton("确定")
        save_btn.clicked.connect(self.save_config)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
    
    def load_config(self):
        """加载现有配置"""
        config = self.dataset_config.load_config()
        self.class_list.clear()
        self.class_list.addItems(config['names'])
    
    def add_class(self):
        """添加新类别"""
        class_name = self.class_input.text().strip()
        if not class_name:
            return
        
        # 检查是否重复
        existing_items = [self.class_list.item(i).text() 
                         for i in range(self.class_list.count())]
        if class_name in existing_items:
            QMessageBox.warning(self, "警告", "该类别已存在！")
            return
        
        self.class_list.addItem(class_name)
        self.class_input.clear()
    
    def delete_class(self):
        """删除选中的类别"""
        current_item = self.class_list.currentItem()
        if current_item:
            self.class_list.takeItem(self.class_list.row(current_item))
    
    def save_config(self):
        """保存配置"""
        class_names = [self.class_list.item(i).text() 
                      for i in range(self.class_list.count())]
        
        if not class_names:
            QMessageBox.warning(self, "警告", "请至少添加一个类别！")
            return
        
        # 创建目录结构
        self.dataset_config.create_directory_structure()
        
        # 更新配置文件
        self.dataset_config.update_class_info(class_names)
        
        self.accept() 