from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from MainApp import views

urlpatterns = [
    path('', views.index, name="main_page"),
    path('accounts/login/', views.index, name="main_page"),
    path('snippet/add', views.snippet_add, name="snippet_add"),
    path('snippet/list', views.snippet_list, name="snippet_list"),
    path('snippet/my', views.snippet_my, name="snippet_my"),
    path('snippet/<int:snippet_id>', views.snippet, name="snippet"),
    path('snippet/delete/<int:snippet_id>', views.snippet_delete, name="snippet_delete"),
    path('snippet/edit/<int:snippet_id>', views.snippet_edit, name="snippet_edit"),
    path('auth/login', views.login_page, name='login'),
    path('auth/logout', views.logout_page, name='logout'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


