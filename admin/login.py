from flask import request, render_template, g, redirect, url_for
from flask import session
import jwt
import time


def Login():
    if request.method == 'GET':  # 登录页面
        return render_template('login.html')
    # 传递登录数据
    if request.method == 'POST':
        if not g.db.open:
            g.db.ping(reconnect=True)
        DBCONN = g.db.cursor()
        username = request.json.get('username')
        password = request.json.get('password')
        CheckUSER = "SELECT password FROM user WHERE username = %s limit 1"
        DBCONN.execute(CheckUSER, username)
        res = DBCONN.fetchall()
        if len(res) == 0:
            return {
                "status_code": -1,
                "status_msg": "不存在该用户，请重新输入",
                "user_id": 0,
                "token": ''
            }
        jwt_decode = jwt.decode(res[0][0],username, algorithms=['HS256'])
        if password == jwt_decode['data']['password']:
            # 存入session
            session['username'] = username
            session['password'] = res[0][0]
            return {
                "status_code": 0,
                "status_msg": "登录成功",
                "user_id": 0,
                "token": res[0][0]
            }
        else:
            return {
                "status_code": 0,
                "status_msg": "登录失败,密码错误",
                "user_id": 0,
                "token": ''
            }


def OutLogin():
    session.pop('username', None)
    session.pop('password', None)
    return redirect('/admin')
