from flask import request
from flask_restx import Resource
from services.battle_service import simulate_battle

class BattleSimulate(Resource):
    def post(self):
        payload = request.get_json() or {}
        result = simulate_battle(payload)
        return result, 200

def init_battle_api(api):
    api.add_resource(BattleSimulate, '/battle/simulate')

