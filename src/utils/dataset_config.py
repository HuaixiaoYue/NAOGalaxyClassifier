from pathlib import Path
import yaml
from typing import List, Dict

class DatasetConfig:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.config_path = project_path / 'data.yaml'
        self.default_config = {
            'train': './train/images',
            'val': './valid/images',
            'test': './test/images',
            'nc': 0,
            'names': []
        }
    
    def create_directory_structure(self):
        """创建数据集目录结构"""
        (self.project_path / 'train' / 'images').mkdir(parents=True, exist_ok=True)
        (self.project_path / 'valid' / 'images').mkdir(parents=True, exist_ok=True)
        (self.project_path / 'test' / 'images').mkdir(parents=True, exist_ok=True)
    
    def save_config(self, config: Dict):
        """保存数据集配置"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(config, f, allow_unicode=True)
    
    def load_config(self) -> Dict:
        """加载数据集配置"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self.default_config.copy()
    
    def update_class_info(self, class_names: List[str]):
        """更新类别信息"""
        config = self.load_config()
        config['nc'] = len(class_names)
        config['names'] = class_names
        self.save_config(config) 