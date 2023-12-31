from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('listing/<int:id>',views.listing,name='listing'),
    path('comments/<int:id>',views.comment,name='comment'),
    path('bids/<int:id>',views.bids,name='bids'),
    path('create',views.create,name='create'),
    path('watchlist',views.Watchlist,name='watchlist'),
    path('deletewatchlist',views.deletewatch,name='deletewatchlist'),
    path('closelisting',views.closelistings,name='closelisting'),
    path('categories',views.Categories,name='categories'),
    path('viewcat',views.viewcat,name='viewcat')
]
