import json
import os
from dotenv import load_dotenv

load_dotenv()
GENERAL_DATA_PATH = os.getenv('GENERAL_DATA_PATH') or 'data/conf/json/general/general.json'

class GeneralModel:
    def __init__(self):
        self.data_path = GENERAL_DATA_PATH
        self._ensure_data_file_exists()
    
    def _ensure_data_file_exists(self):
        if not os.path.exists(self.data_path):
            os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump({'title': '武将配置', 'list': []}, f, ensure_ascii=False, indent=4)
    
    def get_all_generals(self):
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('list', [])
    
    def get_general_by_id(self, cfgId):
        generals = self.get_all_generals()
        for general in generals:
            if general.get('cfgId') == cfgId:
                return general
        return None
    
    def get_generals_by_name(self, general_name):
        generals = self.get_all_generals()
        return [g for g in generals if g.get('name') == general_name]
    
    def check_general_exists_by_name(self, general_name):
        generals = self.get_all_generals()
        return any(g.get('name') == general_name for g in generals)
    
    def get_next_cfg_id(self):
        generals = self.get_all_generals()
        if not generals:
            return 100001
        max_id = max(g.get('cfgId', 100000) for g in generals)
        return max_id + 1 if max_id >= 100001 else 100001
    
    def add_general(self, general_data):
        generals = self.get_all_generals()
        generals.append(general_data)
        self._save_generals(generals)
        return general_data
    
    def update_general(self, general_data):
        generals = self.get_all_generals()
        general_id = general_data.get('cfgId')
        for i, general in enumerate(generals):
            if general.get('cfgId') == general_id:
                generals[i] = general_data
                self._save_generals(generals)
                return True
        return False
    
    def delete_general(self, general_id):
        generals = self.get_all_generals()
        original_count = len(generals)
        generals = [g for g in generals if g.get('cfgId') != general_id]
        if len(generals) < original_count:
            self._save_generals(generals)
            return True
        return False
    
    def _save_generals(self, generals):
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump({'title': '武将配置', 'list': generals}, f, ensure_ascii=False, indent=4)