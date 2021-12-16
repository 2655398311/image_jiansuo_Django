from django.urls import path


from . import views


# fmt: off
urlpatterns = [
    # path("recoginize",views.recognize_image, name = "recognize_image")
    path('', views.index_view),
    path('login/', views.login_view),
    # 退出登录
    path('logout/', views.logout_view),
    path("dzk/",views.recognize_image, name = "recognize_image"),
    path('loadCode/',views.LoadCodeView),
    path('loadCode/',views.LoadCodeView),
    path('checkCode/',views.CheckCodeView),
    path('forget/',views.forget),
    path('touxiang/',views.touxiang),

]
