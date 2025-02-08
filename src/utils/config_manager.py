import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.parent
        self.config_file = self.root_dir / 'config' / 'user_settings.json'
        self.default_config = {
            'last_upload_path': str(Path.home()),  # 上次上传文件的路径
            'training_params': {
                'batch_size': 16,
                'learning_rate': 0.001,
                'epochs': 100
            }
        }
        self._ensure_config_file()
    
    def _ensure_config_file(self):
        """确保配置文件存在"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.config_file.exists():
            self.save_config(self.default_config)
    
    def load_config(self) -> Dict[str, Any]:
        """加载配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return self.default_config
    
    def save_config(self, config: Dict[str, Any]):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}") 