from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QSpinBox, QDoubleSpinBox, 
                           QComboBox, QGroupBox, QProgressBar,
                           QCheckBox)
from PyQt6.QtCore import Qt

class TrainingPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 模型参数组
        model_group = QGroupBox("模型参数")
        model_layout = QVBoxLayout()
        
        # 模型大小选择
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("模型大小:"))
        self.size_combo = QComboBox()
        self.size_combo.addItems(["nano", "small", "medium", "large", "xlarge"])
        size_layout.addWidget(self.size_combo)
        size_layout.addStretch()
        model_layout.addLayout(size_layout)
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # 训练参数组
        train_group = QGroupBox("训练参数")
        train_layout = QVBoxLayout()
        
        # 图像尺寸设置
        img_size_layout = QHBoxLayout()
        img_size_layout.addWidget(QLabel("图像尺寸:"))
        self.img_size_spin = QSpinBox()
        self.img_size_spin.setRange(32, 1280)
        self.img_size_spin.setValue(640)
        self.img_size_spin.setSingleStep(32)
        img_size_layout.addWidget(self.img_size_spin)
        img_size_layout.addWidget(QLabel("(32-1280)"))
        img_size_layout.addStretch()
        train_layout.addLayout(img_size_layout)
        
        # 批次大小设置
        batch_size_layout = QHBoxLayout()
        batch_size_layout.addWidget(QLabel("批次大小:"))
        self.batch_size_spin = QSpinBox()
        self.batch_size_spin.setRange(1, 128)
        self.batch_size_spin.setValue(16)
        batch_size_layout.addWidget(self.batch_size_spin)
        batch_size_layout.addWidget(QLabel("(1-128)"))
        batch_size_layout.addStretch()
        train_layout.addLayout(batch_size_layout)
        
        # 学习率设置
        lr_layout = QHBoxLayout()
        lr_layout.addWidget(QLabel("学习率:"))
        self.lr_spin = QDoubleSpinBox()
        self.lr_spin.setRange(0.0001, 0.1)
        self.lr_spin.setValue(0.01)
        self.lr_spin.setDecimals(4)
        lr_layout.addWidget(self.lr_spin)
        lr_layout.addWidget(QLabel("(0.0001-0.1)"))
        lr_layout.addStretch()
        train_layout.addLayout(lr_layout)
        
        # 训练轮数设置
        epochs_layout = QHBoxLayout()
        epochs_layout.addWidget(QLabel("训练轮数:"))
        self.epochs_spin = QSpinBox()
        self.epochs_spin.setRange(1, 1000)
        self.epochs_spin.setValue(100)
        epochs_layout.addWidget(self.epochs_spin)
        epochs_layout.addWidget(QLabel("(1-1000)"))
        epochs_layout.addStretch()
        train_layout.addLayout(epochs_layout)
        
        # 预训练权重选项
        pretrain_layout = QHBoxLayout()
        self.pretrain_check = QCheckBox("使用预训练权重")
        self.pretrain_check.setChecked(True)
        pretrain_layout.addWidget(self.pretrain_check)
        pretrain_layout.addStretch()
        train_layout.addLayout(pretrain_layout)
        
        train_group.setLayout(train_layout)
        layout.addWidget(train_group)
        
        # 添加进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 添加弹性空间
        layout.addStretch()
    
    def get_training_params(self):
        """获取训练参数"""
        return {
            'model_size': self.size_combo.currentText(),
            'img_size': self.img_size_spin.value(),
            'batch_size': self.batch_size_spin.value(),
            'learning_rate': self.lr_spin.value(),
            'epochs': self.epochs_spin.value(),
            'pretrained': self.pretrain_check.isChecked()
        }
    
    def set_training_params(self, params: dict):
        """设置训练参数"""
        if 'model_size' in params:
            index = self.size_combo.findText(params['model_size'])
            if index >= 0:
                self.size_combo.setCurrentIndex(index)
        if 'img_size' in params:
            self.img_size_spin.setValue(params['img_size'])
        if 'batch_size' in params:
            self.batch_size_spin.setValue(params['batch_size'])
        if 'learning_rate' in params:
            self.lr_spin.setValue(params['learning_rate'])
        if 'epochs' in params:
            self.epochs_spin.setValue(params['epochs'])
        if 'pretrained' in params:
            self.pretrain_check.setChecked(params['pretrained']) 