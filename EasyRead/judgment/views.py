from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
import pdfplumber
import os

def index(request):
    return render(request, 'index.html')  # index.html 렌더링

def upload_file(request):
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

            # HTML로 응답 생성
            html_response = f"<h2>추출된 텍스트:</h2><pre>{extracted_text}</pre>"
            return HttpResponse(html_response)

        else:
            return HttpResponse("<h2>오류:</h2><p>파일이 선택되지 않았습니다.</p>")

    return HttpResponse("<h2>오류:</h2><p>파일 업로드 실패</p>")

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # 각 페이지에서 텍스트 추출
    print(text)  # 콘솔에 출력
    return text
