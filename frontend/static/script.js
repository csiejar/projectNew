// SideBar目的地設定
document.getElementById("questionBankSideBar").addEventListener("click", function () {
    window.location.href = "/question";
});

  document.getElementById("mainPageSideBar").addEventListener("click", function () {
    window.location.href = "/";
});


document.addEventListener("DOMContentLoaded", function () {
    const menuBtn = document.getElementById("menuBtn");
    const sidebar = document.getElementById("sidebar");
    const closeSidebar = document.getElementById("closeSidebar");

    // 點擊按鈕開啟 Sidebar
    menuBtn.addEventListener("click", function () {
        sidebar.classList.add("show"); // 添加 show 類別
    });

    // 點擊關閉按鈕隱藏 Sidebar
    closeSidebar.addEventListener("click", function () {
        sidebar.classList.remove("show"); // 移除 show 類別
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

