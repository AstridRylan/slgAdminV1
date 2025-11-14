from models.skill_model import SkillModel

skill_model = SkillModel()

def list_all_skills():
    return skill_model.get_all_skills()

def get_skill_by_id(skill_id):
    return skill_model.get_skill_by_id(skill_id)

def get_skill_by_name(skill_name):
    return skill_model.get_skill_by_name(skill_name)

def add_skill(skill_data):
    skill_data['cfgId'] = skill_model.get_next_cfg_id()
    return skill_model.create_skill(skill_data)

def update_skill(skill_data):
    return skill_model.update_skill(skill_data)

def delete_skill(skill_id):
    if skill_model.delete_skill(skill_id):
        return {'message': '删除成功'}, 200
    return {'error': '战法不存在'}, 404