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

document.addEventListener("DOMContentLoaded", function () {
    const userBtn = document.getElementById("userBtn");
    const userInfoOverlay = document.getElementById("userInfoOverlay");
    const closeUserCard = document.getElementById("closeUserCard");

    const menuBtn = document.getElementById("menuBtn");
    const sidebar = document.getElementById("sidebar");
    // SideBar目的地設定
    document.getElementById("questionBankSideBar").addEventListener("click", function () {
        window.location.href = "/question";
    });

    document.getElementById("mainPageSideBar").addEventListener("click", function () {
        window.location.href = "/";
    });
    document.getElementById("WrongQuestionBookSideBar").addEventListener("click", function () {
        window.location.href = "/userAnswerRecord";
    });


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

    userBtn.addEventListener("click", function () {
      fetch('/api/authUser', { method: 'GET', credentials: 'include' })
        .then(res => res.json())
        .then(data => {
          if (data.message === "已登入") {
            document.getElementById("userAvatar").src = data.userData.userImg || "../static/img/default-avatar.png";
            document.getElementById("userName").textContent = data.userData.name;
            document.getElementById("userEmail").textContent = data.userData.email;
            document.getElementById("g_id_onload").style.display = "none";
            document.getElementById("loginBtn").style.display = "none";
            userInfoOverlay.style.display = "flex";
          }
          else {
            document.getElementById("userAvatar").src = "../static/img/default-avatar.png";
            document.getElementById("userName").textContent = "您尚未登入";
            document.getElementById("userEmail").textContent = "登入後即顯示";
            document.getElementById("manageAccountBtn").style.display = "none";
            document.getElementById("addAccountBtn").style.display = "none";
            document.getElementById("logoutFromCard").style.display = "none";
            userInfoOverlay.style.display = "flex";
          }
        })
        .catch(err => console.error("取得使用者資訊失敗:", err));
    });

    // 關閉卡片按鈕
    closeUserCard.addEventListener("click", function () {
      userInfoOverlay.classList.add('fade-out');
      setTimeout(() => {
        userInfoOverlay.style.display = 'none';
        userInfoOverlay.classList.remove('fade-out');
      }, 300);
    });

    // 點擊遮罩關閉
    userInfoOverlay.addEventListener("click", function (event) {
      if (event.target === userInfoOverlay) {
        userInfoOverlay.classList.add('fade-out');
        setTimeout(() => {
          userInfoOverlay.style.display = 'none';
          userInfoOverlay.classList.remove('fade-out');
        }, 300);
      }
    });

    // 登出按鈕
    document.getElementById("logoutFromCard").addEventListener("click", logout);

    // 新增帳戶事件處理
    document.getElementById("addAccountBtn").addEventListener("click", function () {
      window.location.href = "/addAccount";
    });

    // 管理帳戶事件處理
    document.getElementById("manageAccountBtn").addEventListener("click", function () {
      window.location.href = "/manageAccount";
    });

    // ESC 鍵關閉彈窗
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && userInfoOverlay.style.display === 'flex') {
        userInfoOverlay.classList.add('fade-out');
        setTimeout(() => {
          userInfoOverlay.style.display = 'none';
          userInfoOverlay.classList.remove('fade-out');
        }, 300);
      }
    });

    const urlParams = new URLSearchParams(window.location.search);
    const refreshed = urlParams.get('refreshed');

    if (refreshed === 'true') {
      checkAuthStatus();
    } else {
      checkAuthStatus();
    }

    function checkAuthStatus() {
      fetch('/api/authUser', { method: 'GET', credentials: 'include' })
        .then(response => response.json())
        .then(data => {
          if (data.message === "已登入") {
            loginButton.style.display = "none";
            logoutButton.style.display = "block";
            loginButtonMainPage.style.display = "none";
            logoutButtonMainPage.style.display = "flex";
            console.log("用戶資料:", data.userData);
          } else {
            loginButton.style.display = "block";
            logoutButton.style.display = "none";
            loginButtonMainPage.style.display = "flex";
            logoutButtonMainPage.style.display = "none";
            console.log("用戶未登入");
          }
        })
        .catch(error => console.error('Error fetching authUser:', error));
    }

    function logout() {
      fetch('/api/logout', { method: 'POST', credentials: 'include' })
        .then(response => response.json())
        .then(result => {
          if (result.message === "登出成功") {
            window.location.href = "/"; // 導回首頁
          }
        })
        .catch(error => console.error('登出失敗:', error));
    }
  });