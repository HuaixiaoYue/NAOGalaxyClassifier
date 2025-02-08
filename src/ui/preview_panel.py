from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                           QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QImage
from pathlib import Path
try:
    import cv2
except ImportError:
    print("警告：无法导入cv2，尝试安装 opencv-python")
    # 可以添加一些降级处理逻辑
import numpy as np

class PreviewPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # 标题
        title = QLabel("数据预览")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 创建滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # 创建网格容器
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        scroll.setWidget(self.grid_widget)
        
        # 设置缩略图大小
        self.thumbnail_size = QSize(100, 100)
        
        # 设置最小宽度
        self.setMinimumWidth(400)
        
        # 记录当前图片数量
        self.image_count = 0
    
    def clear_images(self):
        """清除所有图片"""
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        self.image_count = 0
    
    def add_image(self, image: np.ndarray, tooltip: str = ""):
        """
        添加单张图片
        
        Args:
            image: numpy数组格式的图片
            tooltip: 鼠标悬停时显示的文字
        """
        try:
            # 创建缩略图
            h, w = image.shape[:2]
            aspect = w / h
            if aspect > 1:
                new_w = self.thumbnail_size.width()
                new_h = int(new_w / aspect)
            else:
                new_h = self.thumbnail_size.height()
                new_w = int(new_h * aspect)
            
            img = cv2.resize(image, (new_w, new_h))
            
            # 转换为QPixmap
            height, width = img.shape[:2]
            bytes_per_line = 3 * width
            q_img = QImage(img.data, width, height, bytes_per_line,
                            QImage.Format.Format_RGB888)
            q_pixmap = QPixmap.fromImage(q_img)
            
            # 创建标签显示图片
            label = QLabel()
            label.setPixmap(q_pixmap)
            label.setToolTip(tooltip)
            
            # 添加到网格
            row = self.image_count // 4  # 每行4个图片
            col = self.image_count % 4
            self.grid_layout.addWidget(label, row, col)
            
            self.image_count += 1
            
        except Exception as e:
            print(f"无法加载图片: {e}")
    
    def load_images(self, folder_path: Path):
        """加载文件夹中的图片"""
        self.clear_images()
        
        # 获取所有图片文件
        image_files = list(folder_path.glob("*.jpg")) + list(folder_path.glob("*.png"))
        
        # 调试信息
        print(f"找到 {len(image_files)} 张图片")
        
        # 创建缩略图
        for img_path in image_files:
            try:
                # 读取图片
                img = cv2.imread(str(img_path))
                if img is None:
                    print(f"无法读取图片: {img_path}")
                    continue
                
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                self.add_image(img, img_path.name)
                
            except Exception as e:
                print(f"无法加载图片 {img_path}: {e}") 
    
    def show_inference_result(self, results):
        """显示推理结果"""
        self.clear_images()
        
        # 显示原始图片
        orig_img = results[0].orig_img
        self.add_image(orig_img, "原始图片")
        
        # 显示带预测结果的图片
        plot_img = results[0].plot()
        self.add_image(plot_img, "预测结果")
        
        # 添加类别概率
        probs = results[0].probs.top5
        names = results[0].names
        for i, prob in enumerate(probs):
            label = QLabel(f"{names[i]}: {prob:.2%}")
            self.grid_layout.addWidget(label, self.image_count // 4, self.image_count % 4)
            self.image_count += 1 