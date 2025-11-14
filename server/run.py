from flask import Flask, send_from_directory
from flask_restx import Api
from flask_cors import CORS

from api.general_api import init_general_api
from api.skill_api import init_skill_api
from api.auth_api import init_auth_api
from api.battle_api import init_battle_api

app = Flask(__name__)
CORS(app)
api = Api(
    app,
    prefix="/api",
    title='General & Skill API',
    description='A simple example API',
    doc='/apidocs'
)

# 初始化API路由
init_general_api(api)
init_skill_api(api)
init_auth_api(api)
init_battle_api(api)

# Static resource endpoint
@app.route('/resources/skin/<path:path>')
def send_resource(path):
    return send_from_directory('resources/skin', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5050)
