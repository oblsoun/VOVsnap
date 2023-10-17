from django.shortcuts import render
import os

def main_view(request):
    if request.method == "GET":
        
        if 'safe_image_web_urls' in request.session:
            del request.session['safe_image_web_urls']
        if 'danger_image_web_urls' in request.session:
            del request.session['danger_image_web_urls']

        # 이미지가 저장된 폴더들의 경로
        media_folders = ["media", "media_danger", "media_safe"]

        # 모든 폴더 내의 모든 파일을 가져와 삭제
        for folder in media_folders:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)

    return render(request, 'main.html')

# 이미지 파일을 삭제하는 함수
def delete_image(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)