from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QPushButton, QFileDialog, QLabel,
                           QHBoxLayout, QStatusBar, QToolBar)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from pathlib import Path
from .training_panel import TrainingPanel
from utils.path_manager import PathManager
from utils.config_manager import ConfigManager
from .preview_panel import PreviewPanel
import time
from PyQt6.QtWidgets import QApplication
from .help_panel import HelpDialog
from .settings_dialog import SettingsDialog
from PyQt6.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("星系分类器")
        self.setMinimumSize(1000, 600)
        
        self.path_manager = PathManager()
        self.config_manager = ConfigManager()
        self.load_user_settings()
        self.help_panel = None  # 初始化为None
        self.setup_ui()
        

        self.status_label.setText("请上传训练数据...")
    
    def load_user_settings(self):
        """加载用户设置"""
        self.config = self.config_manager.load_config()
    
    def save_user_settings(self, dialog):
        """保存用户设置"""
        self.config['training_params'] = self.training_panel.get_training_params()
        self.config_manager.save_config(self.config)
    
    def closeEvent(self, event):
        """窗口关闭时保存设置"""
        self.save_user_settings(None)
        super().closeEvent(event)
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧控制面板
        control_panel = QWidget()
        control_layout = QVBoxLayout(control_panel)
        
        # 添加文件上传按钮
        self.upload_btn = QPushButton("上传训练数据")
        self.upload_btn.setIcon(QIcon("icons/upload.png"))  # 添加图标
        self.upload_btn.setToolTip("点击上传训练数据文件夹")
        self.upload_btn.clicked.connect(self.upload_data)
        control_layout.addWidget(self.upload_btn)
        
        # 添加状态标签
        self.status_label = QLabel("请上传训练数据...")
        self.status_label.setMaximumWidth(100)  # 设置最大宽度
        self.status_label.setWordWrap(True)  # 启用自动换行
        control_layout.addWidget(self.status_label)
        
        # 添加训练按钮
        self.train_btn = QPushButton("开始训练")
        self.train_btn.setIcon(QIcon("icons/train.png"))  # 添加图标
        self.train_btn.setToolTip("点击开始训练模型")
        self.train_btn.setEnabled(False)
        self.train_btn.clicked.connect(self.start_training)
        control_layout.addWidget(self.train_btn)
        
        # 添加弹性空间
        control_layout.addStretch()
        
        # 中间训练参数面板
        self.training_panel = TrainingPanel()
        
        # 右侧预览面板
        self.preview_panel = PreviewPanel()
        
        # 将面板添加到主布局
        main_layout.addWidget(control_panel, 1)      # 比例1
        main_layout.addWidget(self.training_panel, 2) # 比例2
        main_layout.addWidget(self.preview_panel, 3)  # 比例3
        
        # 添加状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("准备就绪")
        
        # 添加工具栏
        toolbar = QToolBar("主工具栏")
        self.addToolBar(toolbar)
        toolbar.addAction(QIcon("icons/open.png"), "打开", self.upload_data)
        toolbar.addAction(QIcon("icons/save.png"), "保存", self.save_user_settings)
        
        # 添加帮助按钮
        help_action = toolbar.addAction(QIcon("icons/help.png"), "帮助")
        help_action.setToolTip("显示帮助信息")
        help_action.triggered.connect(self.toggle_help_panel)
        
        # 添加设置按钮
        settings_action = toolbar.addAction(QIcon("icons/settings.png"), "设置")
        settings_action.setToolTip("打开设置")
        settings_action.triggered.connect(self.open_settings)
    
    def upload_data(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "选择训练数据文件夹",
            self.config.get('last_upload_path', str(Path.home())),
            QFileDialog.Option.ShowDirsOnly  # 只显示文件夹
        )
        
        if folder_path:
            try:
                # 检查目录结构：每个子文件夹作为一个类别
                folder_path = Path(folder_path)
                class_dirs = [d for d in folder_path.iterdir() if d.is_dir()]
                
                if not class_dirs:
                    self.status_label.setText("错误：未找到分类目录，请确保数据按类别分类存放")
                    return
                
                # 递归查找所有图片文件
                image_files = []
                for class_dir in class_dirs:
                    class_images = list(class_dir.glob("**/*.jpg")) + \
                                 list(class_dir.glob("**/*.png"))
                    if not class_images:
                        self.status_label.setText(f"警告：类别 '{class_dir.name}' 中未找到图片文件")
                        return
                    image_files.extend(class_images)
                
                # 保存数据
                saved_path = self.path_manager.save_training_data(folder_path)
                self.status_label.setText(f"数据已保存到: {saved_path}\n"
                                        f"共 {len(class_dirs)} 个类别，"
                                        f"{len(image_files)} 个图片文件")
                
                # 启用训练按钮
                self.train_btn.setEnabled(True)
                
                # 保存上传路径
                self.config['last_upload_path'] = str(folder_path)
                self.save_user_settings(None)
                
                # 更新预览
                self.preview_panel.load_images(folder_path)
                
            except Exception as e:
                self.status_label.setText(f"保存数据时出错: {str(e)}")
                self.train_btn.setEnabled(False)
    
    def start_training(self):
        try:
            # 禁用训练按钮，防止重复启动
            self.train_btn.setEnabled(False)
            self.upload_btn.setEnabled(False)
            self.status_label.setText("准备训练数据...")
            
            data_dir = self.path_manager.get_data_dir()
            
            # 创建数据集配置
            yaml_path = self.model_manager.create_dataset_yaml(data_dir)
            
            # 获取训练参数
            params = self.training_panel.get_training_params()
            
            # 开始训练
            self.status_label.setText("开始训练...")
            self.training_panel.progress_bar.setVisible(True)
            
            results = self.model_manager.train(
                yaml_path,
                epochs=params['epochs'],
                batch_size=params['batch_size']
            )
            
            self.status_label.setText("训练完成！")
            
        except Exception as e:
            self.status_label.setText(f"训练出错: {str(e)}")
        finally:
            # 恢复按钮状态
            self.train_btn.setEnabled(True)
            self.upload_btn.setEnabled(True)
            self.training_panel.progress_bar.setVisible(False)
    
    def toggle_help_panel(self):
        """显示帮助对话框"""
        help_dialog = HelpDialog(self)
        help_dialog.exec()
    
    def open_settings(self):
        """打开设置对话框"""
        settings_dialog = SettingsDialog(self)
        if settings_dialog.exec():
            # 如果用户点击了确定，则保存设置
            self.apply_settings(settings_dialog)
    
    def apply_settings(self, dialog):
        """应用设置"""
        # 应用字体大小
        font_size = dialog.font_size_spin.value()
        self.setFont(QFont("Arial", font_size))  # 设置字体
        
        # 应用窗口大小
        width = dialog.width_spin.value()
        height = dialog.height_spin.value()
        self.resize(width, height)

        # TODO: 保存其他设置到配置文件
        self.save_user_settings(dialog)