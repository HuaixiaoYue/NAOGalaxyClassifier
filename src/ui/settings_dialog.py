from PyQt6.QtWidgets import (QDialog, QTabWidget, QWidget, QVBoxLayout,
                           QHBoxLayout, QLabel, QSpinBox, QDoubleSpinBox,
                           QPushButton, QFileDialog, QCheckBox, QComboBox,
                           QGroupBox, QSlider)
from PyQt6.QtCore import Qt
from pathlib import Path

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("设置")
        self.setFixedSize(600, 500)
        
        # 创建主布局
        layout = QVBoxLayout(self)
        
        # 创建选项卡
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)
        
        # 添加各个设置页面
        tab_widget.addTab(ModelSettingsTab(), "模型设置")
        tab_widget.addTab(DataProcessingTab(), "数据处理")
        tab_widget.addTab(SaveSettingsTab(), "保存设置")
        
        # 添加确定和取消按钮
        button_layout = QHBoxLayout()
        layout.addLayout(button_layout)
        
        save_btn = QPushButton("确定")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)

class ModelSettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 预训练模型设置
        model_group = QGroupBox("预训练模型设置")
        model_layout = QVBoxLayout(model_group)
        
        # 模型选择
        model_select_layout = QHBoxLayout()
        model_label = QLabel("预训练模型:")
        self.model_combo = QComboBox()
        self.model_combo.addItems(["ResNet18", "ResNet34", "ResNet50", "VGG16"])
        model_select_layout.addWidget(model_label)
        model_select_layout.addWidget(self.model_combo)
        model_select_layout.addStretch()
        model_layout.addLayout(model_select_layout)
        
        # 模型路径
        model_path_layout = QHBoxLayout()
        path_label = QLabel("模型路径:")
        self.path_edit = QLabel("未选择")
        browse_btn = QPushButton("浏览")
        browse_btn.clicked.connect(self.browse_model)
        model_path_layout.addWidget(path_label)
        model_path_layout.addWidget(self.path_edit)
        model_path_layout.addWidget(browse_btn)
        model_layout.addLayout(model_path_layout)
        
        layout.addWidget(model_group)
        layout.addStretch()
        
    def browse_model(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择预训练模型",
            str(Path.home()),
            "Model Files (*.pth *.pt);;All Files (*.*)"
        )
        if file_path:
            self.path_edit.setText(file_path)

class DataProcessingTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 图像预处理设置
        preprocess_group = QGroupBox("图像预处理")
        preprocess_layout = QVBoxLayout(preprocess_group)
        
        # 图像大小设置
        size_layout = QHBoxLayout()
        size_label = QLabel("图像大小:")
        self.size_spin = QSpinBox()
        self.size_spin.setRange(32, 512)
        self.size_spin.setValue(224)
        self.size_spin.setSuffix(" px")
        size_layout.addWidget(size_label)
        size_layout.addWidget(self.size_spin)
        size_layout.addStretch()
        preprocess_layout.addLayout(size_layout)
        
        # 数据增强选项
        augment_group = QGroupBox("数据增强")
        augment_layout = QVBoxLayout(augment_group)
        
        self.rotate_check = QCheckBox("随机旋转")
        self.flip_check = QCheckBox("随机翻转")
        self.scale_check = QCheckBox("随机缩放")
        
        augment_layout.addWidget(self.rotate_check)
        augment_layout.addWidget(self.flip_check)
        augment_layout.addWidget(self.scale_check)
        
        # 数据划分比例
        split_group = QGroupBox("数据划分比例")
        split_layout = QVBoxLayout(split_group)
        
        # 训练集比例
        train_split_layout = QHBoxLayout()
        train_split_layout.addWidget(QLabel("训练集:"))
        self.train_split = QSpinBox()
        self.train_split.setRange(50, 90)
        self.train_split.setValue(70)
        self.train_split.setSuffix("%")
        train_split_layout.addWidget(self.train_split)
        
        # 验证集比例
        val_split_layout = QHBoxLayout()
        val_split_layout.addWidget(QLabel("验证集:"))
        self.val_split = QSpinBox()
        self.val_split.setRange(5, 30)
        self.val_split.setValue(20)
        self.val_split.setSuffix("%")
        val_split_layout.addWidget(self.val_split)
        
        # 测试集比例会自动计算
        test_split_label = QLabel("测试集: 自动计算剩余比例")
        
        split_layout.addLayout(train_split_layout)
        split_layout.addLayout(val_split_layout)
        split_layout.addWidget(test_split_label)
        
        layout.addWidget(preprocess_group)
        layout.addWidget(augment_group)
        layout.addWidget(split_group)
        layout.addStretch()

class SaveSettingsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 保存路径设置
        path_group = QGroupBox("保存路径设置")
        path_layout = QVBoxLayout(path_group)
        
        # 模型保存路径
        model_path_layout = QHBoxLayout()
        model_path_label = QLabel("模型保存路径:")
        self.model_path_edit = QLabel("未选择")
        model_browse_btn = QPushButton("浏览")
        model_browse_btn.clicked.connect(lambda: self.browse_path(self.model_path_edit))
        model_path_layout.addWidget(model_path_label)
        model_path_layout.addWidget(self.model_path_edit)
        model_path_layout.addWidget(model_browse_btn)
        path_layout.addLayout(model_path_layout)
        
        # 自动保存设置
        auto_save_group = QGroupBox("自动保存设置")
        auto_save_layout = QVBoxLayout(auto_save_group)
        
        # 保存频率
        freq_layout = QHBoxLayout()
        freq_label = QLabel("保存频率:")
        self.freq_spin = QSpinBox()
        self.freq_spin.setRange(1, 100)
        self.freq_spin.setValue(10)
        self.freq_spin.setSuffix(" epochs")
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(self.freq_spin)
        freq_layout.addStretch()
        auto_save_layout.addLayout(freq_layout)
        
        # 保存检查点
        self.save_checkpoint = QCheckBox("保存检查点")
        self.save_checkpoint.setChecked(True)
        auto_save_layout.addWidget(self.save_checkpoint)
        
        layout.addWidget(path_group)
        layout.addWidget(auto_save_group)
        layout.addStretch()
        
    def browse_path(self, label_widget):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择保存路径",
            str(Path.home())
        )
        if folder_path:
            label_widget.setText(folder_path) 