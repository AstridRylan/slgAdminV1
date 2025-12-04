from flask import request, jsonify
from flask_restx import Resource
from services.general_service import (
    list_all_generals, get_general_by_id, get_generals_by_name,
    add_general, update_general, delete_general
)
from utils.storage import save_portrait

class GeneralListAll(Resource):
    def get(self):
        generals = list_all_generals()
        return generals,200

class GeneralGetById(Resource):
    def get(self, cfgId):
        general = get_general_by_id(cfgId)
        return general,200 

class GeneralGetByName(Resource):
    def get(self, name):
        generals = get_generals_by_name(name)
        return generals,200 

class GeneralAdd(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return {'error': '请求数据不能为空'}, 400
        
        result, status_code = add_general(data)
        if isinstance(result, dict) and 'error' in result:
            return result, status_code
        return result, status_code

class GeneralUpdate(Resource):
    def put(self):
        data = request.get_json()
        if not data:
            return {'error': '请求数据不能为空'}, 400
        
        result, status_code = update_general(data)
        if isinstance(result, dict) and 'error' in result:
            return result, status_code
        return result, status_code

class GeneralDelete(Resource):
    def delete(self):
        data = request.get_json()
        if not data or 'cfgId' not in data:
            return {'error': 'cfgId不能为空'}, 400
        
        result, status_code = delete_general(data['cfgId'])
        return result, status_code

class GeneralPortraitUpload(Resource):
    def post(self, cfgId):
        # 使用 form-data: file
        file = request.files.get('file')
        public_url, err = save_portrait('general', cfgId, file)
        if err:
            return {'error': err}, 400
        # 更新该武将的portrait字段（如存在该武将）
        general = get_general_by_id(cfgId)
        if general:
            general['portrait'] = public_url
            update_general(general)
        # 返回前端可直接使用的URL
        return {'portrait': public_url}, 200

def init_general_api(api):
    api.add_resource(GeneralListAll, '/generals/listall')
    api.add_resource(GeneralGetById, '/generals/get_general/<int:cfgId>')
    api.add_resource(GeneralGetByName, '/generals/get_general_by_name/<string:name>')
    api.add_resource(GeneralAdd, '/generals/add_general')
    api.add_resource(GeneralUpdate, '/generals/update_general')
    api.add_resource(GeneralDelete, '/generals/del_general')
    api.add_resource(GeneralPortraitUpload, '/generals/upload_portrait/<int:cfgId>')
