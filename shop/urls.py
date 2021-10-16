from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="ShopHome"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("tracker/", views.tracker, name="tracker"),
    path("search/", views.search, name="search"),
    path("products/<int:myid>", views.productView, name="productView"),
    path("checkout/", views.checkout, name="checkout"),
    path('signin/', views.signin, name="signin"),
    path('signout/', views.signout, name="signout"),
    path('signup/', views.signup, name="signup"),
    path('account/', views.account, name="account"),
    path('temp/', views.temp, name="temp"),
    path('temp2/', views.temp2, name="temp2"),
]
