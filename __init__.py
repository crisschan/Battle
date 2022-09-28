#!/usr/bin/env python
# -*- coding: utf-8 -*-

#__from__ = 'Battle'
#__title__='PyCharm'
#__author__ = 'chancriss'
#__mtime__ = '2018/01/01'
#__instruction__=''

from bottle import Bottle, run,get,post,request,static_file,redirect
from beaker.middleware import SessionMiddleware
import json
app = Bottle()
msUsername = ''
msEquipmentid=''
session_opts = {
   'session.type':'file',              #以文件的方式保存session
   'session.cookei_expires':300,       #session过期时间为300秒
   'session.data_dir':'/tmp/sessions_dir', #session保存目录
   'session.auto':True               #自动保存session
    }

@app.get('/')
@app.get('/index')
def index():
    return 'please input your username(your english name) and password(your english name)'

@app.post('/login')
def login():

    msUsername = request.POST.get('username')

    sPassword = request.POST.get('password')
    if msUsername==sPassword:
        ssSession = request.environ.get('beaker.session')

        ssSession['user'] = msUsername
        ssSession.save


        return 'please select One Equipment:\n10001:Knife\n10002:Big Sword\n10003:KuiHuaBaoDian'
    else:
        return 'Error 9901: Username or PassWord!!'
@app.post('/selectEq')
def selectEq():

    msEquipmentid = request.POST.get('equipmentid')
    ssSession = request.environ.get('beaker.session')
    #print 'msEquipmentid:'+msEquipmentid
    #print 'ssSession:'+ssSession
    if msEquipmentid is not None:
        if str(msEquipmentid).isdigit():
            ssSession['equipmentid']=msEquipmentid
            ssSession.save
            return {'equipmentid':msEquipmentid,'Message':'your pick up equipmentid:'+msEquipmentid+' please select your  enemyid:\n20001:Terran\n20002:ORC\n20003:Undead'}
    else:
        return {'equipmentid':'-1','Message':'Error 9902: Your kill yourself!!'}


@app.post('/kill')
def kill():
    sEnemyid = request.POST.get('enemyid')
    #print 'sEnemyid'+sEnemyid
    msEquipmentid = request.POST.get('equipmentid')
    coockies = request.get_cookie("account", secret='some-secret-key')
    #print sEnemyid
    #print msEquipmentid
    if sEnemyid is None:
        return 'Error 9904: Your kill yourself!!'
    if msEquipmentid is None:
        return 'Error 9905: Your fight your enemy by nothing!And you are  died!'
    if msEquipmentid in ['10001','10002','10003']:
        if sEnemyid in ['20001','20002','20003']:

            if (int(msEquipmentid)-int(sEnemyid)+10000)>0:
                return 'You are win Level 1!'
            elif (int(msEquipmentid)-int(sEnemyid)+10000)==0:
                return 'Your and your enemy all dead!!!'
            else:
                return 'Your dead!'
        else:
            return 'Error 9902: Your kill yourself!!'
    else:
        return 'Error 9903: You Broken The Rule!And Kill yourself'


app = SessionMiddleware(app, session_opts)

if __name__ == '__main__':
    run(app=app, port=12356)
