from flask import render_template, request, redirect, make_response, g, session


def AdminIndex():
    if 'username' in session and 'password' in session:
        username = session['username']
        password = session['password']
        if not g.db.open:
            g.db.ping(reconnect=True)
        CheckSql = "SELECT * FROM user WHERE username = %s and password = %s"
        DBCONN = g.db.cursor()
        DBCONN.execute(CheckSql, (username, password))
        results = DBCONN.fetchall()
        #数据库中不存在则删除
        if len(results) == 0:
            session.pop('username', None)
            session.pop('password', None)
            print(len(results))
            resp = make_response(render_template('index.html', username=None))
            resp.delete_cookie('banners_id')
            resp.delete_cookie('mod')
            resp.delete_cookie('title_id')
            resp.delete_cookie('title_mod')
            return resp
        resp = make_response(render_template('index.html', username=username))
        resp.delete_cookie('banners_id')
        resp.delete_cookie('mod')
        resp.delete_cookie('title_id')
        resp.delete_cookie('title_mod')
        print(username)
        return resp
        #正常返回
    resp = make_response(render_template('index.html', username=None))
    resp.delete_cookie('banners_id')
    resp.delete_cookie('mod')
    resp.delete_cookie('title_id')
    resp.delete_cookie('title_mod')
    return resp