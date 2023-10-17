document.addEventListener('DOMContentLoaded', function () {
    // 서버에서 이미지 처리를 수행하기 위한 AJAX 요청
    fetch('/loading/image_processing/', {  // URL을 '/loading/image_processing/'로 수정
        method: 'POST',
    })
    .then(response => {
        if (response.status === 200) {
            return response.json(); // 서버에서 반환한 JSON 데이터를 처리
        } else {
            throw new Error('이미지 처리 실패');
        }
    })
    // JSON 응답을 처리하는 자바스크립트
    .then(data => {
        // 두 가지 경우에 따라 다른 URL로 리디렉션
        if (data.redirect_url_safe) {
            window.location.href = data.redirect_url_safe;  // safe_result 페이지로 이동
        } else if (data.redirect_url_danger) {
            window.location.href = data.redirect_url_danger;  // danger_result 페이지로 이동
        }
    });
});
