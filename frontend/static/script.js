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

document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.getElementById("menuBtn");
    const sidebar = document.getElementById("sidebar");

    // 點擊按鈕開啟 Sidebar
    menuBtn.addEventListener("click", function () {
        sidebar.classList.add("show"); // 添加 show 類別
    });    

    // 點擊側邊欄外部時關閉
    document.addEventListener("click", function (event) {
        if (!sidebar.contains(event.target) && !menuBtn.contains(event.target)) {
            sidebar.classList.remove("show");
        }
    });
});

function toggleSidebar() {
    document.getElementById('sidebar').classList.toggle('collapsed');
}

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

