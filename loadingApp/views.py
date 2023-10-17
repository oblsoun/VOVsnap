from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .detectApi import DetectImageFinger
import os
from safesnap import settings
from django.urls import reverse
from django.shortcuts import render
from PIL import Image

def loading_view(request):
    return render(request, 'loading.html')

@csrf_exempt
def image_processing_view(request):
    # 이미지 파일 경로를 가져오는 부분 수정
    image_file_paths = []

    # 불러올 디렉토리 경로
    directory_path = 'media'

    # 디렉토리 내의 이미지 파일 경로 목록 가져오기
    for file_name in os.listdir(directory_path):
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(directory_path, file_name)
            image_file_paths.append(file_path)

    # DetectImageFinger 클래스 인스턴스 생성 (image_file_paths와 yolo_model 인자를 모두 전달)
    detector = DetectImageFinger(image_file_paths)

    # 이미지 처리 및 결과 확인
    results_list = detector.process_images()

    # 이미지 파일 경로 저장
    danger_image_file_paths = []
    safe_image_file_paths = []

    for i, (result, image) in enumerate(results_list):
        print(f"Result for image {i + 1}: {result}")

        if result == "danger":
            file_name = os.path.join("media_danger", f"danger_{i + 1}.jpg")
            danger_image_file_paths.append(file_name)
        else:
            file_name = os.path.join("media_safe", f"safe_{i + 1}.jpg")
            safe_image_file_paths.append(file_name)
        detector.save_blurred_image(image, file_name)


    # 이미지 파일 경로를 웹 URL로 변환
    safe_image_web_urls = [settings.MEDIA_SAFE_URL + os.path.basename(image_path) for image_path in safe_image_file_paths]
    danger_image_web_urls = [settings.MEDIA_DANGER_URL + os.path.basename(image_path) for image_path in danger_image_file_paths]

    # 이미지 데이터를 세션에 저장
    request.session['safe_image_web_urls'] = safe_image_web_urls
    request.session['danger_image_web_urls'] = danger_image_web_urls

    # 이미지 프레임에 합치기
    image_paths = []
    image_paths = get_image_paths("media_safe")
    image_paths = image_paths + get_image_paths("media_danger")
    image_paths.sort()

    images = [Image.open(path) for path in image_paths]
    width, height = images[0].size
    border_width = 30
    result = Image.new('RGB', (2 * width + 3 * border_width + 60, 2 * height + 3 * border_width + 60), 'black')
    for i in range(2):
        for j in range(2):
            bordered_image = Image.new('RGB', (width + 2 * border_width, height + 2 * border_width), 'black')
            bordered_image.paste(images[i * 2 + j], (border_width, border_width))
            result.paste(bordered_image, (j * (width + 3 * border_width), i * (height + 3 * border_width)))
    
    result_path = 'media/merged_image.jpg'
    result.save(result_path)

    # JSON 응답을 위한 결과 데이터 준비
    result_data = {
        'result': '이미지 처리 결과',  # 이미지 처리 결과를 여기에 추가
    }

    # 서버에서 두 가지 URL을 반환하는 코드
    if not danger_image_web_urls and safe_image_web_urls:
        result_data['redirect_url_safe'] = reverse('resultApp:safe_result')
    else:
        result_data['redirect_url_danger'] = reverse('resultApp:danger_result')

    # JSON 응답으로 결과 데이터 반환
    return JsonResponse(result_data)


# 이미지 합치기 위해 각 경로에 있는 이미지 배열에 넣기
def get_image_paths(folder_path):
    image_paths = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_paths.append(os.path.join(folder_path, filename))
    return image_paths