from flask import request, jsonify
from flask_restx import Resource
from services.skill_service import (
    list_all_skills, get_skill_by_id, get_skill_by_name, add_skill, update_skill, delete_skill
)
from utils.storage import save_portrait

class SkillListAll(Resource):
    def get(self):
        skills = list_all_skills()
        return skills

class SkillGetById(Resource):
    def get(self, cfgId):
        skill = get_skill_by_id(cfgId)
        return skill

class SkillGetByName(Resource):
    def get(self, name):
        skill = get_skill_by_name(name)
        return skill

class SkillAdd(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': '请求数据不能为空'}, 400
        
        result = add_skill(data)
        return result,200

class SkillUpdate(Resource):
    def put(self):
        data = request.get_json()
        if not data:
            return {'error': '请求数据不能为空'}, 400
        
        result = update_skill(data)
        return result,200

class SkillDelete(Resource):
    def delete(self):
        data = request.get_json()
        print(data)
        if not data or 'cfgId' not in data:
            return {'error': 'cfgId不能为空'}, 400
        result, status_code = delete_skill(data['cfgId'])
        return result, status_code

class SkillPortraitUpload(Resource):
    def post(self, cfgId):
        file = request.files.get('file')
        public_url, err = save_portrait('skill', cfgId, file)
        if err:
            return {'error': err}, 400
        # 同步更新技能JSON中的portrait
        skill = get_skill_by_id(cfgId)
        if skill:
            skill['portrait'] = public_url
            update_skill(skill)
        return {'portrait': public_url}, 200

def init_skill_api(api):
    api.add_resource(SkillListAll, '/skills/listall')
    api.add_resource(SkillGetById, '/skills/get_skill/<int:cfgId>')
    api.add_resource(SkillGetByName, '/skills/get_skill_by_name/<string:name>')
    api.add_resource(SkillAdd, '/skills/add_skill')
    api.add_resource(SkillUpdate, '/skills/update_skill')
    api.add_resource(SkillDelete, '/skills/del_skill')
    api.add_resource(SkillPortraitUpload, '/skills/upload_portrait/<int:cfgId>')
