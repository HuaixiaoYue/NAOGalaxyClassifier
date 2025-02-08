from pathlib import Path
import shutil
import random

class PathManager:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent
        
    def get_model_dir(self) -> Path:
        model_dir = self.root_dir / 'models'
        model_dir.mkdir(exist_ok=True)
        return model_dir
    
    def get_data_dir(self) -> Path:
        data_dir = self.root_dir / 'data' / 'raw'
        data_dir.mkdir(parents=True, exist_ok=True)
        return data_dir
    
    def get_processed_dir(self) -> Path:
        processed_dir = self.root_dir / 'data' / 'processed'
        processed_dir.mkdir(parents=True, exist_ok=True)
        return processed_dir
    
    def save_training_data(self, folder_path: str | Path) -> Path:
        """
        保存训练数据文件夹到数据目录
        
        Args:
            folder_path: 源训练数据文件夹路径
            
        Returns:
            保存后的目标文件夹路径
        """
        folder_path = Path(folder_path)
        dest_dir = self.get_data_dir() / folder_path.name
        
        # 如果目标文件夹已存在，先删除
        if dest_dir.exists():
            shutil.rmtree(dest_dir)
        
        # 复制整个文件夹
        shutil.copytree(folder_path, dest_dir)
        
        return dest_dir
    
    def split_dataset(self, source_dir: Path, split_ratios: tuple = (0.7, 0.2, 0.1)):
        """
        自动划分数据集到 train/valid/test 目录
        Args:
            source_dir: 原始数据目录
            split_ratios: (训练集比例, 验证集比例, 测试集比例)
        """
        # 确保比例总和为1
        assert sum(split_ratios) == 1.0, "划分比例总和必须为1"
        
        # 目标目录
        data_dir = self.get_data_dir()
        train_dir = data_dir / 'train' / 'images'
        valid_dir = data_dir / 'valid' / 'images'
        test_dir = data_dir / 'test' / 'images'
        
        # 清空现有数据
        shutil.rmtree(data_dir, ignore_errors=True)
        train_dir.mkdir(parents=True, exist_ok=True)
        valid_dir.mkdir(parents=True, exist_ok=True)
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # 遍历每个类别
        for class_dir in source_dir.iterdir():
            if class_dir.is_dir():
                # 获取所有图片文件
                images = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png"))
                random.shuffle(images)
                
                # 计算划分点
                total = len(images)
                train_end = int(total * split_ratios[0])
                valid_end = train_end + int(total * split_ratios[1])
                
                # 复制文件
                for img in images[:train_end]:
                    dest = train_dir / class_dir.name / img.name
                    dest.parent.mkdir(exist_ok=True)
                    shutil.copy(img, dest)
                
                for img in images[train_end:valid_end]:
                    dest = valid_dir / class_dir.name / img.name
                    dest.parent.mkdir(exist_ok=True)
                    shutil.copy(img, dest)
                
                for img in images[valid_end:]:
                    dest = test_dir / class_dir.name / img.name
                    dest.parent.mkdir(exist_ok=True)
                    shutil.copy(img, dest)