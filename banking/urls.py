from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name="register"),
    path('login', views.login_view, name="login"),
    path('login_flutter', views.login_view_flutter, name="login_flutter"),
    path('statement', views.statement, name="statement"),
    path("logout", views.logout_view, name="logout"),
    path("family", views.family_member, name="family"),
    path("pay_bills",views.pay_bills, name="pay_bills"),
    path("add_debits",views.add_debits,name="add_debits"),

    # path("<str:etc>", views.errorPage, name="errorPage"),



    #API Routes
    path("ccds", views.credit_card_details, name="ccds")
]