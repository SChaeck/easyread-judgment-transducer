from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 메인 페이지 URL 설정
    path('upload/', views.upload_file, name='upload'),  # 파일 업로드 URL
]

