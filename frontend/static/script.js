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

function isMobile() {
    return window.innerWidth <= 767;
}

function initSidebar() {
    if (isMobile()) {
        sidebar.classList.add('closed');
        toggle.classList.remove('open');
    } else {
        // 在桌面版本，預設展開
        sidebar.classList.add('closed'); // 保持原有的預設收合狀態
    }
}

toggle.addEventListener('click', () => {
    if (isMobile()) {
        // 手機版：完全顯示/隱藏 sidebar
        sidebar.classList.toggle('closed');
        toggle.classList.toggle('open');
        
        // 防止背景滾動
        if (!sidebar.classList.contains('closed')) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    } else {
        // 桌面版：原有的收合/展開邏輯
        sidebar.classList.toggle('closed');
        toggle.classList.toggle('open');
    }
});

// 窗口大小改變時重新初始化
window.addEventListener('resize', () => {
    initSidebar();
    // 重置 body overflow
    document.body.style.overflow = '';
});

// 點擊 sidebar 外部關閉（僅手機版）
document.addEventListener('click', (e) => {
    if (isMobile() && !sidebar.classList.contains('closed')) {
        if (!sidebar.contains(e.target) && !toggle.contains(e.target)) {
            sidebar.classList.add('closed');
            toggle.classList.remove('open');
            document.body.style.overflow = '';
        }
    }
});

// 初始化
document.addEventListener('DOMContentLoaded', () => {
    initSidebar();
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

