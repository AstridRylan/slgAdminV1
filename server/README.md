# SLG游戏管理后台 - 后端API服务

## 项目概述

这是一个基于Flask框架的RESTful API服务，为SLG游戏管理后台提供武将和战法数据的管理功能。采用分层架构设计，实现了数据访问、业务逻辑和API接口的分离。

## 技术栈

- **框架**: Flask + Flask-RESTful
- **跨域支持**: Flask-CORS
- **数据存储**: JSON文件存储
- **Python版本**: Python 3.6+

## 项目结构

```
server/
├── api/                    # API接口层
│   ├── __init__.py
│   ├── general_api.py       # 武将相关API
│   └── skill_api.py        # 战法相关API
├── models/                 # 数据模型层
│   ├── __init__.py
│   ├── general_model.py    # 武将数据操作
│   └── skill_model.py      # 战法数据操作
├── services/               # 业务逻辑层
│   ├── __init__.py
│   ├── general_service.py  # 武将业务逻辑
│   └── skill_service.py    # 战法业务逻辑
├── data/                   # 数据存储目录
│   └── conf/
│       └── json/
│           ├── general/    # 武将数据文件
│           │   └── general.json
│           └── skill/      # 战法数据文件
│               └── *.json
├── resources/              # 静态资源目录
│   └── skin/               # 皮肤资源文件
├── run.py                  # 应用入口文件
├── requirements.txt        # 项目依赖
└── README.md              # 项目文档
```

## 架构设计

### 分层架构

1. **API层** (`api/`): 处理HTTP请求和响应，定义路由和参数验证
2. **Service层** (`services/`): 封装业务逻辑，处理业务规则和流程
3. **Model层** (`models/`): 封装数据访问操作，负责JSON文件的读写

### 数据存储设计

- **武将数据**: 存储在 `data/conf/json/general/general.json` 中，采用列表结构
- **战法数据**: 每个战法单独存储为 `data/conf/json/skill/{skill_id}.json` 文件
- **ID分配规则**: 
  - 武将cfgId从100001开始自动递增
  - 战法id从200001开始自动递增

## API接口文档

### 武将相关接口

#### 1. 获取所有武将
- **接口**: `GET /api/generals/listall`
- **描述**: 获取所有武将数据列表
- **返回**: 武将列表数组

#### 2. 根据ID获取武将
- **接口**: `GET /api/generals/get_general/<int:general_id>`
- **描述**: 根据武将ID获取单个武将数据
- **返回**: 包含武将数据的数组（最多一个元素）

#### 3. 根据名称获取武将
- **接口**: `GET /api/generals/get_general_by_name/<string:general_name>`
- **描述**: 根据武将名称模糊匹配获取武将数据
- **返回**: 匹配的武将列表数组

#### 4. 添加武将
- **接口**: `POST /api/generals/add_general`
- **描述**: 添加新武将
- **请求体**: 武将JSON数据（不含cfgId）
- **返回**: 添加成功的武将数据或错误信息
- **注意**: 如果武将名称已存在，返回添加失败

#### 5. 更新武将
- **接口**: `PUT /api/generals/update_general`
- **描述**: 更新现有武将数据
- **请求体**: 完整的武将JSON数据（含cfgId）
- **返回**: 更新后的武将数据或错误信息

#### 6. 删除武将
- **接口**: `DELETE /api/generals/del_general`
- **描述**: 删除指定武将
- **请求体**: `{"cfgID": <武将ID>}`
- **返回**: 删除成功消息或错误信息

### 战法相关接口

#### 1. 获取所有战法
- **接口**: `GET /api/skills/listall`
- **描述**: 获取所有战法数据列表
- **返回**: 战法列表数组

#### 2. 根据ID获取战法
- **接口**: `GET /api/skills/get_skill/<int:skill_id>`
- **描述**: 根据战法ID获取单个战法数据
- **返回**: 战法JSON数据

#### 3. 添加战法
- **接口**: `POST /api/skills/add_skill`
- **描述**: 添加新战法
- **请求体**: 战法JSON数据（不含id）
- **返回**: 添加成功的战法数据

#### 4. 更新战法
- **接口**: `PUT /api/skills/update_skill`
- **描述**: 更新现有战法数据
- **请求体**: 完整的战法JSON数据（含id）
- **返回**: 更新后的战法数据

#### 5. 删除战法
- **接口**: `DELETE /api/skills/del_skill`
- **描述**: 删除指定战法
- **请求体**: `{"id": <战法ID>}`
- **返回**: 删除成功消息或错误信息

### 静态资源接口

#### 获取皮肤资源
- **接口**: `GET /resources/skin/<path:path>`
- **描述**: 获取皮肤图片等静态资源
- **返回**: 静态文件

## 配置说明

### 环境要求

- Python 3.6+
- Flask 2.0+
- Flask-RESTful 0.3.9+
- Flask-CORS 3.0+

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动服务

```bash
python run.py
```

服务启动后，API将在 `http://127.0.0.1:5000` 上提供访问。

## 使用示例

### 添加武将示例

```bash
curl -X POST http://127.0.0.1:5000/api/generals/add_general \
  -H "Content-Type: application/json" \
  -d '{
    "name": "关羽",
    "attack": 95,
    "defense": 85,
    "intelligence": 75
  }'
```

### 获取所有武将示例

```bash
curl http://127.0.0.1:5000/api/generals/listall
```

### 更新武将示例

```bash
curl -X PUT http://127.0.0.1:5000/api/generals/update_general \
  -H "Content-Type: application/json" \
  -d '{
    "cfgID": 100001,
    "name": "关羽",
    "attack": 98,
    "defense": 88,
    "intelligence": 78
  }'
```

## 注意事项

1. **数据持久化**: 所有数据存储在JSON文件中，请确保有适当的文件权限
2. **ID管理**: 系统自动管理ID分配，不要手动指定ID
3. **名称唯一性**: 武将名称必须唯一，重复名称会导致添加失败
4. **跨域支持**: 默认开启CORS，支持前端跨域访问
5. **错误处理**: API会返回适当的HTTP状态码和错误信息

## 开发建议

1. **数据备份**: 定期备份 `data/` 目录下的JSON文件
2. **扩展性**: 如需添加新功能，建议遵循现有的三层架构
3. **测试**: 建议使用Postman或类似工具测试API接口
4. **日志**: 生产环境建议添加日志记录功能

## 版本历史

- v1.0.0: 初始版本，实现基本的武将和战法CRUD功能
- v1.1.0: 重构API端点，优化架构分层，完善错误处理