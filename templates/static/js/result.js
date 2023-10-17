function isValidEmail(email) {
    // 이메일 유효성 검사를 위한 정규 표현식
    const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    return emailRegex.test(email);
}

// 이메일 전송
let isEmailSent = false; // 이메일 전송 여부를 저장하는 변수
function sendVerificationCode() {
    const email = document.getElementById("email").value;
    const csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;

    if (!isValidEmail(email)) {
        alert("올바른 이메일 주소를 입력해주세요.");
        return;
    }
    if (isEmailSent) {
        return; // 이미 이메일이 전송된 경우 아무것도 하지 않음
    }
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/result/send_email/", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.setRequestHeader("X-CSRFToken", csrf_token);
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 400) {
            const data = JSON.parse(xhr.responseText);
            if ('message' in data) {
                alert(data.message);
                isEmailSent = true; 
                // 이메일 전송 후 페이지 이동 
                window.location.href = '/'; 
            } else if ('error' in data) {
                alert(data.error);
            }
        } else {
            alert("이메일 전송에 실패했습니다.");
        }
    };
    xhr.send("email=" + email);
}