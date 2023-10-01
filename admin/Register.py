from flask import Flask, render_template, request, g, make_response, redirect, session
import jwt
import time

def Register():
    if not g.db.open:
        g.db.ping(reconnect=True)
    DBCONN = g.db.cursor()
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        repassword = request.json.get('repassword')
        print(username)
        print(password)
        print(repassword)
        if password != repassword :
            return {
                    "status_code": -1,
                    "status_msg": "两次输入的密码不相同请重新输入",
                    "user_id": 0,
                    "token": ''
            }
        CheckSql = "SELECT * FROM user where username = %s"
        DBCONN.execute(CheckSql,username)
        results = DBCONN.fetchall() #得到结果
        if len(results) != 0 :
            return {
            "status_code": -1,
            "status_msg": "已经存在用户，请返回重新登录",
            "user_id": 0,
            "token": ''
        }
    if username != None and password != None:
        # 生成一个字典，包含我们的具体信息
        d = {
            # 公共声明
            'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
            # 私有声明
            'data': {
                'username': username,
                'password': password
            }
        }
        token = jwt.encode(d, username, algorithm='HS256')
        RegisterSql ="INSERT INTO user( username, password) VALUES (%s, %s)"
            # 执行sql语句
        DBCONN.execute(RegisterSql,(username, token))
            # 提交事务，否则数据库中不会出现数据
        g.db.commit()
            # 存入session
        session['username'] = username
        session['password'] = token
        return {
            "status_code": 0,
            "status_msg": "注册成功",
            "user_id": 0,
            "token": token
        }
    else:
        return {
            "status_code": -1,
            "status_msg": "注册失败",
            "user_id": 0,
            "token": ''
        }
