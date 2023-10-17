from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from safesnap import settings
from django.http import JsonResponse
import os

def danger_result_view(request):
    # 세션에서 이미지 데이터 가져오기
    danger_image_web_urls = request.session.get('danger_image_web_urls', [])
    safe_image_web_urls = request.session.get('safe_image_web_urls', [])
    danger_image_count = len(danger_image_web_urls)

    if danger_image_web_urls:
        # danger 이미지 데이터가 하나 이상 있는 경우
        return render(request, 'danger_result.html', {'danger_image_web_urls': danger_image_web_urls, 'safe_image_web_urls': safe_image_web_urls, 'danger_image_count': danger_image_count})
    else:
        # danger 이미지 데이터가 없고 safe 이미지 데이터가 있는 경우
        return render(request, 'safe_result.html', {'safe_image_web_urls': safe_image_web_urls})

def safe_result_view(request):
    # 세션에서 안전한 이미지 데이터 가져오기
    danger_image_web_urls = request.session.get('danger_image_web_urls', [])
    safe_image_web_urls = request.session.get('safe_image_web_urls', [])

    if not danger_image_web_urls:
        # 위험한 이미지가 없는 경우
        return render(request, 'safe_result.html', {'safe_image_web_urls': safe_image_web_urls})
    else:
         return render(request, 'danger_result.html', {'danger_image_web_urls': danger_image_web_urls, 'safe_image_web_urls': safe_image_web_urls})

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        result = None
        if not email:
            result = JsonResponse({'error': '이메일 주소를 입력해주세요.'}, status=400)
        else:
            try:
                # 이메일 객체 생성
                email_subject = "[VOV] 사진 전송"
                email_body = "[VOV] 안전한 사진 파일이 전송되었습니다."

                email = EmailMessage(
                    email_subject,
                    email_body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                
                
                email.attach_file("media/merged_image.jpg")
                email.content_subtype = "html"

                # 이메일 전송
                email.send()

                result = JsonResponse({'message': '이메일이 성공적으로 전송되었습니다.'})
            except Exception as e:
                # print(f"이메일 전송 오류: {str(e)}")
                result = JsonResponse({'error': str(e)}, status=500)
    else:
        result = JsonResponse({'error': '올바르지 않은 요청입니다.'}, status=405)
    return result 