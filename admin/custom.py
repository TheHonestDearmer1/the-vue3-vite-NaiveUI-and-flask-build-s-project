from flask import render_template, request, g, redirect, make_response
from werkzeug.utils import secure_filename
import json
URL_POST="http://localhost:5000/"

def Custom():
    #GET请求访问页面并将数据展示
    if request.method == "GET":
        if not g.db.open:
            g.db.ping(reconnect=True)
        defaultCustomList = []
        SREACHSQL = "SELECT * FROM custom_table"
        DBCONN = g.db.cursor()
        DBCONN.execute(SREACHSQL)
        results = DBCONN.fetchall()
        for i in results:
            defaultCustomList.append({
                'ID': i[0],
                'title': i[1],
                'description': i[2],
                'avatar': i[3]
            })
        return {
            "status_code": 0,
            "status_msg": "获取列表成功",
            "DataList" : defaultCustomList
        }
    #对页面发起POST请求增添custom数据操作，保存在数据库
    if request.method == "POST":
        if not g.db.open :
            g.db.ping(reconnect=True)
        DBCONN = g.db.cursor()
        title = request.json.get('title')
        description = request.json.get('description')
        if title == '' and description == '':
            return {
            "status_code": -1,
            "status_msg": "请至少输入一样参数",
        }
        SRC = "add"
        INSERTTABLE="INSERT INTO custom_table(title,description,src) values (%s,%s,%s)"
        DBCONN.execute(INSERTTABLE,(title,description,SRC))
        g.db.commit()
        INSREACHID = "select id from custom_table order by id desc limit 1"
        DBCONN.execute(INSREACHID)
        results = DBCONN.fetchall()
        return {
            "status_code": 0,
            "img_id" :results[0][0],
            "status_msg": "添加成功",
        }
    #图片上传
def AddCustomImg():
    if request.method == "POST":
        id = request.form['id']
        file = request.files['file']
        if not g.db.open:
            g.db.ping(reconnect=True)
        DBCONN = g.db.cursor()
        FileName = secure_filename(file.filename)
        file.save(f"static/{FileName}")
        SRC = URL_POST + "static/" + FileName
        INSERTTABLE = f"UPDATE custom_table SET src = %s WHERE id = %s;"
        DBCONN.execute(INSERTTABLE, (SRC,id))
        g.db.commit()
        return {
            "status_code": 0,
            "status_msg": "加入img成功",
        }




def Open_Change_Custom(title_id,title_mod):
    resp = make_response(redirect('/admin/custom'))
    resp.set_cookie('title_id',title_id)
    resp.set_cookie('title_mod',title_mod)
    return resp

#修改操作
def Change_Custom() :
    if request.method == "POST":
        if not g.db.open:
            g.db.ping(reconnect=True)
        DBCONN = g.db.cursor()
        title_id = request.json.get('id')
        title = request.json.get('title')
        description = request.json.get('description')
        SCID ="select id from custom_table where id = %s"
        DBCONN.execute(SCID, title_id)
        g.db.commit()
        if DBCONN.rowcount == 0:
            return {
            "status_code": -1,
            "status_msg": f"不存在有该ID为{title_id}的用户信息",
        }
        SetTitle = ''
        SetDescription = ''
        params = []
        if title != '':
            params.append(title)
            if description != '':
                SetTitle = "title = %s,"
            else:
                SetTitle = "title = %s"
        if description != '':
            params.append(description)
            SetDescription = "description = %s"
            #参数都为空直接返回
        if title == '' and description == '' :
            return {
            "status_code": 0,
            "status_msg": "修改成功",
        }
        INSERTTABLE = f"UPDATE custom_table SET {SetTitle} {SetDescription} WHERE id = %s;"
        # 更新数据
        params.append(title_id)
        DBCONN.execute(INSERTTABLE, params)
        g.db.commit()
        return  {
            "status_code": 0,
            "status_msg": "删除成功",
        }



def Delete_Custom():
    if not g.db.open:
        g.db.ping(reconnect=True)
    id = request.args.get('ID')  # 通过传递的参数名获取值
    SREACHTIDSQL = "DELETE FROM custom_table WHERE ID = %s"
    DBCONN = g.db.cursor()
    DBCONN.execute(SREACHTIDSQL, id)
    g.db.commit()
    return {
            "status_code": 0,
            "status_Msg": "删除成功",
        }