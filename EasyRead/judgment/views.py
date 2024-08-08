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



import requests


@csrf_exempt  
def receive_highlighted_text(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            highlighted_texts = data.get('highlighted_texts', '')
            # 여기서 highlighted_texts를 처리하는 로직 추가

            # 하이라이트된 텍스트 출력
            print("하이라이트된 텍스트:", highlighted_texts)

            # FastAPI 엔드포인트 URL
            url = "https://oriented-enormous-egret.ngrok-free.app/judgment/chain"

            judgment = highlighted_texts
            
            # 전송할 JSON 데이터
            data = {
                "judgment": judgment
            }
            # POST 요청을 JSON 데이터와 함께 전송
            response = requests.post(url, json=data)

            # 요청이 성공했는지 확인
            if response.status_code == 200:
                # JSON 응답 출력
                response_dict = response.json()
                
                # JSON 응답을 보기 좋게 포맷팅하여 출력
                print("Response JSON:", json.dumps(response_dict, indent=4, ensure_ascii=False))
            else:
                
                # 오류 응답 출력
                print("Error:", response.status_code, response.text)
                
            

            # HTML 템플릿을 렌더링하여 응답
            return render(request, 'template_name.html', {'highlighted_texts': highlighted_texts, 'response': response})
        
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)