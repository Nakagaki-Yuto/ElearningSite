from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='blog-home'),
    path('parttimer/', views.PartTimerView.as_view(), name='blog-parttimer'),
    path('manager/', views.ManagerView.as_view(), name='blog-manager'),
    path('post/admin/', views.PostAdmin.as_view(), name='post-admin'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    path('upload', views.model_form_upload, name='upload'),
    path('pdf_view', views.pdf_view, name='pdf_view'),
]
