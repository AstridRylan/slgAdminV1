from models.general_model import GeneralModel

general_model = GeneralModel()

def list_all_generals():
    return general_model.get_all_generals()


def get_general_by_id(cfgId):
    general = general_model.get_general_by_id(cfgId)
    return general

def get_generals_by_name(name):
    return general_model.get_generals_by_name(name)

def add_general(general_data):
    if general_model.check_general_exists_by_name(general_data.get('name')):
        return {'error': '添加失败，武将已经存在'}, 400
    
    general_data['cfgId'] = general_model.get_next_cfg_id()
    return general_model.add_general(general_data), 201

def update_general(general_data):
    if general_model.update_general(general_data):
        return general_data,200
    return {'error': '武将不存在'}, 404

def delete_general(general_id):
    if general_model.delete_general(general_id):
        return {'message': '删除成功'}, 200
    return {'error': '武将不存在'}, 404