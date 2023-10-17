document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('webcam');
    const countdownElement = document.createElement('div');
    const imageCanvas = document.createElement('canvas');
    const imageContext = imageCanvas.getContext('2d');
    const backgroundMusic = document.getElementById('backgroundMusic');
    
    setTimeout(function () {
        backgroundMusic.play(); // 2초 후에 음악을 재생합니다.
    }, 1000); // 2초를 밀리초로 표시
    
    let capturedImages = [];
  
    // 비디오 가져오기
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function (stream) {
        video.srcObject = stream;
        video.addEventListener('loadedmetadata', function () {
          startCountdown();
        });
      })
      .catch(function (error) {
        console.error('getUserMedia 오류:', error);
      });
    
    // 카운트다운
    let countdownIntervalId;

    function startCountdown() {
        let countdown = 3;
        countdownElement.textContent = countdown;
        countdownElement.style.fontSize = '48px';
        countdownElement.style.position = 'absolute';
        countdownElement.style.top = '50%';
        countdownElement.style.left = '50%';
        countdownElement.style.transform = 'translate(-50%, -50%)';
        countdownElement.style.color = 'white';
        countdownElement.style.zIndex = '1000';
        document.body.appendChild(countdownElement);

        if (countdownIntervalId) {
            clearInterval(countdownIntervalId);
        }

        countdownIntervalId = setInterval(() => {
            countdown--;

            if (countdown === 0) {
                clearInterval(countdownIntervalId);
                countdownElement.style.display = 'none';
                startCapturingImages();
            } else {
                countdownElement.textContent = countdown.toString();
            }
        }, 1200);
    }

    function whiteOut() {
        video.style.opacity = 0;
        video.style.transition = "opacity 0.3s ease-in-out";
        setTimeout(() => {
            // 화이트아웃 효과 해제
            video.style.opacity = 1;
        }, 300); // 0.3초 후에 화이트아웃 효과를 해제합니다.
    }
    // 이미지 캡처 간격 (3.5초)
    const captureInterval = 3500;
    
    // 이미지 캡처
    function captureImage() {
        const targetWidth = 1000; // 원하는 가로 크기
        const targetHeight = 1400; // 원하는 세로 크기

        // 비디오의 가로 세로 비율
        const videoAspectRatio = video.videoWidth / video.videoHeight;

        // 캔버스의 가로 세로 비율
        const canvasAspectRatio = targetWidth / targetHeight;

        let sx = 0;
        let sy = 0;
        let sw = video.videoWidth;
        let sh = video.videoHeight;

        if (videoAspectRatio > canvasAspectRatio) {
            // 비디오의 가로 세로 비율이 더 넓을 경우
            sw = video.videoHeight * canvasAspectRatio;
            sx = (video.videoWidth - sw) / 2;
        } else {
            // 비디오의 가로 세로 비율이 더 좁을 경우
            sh = video.videoWidth / canvasAspectRatio;
            sy = (video.videoHeight - sh) / 2;
        }

        imageCanvas.width = targetWidth;
        imageCanvas.height = targetHeight;
        imageContext.drawImage(video, sx, sy, sw, sh, 0, 0, targetWidth, targetHeight);
        const imageDataURL = imageCanvas.toDataURL('image/jpeg');
  
        $.ajax({
            type: "POST",
            url: "/picture/upload/",
            data: { image: imageDataURL },
            success: function (response) {
                console.log("이미지 업로드 성공:", response);
                console.log(`targetWidth: ${targetWidth}, targetHeight: ${targetHeight}`);
                console.log(`video.videoWidth: ${video.videoWidth}, video.videoHeight: ${video.videoHeight}`);
                console.log(`sx: ${sx}, sy: ${sy}`);
            },
            error: function (error) {
                console.error("이미지 업로드 중 오류 발생:", error);
            },
        });
        
        capturedImages.push(imageDataURL);

        if (capturedImages.length === 4) {
            console.log('이미지 캡처 완료:', capturedImages);
            clearInterval(captureIntervalId);
            window.location.href = '/loading/';
        } else {
            countdownElement.style.display = 'block';
            startCountdown();
        }
    }
  
    let captureIntervalId;
    let whiteOutId;

    function startCapturingImages() {
        captureImage();
        whiteOut();
        captureIntervalId = setInterval(captureImage, captureInterval);
        whiteOutId = setInterval(whiteOut, captureInterval);
    }
});
