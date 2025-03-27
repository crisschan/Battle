#!/usr/bin/env python
# -*- coding: utf-8 -*-

#__from__ = 'Battle'
#__title__='PyCharm'
#__author__ = 'chancriss'
#__mtime__ = '2018/01/01'
#__instruction__=''

from doctest import BLANKLINE_MARKER
from gettext import install
from bottle import Bottle, run,get,post,request,static_file,redirect
from bottle import Bottle, run, get, post, request, static_file, redirect
from beaker.middleware import SessionMiddleware
import json

import pip
from SQLiteHelper import SQLiteHelper
app = Bottle()
msUsername = ''
msEquipmentid=''
session_opts = {
   'session.type':'file',              #以文件的方式保存session
   'session.cookie_expires':300,       #session过期时间为300秒
   'session.data_dir':'/tmp/sessions_dir', #session保存目录
   'session.auto':True               #自动保存session
    }

#
# 
# 
# #

@app.get('/')
@app.get('/index')
def index():
    return json.dumps({
        'code': 0,
        'message': 'Success',
        'data': {
            'instruction': 'Please input your username(your english name) and password(your english name)'
        }
    })

@app.post('/login')
def login():
    try:
        data = request.json
        msUsername = data.get('username')
        sPassword = data.get('password')

        # 使用 SQLiteHelper 连接到数据库
        db_helper = SQLiteHelper('bat.db')

        # 查询用户信息
        sql = f"SELECT * FROM user WHERE username='{msUsername}' AND password='{sPassword}'"
        user = db_helper.select_one(sql)

        # 查询装备信息
        equipment_data = db_helper.select_more("SELECT * FROM equipment")
        equipment_options = {str(row['id']): row['name'] for row in equipment_data}

        if user:
            ssSession = request.environ.get('beaker.session')
            ssSession['user'] = msUsername
            ssSession.save()

            return json.dumps({
                'code': 0,
                'message': 'Success',
                'data': {
                    'equipment_options': equipment_options  # 从数据库获取装备信息
                }
            })
        else:
            return json.dumps({
                'code': 9901,
                'message': 'Username or Password Error',
                'data': None
            })
    except:
        return json.dumps({
            'code': 9906,
            'message': 'Invalid JSON Input',
            'data': None
        })

@app.post('/select')
def selectEq():
    try:
        data = request.json
        msEquipmentid = data.get('equipmentid')
        ssSession = request.environ.get('beaker.session')
        
        # 获取会话中存储的用户名
        stored_username = ssSession.get('user', None)

        # 使用 SQLiteHelper 连接到数据库
        db_helper = SQLiteHelper('bat.db')

        # 查询敌人信息
        enemy_data = db_helper.select_more("SELECT * FROM enemy")
        enemy_options = {str(row['id']): row['name'] for row in enemy_data}
        
        if msEquipmentid is not None and str(msEquipmentid).isdigit():
            ssSession['equipmentid'] = msEquipmentid
            ssSession.save()
            return json.dumps({
                'code': 0,
                'message': 'Success',
                'data': {
                    'equipmentid': msEquipmentid,
                    'enemy_options': enemy_options
                }
            })
        else:
            return json.dumps({
                'code': 9902,
                'message': 'Invalid Equipment Selection',
                'data': None
            })
    except:
        return json.dumps({
            'code': 9906,
            'message': 'Invalid JSON Input',
            'data': None
        })

@app.post('/kill')
def kill():
    try:
        data = request.json
        sEnemyid = data.get('enemyid')
        msEquipmentid = data.get('equipmentid')
        
        if sEnemyid is None:
            return json.dumps({
                'code': 9904,
                'message': 'Enemy ID is required',
                'data': None
            })
        
        if msEquipmentid is None:
            return json.dumps({
                'code': 9905,
                'message': 'Equipment ID is required',
                'data': None
            })
        
        if msEquipmentid in ['10001', '10002', '10003']:
            if sEnemyid in ['20001', '20002', '20003']:
                battle_result = int(msEquipmentid) - int(sEnemyid) + 10000
                
                if battle_result > 0:
                    result = {'status': 'win', 'level': 1}
                elif battle_result == 0:
                    result = {'status': 'draw', 'message': 'Both dead'}
                else:
                    result = {'status': 'lose', 'message': 'You died'}
                    
                return json.dumps({
                    'code': 0,
                    'message': 'Success',
                    'data': result
                })
            else:
                return json.dumps({
                    'code': 9902,
                    'message': 'Invalid Enemy ID',
                    'data': None
                })
        else:
            return json.dumps({
                'code': 9903,
                'message': 'Invalid Equipment ID',
                'data': None
            })
    except:
        return json.dumps({
            'code': 9906,
            'message': 'Invalid JSON Input',
            'data': None
        })

app = SessionMiddleware(app, session_opts)

if __name__ == '__main__':
    run(app=app, port=12356)
