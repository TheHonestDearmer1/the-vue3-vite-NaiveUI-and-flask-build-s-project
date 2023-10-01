from flask import request, g, render_template, redirect, make_response, session

DataList = [] #将清单定义为全局变量方便返回
#总返回值
def TotalBanners():
    if 'username' not in session:
        return redirect('/admin/login')
    mod = request.cookies.get('mod')
    title_id = request.cookies.get('banners_id')
    return render_template('banners.html', banners=DefaultDanners(), mod=mod, title_id=title_id)


def Banners():
    # 进入页面时读取列表
    if request.method == 'GET':
        if not g.db.open:
            g.db.ping(reconnect=True)
        defaultDataList = []
        SREACHSQL = "SELECT * FROM banner_table"
        DBCONN = g.db.cursor()
        DBCONN.execute(SREACHSQL)
        results = DBCONN.fetchall()
        for i in results:
            defaultDataList.append({
                'ID': i[0],
                'title': i[1],
                'description': i[2],
                'href': i[3]
            })
        return {
            "status_code": 0,
            "status_msg": "读取成功",
            "DataList": defaultDataList
        }
    if request.method == 'POST':
        # 打开数据库
        if not g.db.open:
            g.db.ping(reconnect=True)
        title = request.json.get('title')
        description = request.json.get('description')
        href = request.json.get('href')
        DBCONN = g.db.cursor()
        print(title)
        print(description)
        print(href)
        if title== '' :
            return {
            "status_code": -1,
            "status_msg": "标题不能为空",
        }
        data = {
            'title': title,
            'description': description,
            'href': href
        }
        INSERTSQL = "INSERT INTO banner_table(title,description,href) values(%s,%s,%s)"
        DBCONN.execute(INSERTSQL, (data['title'], data['description'], data['href']))
        g.db.commit()
        SREACHTSQL = "SELECT * FROM banner_table"
        DBCONN.execute(SREACHTSQL)
        results = DBCONN.fetchall()
        DataList.clear()
        for i in results:
            DataList.append({
                'ID': i[0],
                'title': i[1],
                'description': i[2],
                'href': i[3],
            })
        return {
            "status_code": 0,
            "status_msg": "添加成功",
            "DataList": DataList
        }


#删除
def Delete_Banners():
   if not g.db.open:
      g.db.ping(reconnect=True)
   id = request.args.get('ID')  # 通过传递的参数名获取值
   print()
   SREACHTIDSQL = "DELETE FROM banner_table WHERE ID = %s"
   DBCONN = g.db.cursor()
   DBCONN.execute(SREACHTIDSQL,id)
   g.db.commit()
   DataList.clear()
   return {
            "status_code": 0,
            "status_Msg": "删除成功",
        }

#修改
def Change_Banners(id,mod):
   resp = make_response(redirect('/admin/banners'))
   resp.set_cookie('mod', mod)
   resp.set_cookie('banners_id', id)
   return resp

#激发小窗口修改的时候用的
def Change_Action_Banners():
    if request.method == 'POST':
        banners_id = request.json.get('ID')
        title = request.json.get('title')
        description = request.json.get('description')
        href = request.json.get('href')
        if not g.db.open:
            g.db.ping(reconnect=True)
        SetTitle = ''
        SetDescription = ''
        SetHref = ''
        params = []
        if title != '':
            params.append(title)
            SetTitle = "title = %s"
            if description != '' or href != '':
                SetTitle = "title = %s,"
        if description != '':
            params.append(description)
            SetDescription = "description = %s"
            if href != '':
                SetDescription = "description = %s,"
        if href != '':
            params.append(href)
            SetHref = "href = %s"
            # 参数都为空直接返回
        if title == '' and description == '' and href == '':
            return {
            "status_code": -1,
            "status_msg": "请至少输入一样参数"
        }
        SREACHTSQL = f"UPDATE banner_table SET {SetTitle} {SetDescription} {SetHref} WHERE ID = %s;"
        DBCONN = g.db.cursor()
        params.append(banners_id)
        DBCONN.execute(SREACHTSQL, params)
        g.db.commit()
        if DBCONN.rowcount == 0:
            # 处理ID不存在的情况，可以抛出异常或返回自定义错误信息
            return {
                "status_code": -1,
                "status_msg": f"不存在有该ID为{banners_id}的banner信息",
            }
        return {
            "status_code": 0,
            "status_msg": "修改成功",
        }
#从数据库读取
def DefaultDanners():
   if not g.db.open:
      g.db.ping(reconnect=True)
   defaultDataList = []
   SREACHSQL = "SELECT * FROM banner_table"
   DBCONN = g.db.cursor()
   DBCONN.execute(SREACHSQL)
   results = DBCONN.fetchall()
   for i in results:
      defaultDataList.append({
          'ID': i[0],
         'title': i[1],
         'description': i[2],
         'href': i[3]
         })
   return defaultDataList



