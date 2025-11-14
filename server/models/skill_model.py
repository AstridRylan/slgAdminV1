import json
import os
from dotenv import load_dotenv

load_dotenv()
SKILL_DATA_DIR = os.getenv('SKILL_DATA_DIR') or 'data/conf/json/skill'

class SkillModel:
    def __init__(self):
        self.data_dir = SKILL_DATA_DIR
        self._ensure_data_dir_exists()
    
    def _ensure_data_dir_exists(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)
    
    def get_all_skills(self):
        skills = []
        if not os.path.exists(self.data_dir):
            return skills
        filenames = sorted(os.listdir(self.data_dir))
        for filename in filenames:
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        skills.append(json.load(f))
                except (json.JSONDecodeError, IOError):
                    continue
        return skills
    
    def get_skill_by_id(self, skill_id):
        filepath = os.path.join(self.data_dir, f'{skill_id}.json')
        if not os.path.exists(filepath):
            return None
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def get_skill_by_name(self, skill_name):
        skills = self.get_all_skills()
        for skill in skills:
            if skill.get('name') == skill_name:
                return skill
        return None

    def check_skill_exists_by_id(self, skill_id):
        filepath = os.path.join(self.data_dir, f'{skill_id}.json')
        return os.path.exists(filepath)
    
    def get_next_cfg_id(self):
        skills = self.get_all_skills()
        if not skills:
            return 200001
        max_id = max(s.get('cfgId', 200000) for s in skills)
        return max_id + 1 if max_id >= 200001 else 200001
    
    def create_skill(self, skill_data):
        skill_id = skill_data.get('cfgId')
        if not skill_id:
            return None
        filepath = os.path.join(self.data_dir, f'{skill_id}.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(skill_data, f, ensure_ascii=False, indent=4)
        return skill_data
    
    def update_skill(self, skill_data):
        return self.create_skill(skill_data)
    
    def delete_skill(self, skill_id):
        filepath = os.path.join(self.data_dir, f'{skill_id}.json')
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False