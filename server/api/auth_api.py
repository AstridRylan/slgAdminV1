from flask import request
from flask_restx import Resource

DEFAULT_USERS = {
    'jenuos': {
        'password': '123',
        'avatarUrl': '/resources/skin/skill/default_bingren.png'
    },
    'caocao': {
        'password': '123',
        'avatarUrl': '/resources/skin/skill/default_moulue.png'
    },
    'weini': {
        'password': '123',
        'avatarUrl': '/resources/skin/skill/default_zengyi.png'
    }
}

USERS = DEFAULT_USERS.copy()

class Login(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')
        user = USERS.get(username)
        if not user or user.get('password') != str(password):
            return {'error': '用户名或密码错误'}, 401
        token = f"mock-token-{username}"
        return {
            'token': token,
            'username': username,
            'avatarUrl': user.get('avatarUrl')
        }, 200

class Register(Resource):
    def post(self):
        data = request.get_json() or {}
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return {'error': '用户名和密码不能为空'}, 400
        if username in USERS:
            return {'error': '用户名已存在'}, 400
        USERS[username] = {
            'password': str(password),
            'avatarUrl': '/resources/skin/skill/default_jianyi.png'
        }
        return {'message': '注册成功'}, 201

class Me(Resource):
    def get(self):
        auth = request.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            token = auth.replace('Bearer ', '')
            if token.startswith('mock-token-'):
                username = token[len('mock-token-'):]
                user = USERS.get(username)
                if user:
                    return {
                        'username': username,
                        'avatarUrl': user.get('avatarUrl')
                    }, 200
        return {'error': '未认证'}, 401

def init_auth_api(api):
    api.add_resource(Login, '/auth/login')
    api.add_resource(Register, '/auth/register')
    api.add_resource(Me, '/auth/me')

