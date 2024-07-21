from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # 메인 페이지 URL 설정
    path('pdf_to_plain/', views.pdf_to_plain, name='pdf_to_plain'),  # 파일 업로드 URL
]

