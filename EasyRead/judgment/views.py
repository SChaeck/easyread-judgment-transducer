from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
import pdfplumber
import os
from django.urls import reverse

from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'index.html')  # index.html 렌더링

def pdf_to_plain(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)  # 파일 저장
            file_path = fs.path(filename)  # 파일 경로 생성

            # PDF에서 텍스트 추출
            extracted_text = extract_text_from_pdf(file_path)

            # 파일 삭제 (필요시)
            os.remove(file_path)

            # URL을 역으로 찾아서 쿼리 매개변수를 추가
            url = reverse('display_text')  # 여기서 'display_text' 이름을 확인
            return redirect(f'{url}?extracted_text={extracted_text}')

        return HttpResponse("<h2>오류:</h2><p>파일이 선택되지 않았습니다.</p>")

def display_text(request):
    extracted_text = request.GET.get('extracted_text', '')
    return render(request, 'PDFText.html', {'extracted_text': extracted_text})

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # 각 페이지에서 텍스트 추출
    return text


from langserve import RemoteRunnable



@csrf_exempt  # CSRF 검증을 비활성화 (테스트 시에만 사용, 실제로는 사용하지 마세요)
def receive_highlighted_text(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        highlighted_texts = data.get('highlighted_texts', '')
        
        # ngrok remote 주소 설정
        chain = RemoteRunnable("https://oriented-enormous-egret.ngrok-free.app/judgment/")
        
        # 방법 1: 모든 글자 한 번에 출력
        response = chain.invoke({"judgment": highlighted_texts})
        print(response)

        
        return JsonResponse({'status': 'success', 'highlighted_texts': highlighted_texts})
