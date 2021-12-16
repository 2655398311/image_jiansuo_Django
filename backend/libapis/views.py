import hashlib
import json
import uuid

import requests

# from utils.code import gene_code
from django.http import HttpResponse, JsonResponse

from libapis.models import Student
import pandas as pd
from utils.code import gene_code


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from core.settings import UPLOAD_IMAGE_SAVE_DIR, XIANGSI_IMAGES_DIR
from libs.image_recognize import shibie_image

from clickhouse_driver import Client
from .models import UploadImages

def data_default(list_data):
    list_ = []
    for i in list_data:

        if '_3' in i:
            list_.append(i.split('_3')[0])
        else:
            list_.append(i)
    return list_


client2 = Client(host='10.228.81.162', port='39014', user='default', database='zhiyi', password='xtxv%qD%')


UserModel = get_user_model()


def read_sql_():

    click_house = client2.execute("select * from zhiyi.l_taobao_item_test_pipei",types_check=True)
    col = client2.execute('DESCRIBE TABLE zhiyi.l_taobao_item_test_pipei')
    col2 = pd.DataFrame(col)
    aa = pd.Series(col2[0]).tolist()
    data1 = pd.DataFrame(click_house, columns=aa)
    data1 = data1[["item_id","title","taobao_class_name","price","taobao_shop_name"]]
    return data1


def join_data(list_):

    data = read_sql_()
    data2 = pd.DataFrame(list_, columns=['item_id'])
    data2["item_id"] = data2["item_id"].apply(lambda x:str(x)+".jpg")
    frame_3 = pd.merge(data2, data, left_on='item_id', right_on='item_id', how='left', sort=False)
    data_list = [frame_3.iloc[i].to_dict() for i in frame_3.index.values]
    # aa = [i["title"] for i in data_list]
    aa = [[i["title"],i["taobao_class_name"],i["price"],i["taobao_shop_name"]] for i in data_list]

    return aa


def bing_img():
    # url = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=8'
    # aa = requests.get(url).text
    # aa = json.loads(aa)
    # images = aa["images"]
    # bb_url = ['https://cn.bing.com'+i["url"] for i in images]
    # img_desc_ = [i["copyright"] for i in images]
    # index_img = bb_url[0]
    # print(bb_url[0])
    # img_path = []
    # for i in range(len(bb_url)):
    #     img_url = bb_url[i]
    #
    #     img_path.append({"img_url": img_url})
    # # print(img_path)
    # print(index_img)
    # contxt = {
    #     "reuslt":img_path,
    #     "result_index":[{"index_img":index_img,"img_desc_":img_desc_[0]}]
    #
    # }
    # return contxt


    url = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
    aa = requests.get(url).text
    aa = json.loads(aa)
    images = aa["images"]
    bb_url = [i["url"] for i in images]
    print(bb_url)
    aa_url = [i["copyright"] for i in images]
    copyrightlink = [i["copyrightlink"] for i in images]
    index_img = bb_url

    context = {

        "url_img": 'https://cn.bing.com'+''.join(index_img),

        "img_desc": ''.join(aa_url[0]),
        "copyrightlink":''.join(copyrightlink)

    }
    # print("img_path------>", 'https://cn.bing.com' + ''.join(bb[1]))
    return context



def index_view(request):


    bb = gene_code()
    print(bb)
    # print(type(request))
    # print(type(requests))
    context = bing_img()
    if request.method == 'GET':
        # bing_img()

        return render(request,'libapis/register.html',context=context)
    else:
        #1.解收请求参数
        uname = request.POST.get('uname','')
        ucode = request.POST.get('code','')
        image_id = request.POST.get('portrait','')

        print('image_id--->', image_id)

        if len(uname) <3 or len(uname)>8 :
            # return HttpResponse("用户名输入有误！，请重新输入！")
            return render(request, "libapis/register.html",context=context)
        pwd = request.POST.get('pwd','')
        repwd = request.POST.get('repwd','')
        # url = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1"
        if pwd !=repwd:
            return render(request, "libapis/register.html", context={"tishi":"密码不一致！","url_img":context["url_img"],"img_desc":context["img_desc"],"copyrightlink":context["copyrightlink"]})
        else:

            #2.非空判断
            try:
                if uname and pwd:
                    #3.创建模型对象
                    # sutdent = Student(sname=uname,spwd=pwd)
                    #4.插入数据库
                    # sutdent.save()

                    user = UserModel.objects.create_user(username=uname,  password=pwd, first_name=image_id)
                    print('--->', model_to_dict(user))
                    #5.页面响应
                    return redirect('/student/login/')
                else:
                    return render(request, "libapis/register.html",context=context)
            except:
                return render(request,"libapis/register.html",context=context)

def LoadCodeView(request):

    img, str = gene_code()
    # 将生成的验证码存放在session中
    request.session['sessionCode'] = str
    return HttpResponse(img, content_type='image/png')

def CheckCodeView(request):
    # 获取输入框中的验证码
    code = request.GET.get('code', '')
    code = code.upper()
    # 获取生成的验证码
    sessionCode = request.session.get('sessionCode', '')
    sessionCode = sessionCode.upper()
    print(sessionCode)
    # 比较是否相等
    flag = code == sessionCode

    return JsonResponse({'checkFlag': flag})


def login_view(request):

    context = bing_img()

    # aa = gene_code()
    if request.method == 'GET':
        return render(request,'libapis/login.html')
    else:
        #1.获取请求参数

        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')

        #2.查询数据库
        if uname and pwd:
            # c = Student.objects.filter(sname=uname,spwd=pwd).count()
            #
            # if c==1:
            #     # return render(request,"libapis/recognize_image.html")
            #     return redirect('/student/dzk/')
            # data = UserModel.objects.all()
            # print(data)
            # print('sssssssssssssssssssssssss',data.get(username=uname))
            user = authenticate(username=uname, password=pwd)
            if user:
                login(request, user)
                return redirect('/student/dzk/')
            else:
                return render(request, 'libapis/login.html')

        #3.判断是否登录成功
        print("用户名不存在，请创建用户")
        return render(request,"libapis/register.html",context=context)


# 登陆后才能修改密码吧
# @login_required(login_url='/student/login/')
def forget(request):
    context = bing_img()
    print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",context["url_img"])
    if request.method == 'GET':
        # bing_img()

        return render(request,'libapis/forget.html',context={"url_img":context["url_img"],"img_desc":context["img_desc"],"copyrightlink":context["copyrightlink"]})
    else:

        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        repwd = request.POST.get('repwd')
        if uname == '':
            return render(request, 'libapis/forget.html', context={"notexis": "请输入要修改的用户！！！", "url_img": context["url_img"],"copyrightlink":context["copyrightlink"],"img_desc": context["img_desc"]})
        try:

            # 测试一下 嗯嗯
            user = UserModel.objects.get(username=uname)

            if pwd != repwd:
                return render(request, 'libapis/forget.html', context={"notexis": "两个密码不一致！请重试！","url_img":context["url_img"],"img_desc":context["img_desc"],"copyrightlink":context["copyrightlink"]})


            else:
                user.set_password(pwd)
                user.save()
                return render(request, 'libapis/forget.html', context={"notexis": "修改成功！","login":"去登录","url_img":context["url_img"],"img_desc":context["img_desc"],"copyrightlink":context["copyrightlink"]})

        except:

            return render(request, 'libapis/forget.html', context={"notexis": "用户名不存在！！","url_img":context["url_img"],"img_desc":context["img_desc"],"copyrightlink":context["copyrightlink"]})
    # return render(request, 'libapis/forget.html')


def logout_view(request):
    if request.method == 'GET':
        print('User-->', request.user)
        logout(request)
        return redirect('/student/login/')

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator



@login_required(login_url='/student/login/')

def recognize_image(request):
    print(request.GET, request.POST, request.FILES)
    print('User1-->', request.user)
    image_id = request.user.first_name
    upload_image = UploadImages.objects.get(id=image_id)

    if request.method == "POST":
        action = request.POST.get("action", None)


        if action == "upload_image":
            try:
                input_file = request.FILES["input_image"]
            except Exception as e:
                print(e)

            image_raw_name = input_file.name

            image_uname = f"{uuid.uuid4().hex}.png"

            with open(UPLOAD_IMAGE_SAVE_DIR + "/" + image_uname, "wb") as f:
                for chunk in input_file.chunks():
                    f.write(chunk)

            UploadImages.objects.create(raw_name=image_raw_name, uname=image_uname)

            print(request.FILES, image_raw_name, image_uname,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            context = {
                "result": "upload_success",
                "input_image_path": str(UPLOAD_IMAGE_SAVE_DIR + "/" + image_uname),
                "image_uname": image_uname,
                "user_login":request.user,
                'portrait_path': upload_image.raw_name
            }

            return render(
                request,
                "libapis/recognize_image.html",
                context=context,
            )
        elif action == "recognize_image":
            input_image_uname = request.POST.get("input_image_uname", None)
            print(input_image_uname)
            input_image: UploadImages = UploadImages.objects.filter(
                uname=input_image_uname
            ).first()
            print('input_image-->', input_image.uname)
            if input_image:
                queryDir_path = str(UPLOAD_IMAGE_SAVE_DIR + "/" + input_image.uname)
                image_names = shibie_image(queryDir_path=queryDir_path)
                image_names = [name.decode() for name in image_names]
                image_paths = [
                    str(XIANGSI_IMAGES_DIR + '/' + name) for name in image_names
                ]

                img_url_local = [str(ip.split("/")[6].split('.jpg')[0]) for ip in image_paths]
                bb = join_data(img_url_local)
                img_paths = []
                for i in range(len(img_url_local)):
                    item_name = img_url_local[i]
                    item_title = bb[i][0]
                    item_class_name = bb[i][1]
                    price = bb[i][2]
                    taobao_shop_name = bb[i][3]
                    img_paths.append({'item_name': item_name, 'item_title': item_title,"item_class_name":item_class_name,"price":price,"taobao_shop_name":taobao_shop_name})

                print('*'*10)
                print(img_paths)
                print('*'*10)

                print('---->', input_image_uname)
                context = {
                    "result": "recognize_image",
                    "input_image_path": str(
                        UPLOAD_IMAGE_SAVE_DIR + "/" + input_image.uname
                    ),

                    "image_paths": img_paths,
                    "image_uname": input_image_uname,
                    "user_login":request.user,
                    'portrait_path': upload_image.raw_name
                }

                return render(
                    request,
                    "libapis/recognize_image.html",
                    context=context,
                )

    else:

        print('upload_image-->', upload_image.raw_name)
        return render(request, "libapis/recognize_image.html",
                      context={"result": "", "user_login": request.user, 'portrait_path':  upload_image.raw_name})




@method_decorator(csrf_exempt)
def touxiang(request):
    if request.method == "POST":
        # 上传文件
        import hashlib
        hlmd5 = hashlib.md5()
        portrait = request.FILES.get('portrait')
        if portrait.name:
            hlmd5.update(portrait.name.encode('utf-8'))
            file_name = hlmd5.hexdigest()
            ext_name = portrait.name.split('.')[-1]
            file_path = f'{UPLOAD_IMAGE_SAVE_DIR}/%s.%s' % (file_name, ext_name)
            print(file_path,"*******************************************")
            save_path = f'/media/images/upload/%s.%s' % (file_name, ext_name)
            with open(file_path, 'wb+') as destination:
                for chunk in portrait.chunks():
                    destination.write(chunk)
            upload_image = UploadImages.objects.create(raw_name=save_path, uname=portrait.name)
            return JsonResponse({'raw_name': upload_image.raw_name,
                                 'uname': upload_image.uname,
                                 'image_id': upload_image.id})

