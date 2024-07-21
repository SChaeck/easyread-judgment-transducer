from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
import pdfplumber
import os

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

            # HTML로 응답 생성
            html_response = f"""
                <html>
                    <head>
                        <title>추출된 텍스트</title>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                margin: 20px;
                            }}
                            .highlight {{
                                background-color: red; /* 드래그된 글자의 배경색 */
                                color: white; /* 드래그된 글자의 글자색 */
                            }}
                            .text {{
                                display: inline; /* 텍스트를 inline으로 표시 */
                            }}
                        </style>
                        
                    </head>
                    <body>
                        <h2>추출된 텍스트:</h2>
                        <pre id="text">{extracted_text}</pre>
                    
                        <script>
                            
                            const textElement = document.getElementById('text');
                            
                            textElement.addEventListener('mouseup', function() {{
                                const selection = window.getSelection(); // 현재 선택된 텍스트 가져오기

                                if (selection.toString()) {{ // 선택된 텍스트가 있을 경우
                                    const range = selection.getRangeAt(0); // 선택된 영역의 Range 객체
                                    const selectedText = selection.toString();
                                    const parentElement = range.startContainer.parentNode; // 선택된 텍스트의 부모 요소

                                    // 이미 하이라이트가 적용된 경우
                                    if (parentElement.classList.contains('highlight')) {{
                                        // 하이라이트 제거
                                        const span = document.createElement('span');
                                        span.textContent = selectedText; // 선택된 텍스트 복사
                                        range.deleteContents(); // 선택된 텍스트 삭제
                                        range.insertNode(span); // 새로운 스팬으로 대체
                                    }} else {{
                                        // 새로운 하이라이트 추가
                                        const span = document.createElement('span'); // 새로운 스팬 요소 생성
                                        span.className = 'highlight'; // 클래스 추가
                                        range.surroundContents(span); // 선택 영역을 스팬으로 감싸기
                                    }}
                                }}

                                selection.removeAllRanges(); // 선택 해제
                            }});

                            // 드래그 해제 기능을 위한 이벤트 리스너
                            textElement.addEventListener('mousedown', function(event) {{
                                const selection = window.getSelection();
                                const range = selection.getRangeAt(0);
                                const startContainer = range.startContainer;
                                const endContainer = range.endContainer;

                                // 드래그된 텍스트를 해제할 수 있는지 확인
                                if (startContainer.nodeType === Node.TEXT_NODE && endContainer.nodeType === Node.TEXT_NODE) {{
                                    const parentStart = startContainer.parentNode;
                                    const parentEnd = endContainer.parentNode;

                                    // 하이라이트가 적용된 경우
                                    if (parentStart.classList.contains('highlight') || parentEnd.classList.contains('highlight')) {{
                                        // 하이라이트 제거
                                        const highlightedElements = textElement.querySelectorAll('.highlight');
                                        highlightedElements.forEach(element => {{
                                            const textNode = document.createTextNode(element.textContent); // 기존 텍스트 노드 생성
                                            element.parentNode.replaceChild(textNode, element); // 하이라이트 제거
                                        }});
                                    }}
                                }}
                            }});
                        </script>
                    </body>
                </html>
            """
            return HttpResponse(html_response)

        return HttpResponse("<h2>오류:</h2><p>파일이 선택되지 않았습니다.</p>")

def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # 각 페이지에서 텍스트 추출
    return text