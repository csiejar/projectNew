function checkAuthStatus() {
    fetch("/api/authUser", { method: "GET", credentials: "include" })
        .then((response) => response.json())
        .then((data) => {
            if (data.message === "已登入") {
                console.log("使用者已登入:", data.userData);
            } else {
                alert("請先登入！");
                window.location.href = "/"; // 導回首頁
            }
        })
        .catch((error) => console.error("Error fetching authUser:", error));
}

document.addEventListener("DOMContentLoaded", async function () {
    // checkAuthStatus(); // 檢查登入狀態
});