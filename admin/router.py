from flask import render_template, Blueprint, request, redirect, make_response, g, send_from_directory, url_for
from flask_cors import cross_origin

from admin.Register import Register
from admin.login import Login,OutLogin
from admin.admin import AdminIndex
from admin.banners import Banners,Delete_Banners,Change_Banners,Change_Action_Banners,TotalBanners
from admin.custom import Custom,Change_Custom,Delete_Custom, AddCustomImg
def InitRouter(app):
    #前台页面
    @app.route('/interface/<filename>')
    @cross_origin()
    def OtherFile(filename):
        return render_template(f"public/{filename}")

    @app.route('/')
    @cross_origin()
    def IndexFile():
        return render_template('index.html')


    #后台页面
    admin_bp = Blueprint('admin', __name__)

    #登录
    @admin_bp.route('/login',methods=['POST', 'GET'])
    @cross_origin()
    def login():
        return Login()

    #注册
    @admin_bp.route('/register',methods=['POST', 'GET','OPTIONS'])
    @cross_origin()
    def register():
        return Register( )


    #banners增添操作
    @admin_bp.route('/banners/action', methods=['POST', 'GET'])
    @cross_origin()
    def banners_action():
        return Banners()

    #banners删除操作
    @admin_bp.route('/banners/action/delete', methods=['POST', 'GET'])
    @cross_origin()
    def banners_delete():
        return Delete_Banners()


    # banners修改完成操作
    @admin_bp.route('/banners/action/change', methods=['POST', 'GET'])
    @cross_origin()
    def banners_action_change():
        return Change_Action_Banners()

    #custom操作
    @admin_bp.route('/custom',methods=['POST', 'GET'])
    @cross_origin()
    def custom():
        return Custom()

     #图片上传
    @admin_bp.route('/custom/img', methods=['POST', 'GET'])
    @cross_origin()
    def add_custom_img():
        return AddCustomImg()

    #custom修改操作
    @admin_bp.route('/custom/action/change', methods=['POST', 'GET'])
    @cross_origin()
    def change_custom():
        return Change_Custom()


    # custom删除操作
    @admin_bp.route('/custom/action/delete', methods=['POST', 'GET'])
    @cross_origin()
    def delete_custom():
        return Delete_Custom()

    app.register_blueprint(admin_bp, url_prefix='/admin')

