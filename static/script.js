    // 登入彈窗
    document.getElementById("userBtn").addEventListener("click", function () {
        document.getElementById("loginModal").style.display = "block";
    });
    document.querySelector(".close").addEventListener("click", function () {
        document.getElementById("loginModal").style.display = "none";
    });

    document.getElementById("loginBtn").addEventListener("click", function () {
        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;
        fetch("/api/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.message === "登入成功") {
                    document.getElementById("loginModal").style.display = "none";
                    document.getElementById("userBtn").textContent = username;
                } else {
                    alert("登入失敗");
                }
            });
    });

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("loginModal");
    const header = modal.querySelector(".modal-header"); // 設定拖動區域
    const modalBox = modal.querySelector(".modal");
    let isDragging = false;
    let offsetX, offsetY;

    // 按下鼠標開始拖動
    header.addEventListener("mousedown", function (event) {
        isDragging = true;
        offsetX = event.clientX - modal.offsetLeft;
        offsetY = event.clientY - modal.offsetTop;
        modal.classList.add("dragging");
    });

    // 移動時更改視窗位置
    document.addEventListener("mousemove", function (event) {
        if (isDragging) {
            modal.style.left = `${event.clientX - offsetX}px`;
            modal.style.top = `${event.clientY - offsetY}px`;
        }
    });

    // 放開鼠標停止拖動
    document.addEventListener("mouseup", function () {
        isDragging = false;
        modal.classList.remove("dragging");
    });

    // 點擊關閉視窗
    document.querySelector(".close").addEventListener("click", function () {
        modal.style.display = "none";
    });


    // 點擊 userBtn 顯示 Modal
    document.getElementById("userBtn").addEventListener("click", function () {
        modal.style.display = "block";
    });

    // 點擊關閉按鈕
    document.getElementById("loginModalCloseBtn").addEventListener("click", function () {
        modal.style.display = "none";
    });
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



