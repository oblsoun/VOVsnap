from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
import base64
from django.http import JsonResponse

def picture_view(request):
    return render(request, 'photo.html')

@csrf_exempt
def upload_image(request):
    if request.method == "POST" and "image" in request.POST:
        image_data = request.POST["image"]
        image_data_decode = base64.b64decode(image_data.split(',')[1])

        i = 0

        # 이미지 파일의 이름을 숫자로 하여 저장
        while True:
            image_path = os.path.join("media", f"captured_image{i + 1}.jpg")
            if not os.path.exists(image_path):
                break
            i += 1
        with open(image_path, "wb") as image_file:
            image_file.write(image_data_decode)

        # 응답을 반환 (예: 성공적으로 업로드되었음을 알리는 JSON 응답)
        result = JsonResponse({"message": "이미지가 성공적으로 업로드되었습니다."})
    else:
        result = JsonResponse({"error": "POST 요청이 아니거나 이미지 데이터가 없습니다."}, status=400)

    return result
