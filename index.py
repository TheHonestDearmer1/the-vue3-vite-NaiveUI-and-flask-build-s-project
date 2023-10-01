from flask import Flask,request,g,send_from_directory
import  pymysql
from admin.router import InitRouter
from admin.Table import InitTable
from flask_cors import CORS


app = Flask(__name__,static_url_path='/')
CORS(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
#静态文件夹访问
@app.route('/static/<filename>')
def StaticFile(filename):
    return send_from_directory('static',filename, mimetype='image')

#初始化扩展，传入app 创建db
# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='123456',
                     database='blog')


# 使用上下文处理器将变量绑定到请求上下文中
@app.before_request
def before_request():
    g.db = db

InitTable(db)
InitRouter(app)
db.close()
