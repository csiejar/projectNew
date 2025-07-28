// SideBar目的地設定Add commentMore actions
document.getElementById("questionBankSideBar").addEventListener("click", function () {
    window.location.href = "/questionSelector";
});

  document.getElementById("mainPageSideBar").addEventListener("click", function () {
    window.location.href = "/";
});
document.getElementById("WrongQuestionBookSideBar").addEventListener("click", function () {
    window.location.href = "/userAnswerRecord";
});
document.getElementById("demoTestSideBar").addEventListener("click", function () {
    window.location.href = "/question";
});
document.getElementById("correctRateSideBar").addEventListener("click", function () {
    window.location.href = "/correctRate";
});
const sidebar = document.getElementById('sidebar');
const toggle = document.getElementById('toggleButton');

toggle.addEventListener('click', () => {
sidebar.classList.toggle('closed');
toggle.classList.toggle('open');
    });

function handleCredentialResponse(response) {
    // 發送 token 到後端驗證
    fetch('/api/googleLogin', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: response.credential })
    })
    .then(res => res.json())
    .then(data => {
        console.log("後端回應:", data);
        window.location.reload();
    })
    .catch(err => console.error("驗證錯誤:", err));
}

