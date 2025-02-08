from pathlib import Path
import torch
from ultralytics import YOLO
from typing import Callable, Dict, Any

class YOLOTrainer:
    def __init__(self):
        self.model = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    def init_model(self, model_size: str, pretrained: bool = True):
        """初始化YOLO模型"""
        try:
            model_name = f"yolo11{model_size}-cls"  # 修改为yolo11格式
            if pretrained:
                # 加载预训练模型
                self.model = YOLO(f"{model_name}.pt")
            else:
                # 从YAML构建新模型
                self.model = YOLO(f"{model_name}.yaml")
            return True
        except Exception as e:
            print(f"模型初始化失败: {str(e)}")
            return False
    
    def train(self, 
             data_path: Path,
             params: Dict[str, Any],
             progress_callback: Callable[[int, str], None] = None):
        """
        训练模型
        
        Args:
            data_path: 数据集路径
            params: 训练参数字典
            progress_callback: 进度回调函数，接收进度值(0-100)和状态信息
        """
        try:
            # 确保使用正确的 data.yaml 路径
            data_yaml = data_path / 'data.yaml'
            if not data_yaml.exists():
                raise FileNotFoundError(f"找不到数据集配置文件: {data_yaml}")
            
            if self.model is None:
                raise RuntimeError("模型未初始化")
            
            # 准备训练参数（简化为与YOLO11一致的参数）
            train_args = {
                'data': str(data_yaml),  # 使用完整的 data.yaml 路径
                'imgsz': params['img_size'],
                'batch': params['batch_size'],
                'epochs': params['epochs'],
                'device': self.device
            }
            
            # 注册回调函数来更新进度
            def on_train_epoch_end(trainer):
                progress = int((trainer.epoch + 1) / params['epochs'] * 100)
                if progress_callback:
                    progress_callback(progress, f"训练轮次 {trainer.epoch + 1}/{params['epochs']}")
            
            # 开始训练
            if progress_callback:
                progress_callback(0, "开始训练...")
            
            # 使用YOLO11的训练方式
            results = self.model.train(**train_args)
            
            if progress_callback:
                progress_callback(100, "训练完成")
            
            return True
            
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"训练失败: {str(e)}")
            return False 