
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost", views.newpost, name="newpost"),
    path("newcomment", views.newcomment, name="newcomment"),
    path("feed", views.feed, name="feed"),
    path("posts/<int:post_id>", views.liked, name="liked"),
    path("edit_post/<int:post_id>", views.edit, name="edit"),
    path("profile/<str:profile>", views.profile, name="profile"),
    path("following/<str:name>", views.following, name="following"),
    path("followfeed/", views.followfeed, name="followfeed"),
    path("follows", views.user_follows, name="user_follows"),
    path('upload/', views.upload, name="upload"),
    path('banner_upload/', views.banner_upload, name="banner_upload"),
    path('settings/profile_picture', views.settings, name="settings"),
    path('settings/banner_picture', views.settings_banner, name="settings_banner"),
    path('comments/<int:post_id>', views.comments, name="comments"),
    path('search/', views.search, name="search"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)