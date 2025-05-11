// 統一檢查登入狀態的函數
function checkAuthStatus() {
    fetch("/api/authUser", { method: "GET", credentials: "include" })
        .then((response) => response.json())
        .then((data) => {
            if (data.message === "已登入") {
                // 確認是否有權限 編輯題庫
                fetch("/api/isPermitted?link=permissionAdmin", {
                    method: "GET",
                    headers: { "Content-Type": "application/json" },
                    credentials: "include",
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.message === "有權限") {
                            init(); // 有權限，無需進行任何操作
                        } else {
                            // 沒有權限，顯示錯誤訊息
                            alert("您沒有編輯題庫的權限！");
                            window.location.href = "/"; // 導回首頁
                        }
                    })
                    .catch((error) =>
                        console.error("檢查權限失敗:", error)
                    );
            } else {
                alert("請先登入！");
                window.location.href = "/"; // 導回首頁
            }
        })
        .catch((error) => console.error("Error fetching authUser:", error));
}

document.addEventListener("DOMContentLoaded", async function () {
    checkAuthStatus(); // 檢查登入狀態
});

async function init(){
    userTableBody = document.getElementById("userTableBody");
    try {
        const response = await fetch("/api/getAllPermissions");
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("Permissions data:", data);
        data.forEach((permission) => {

            const links = permission.allowLink
                .map((link) => `<a href="/${link}" class="me-2">/${link}</a>`)
                .join("");

            let count = 0;
            const permissionUserWithNames = permission.permissionUser
                .map((user) => {
                    const userName = permission.permissionUserName[count++];
                    // when hovering over the user name, show the user ID
                    return `<span title="${user}">[${userName}] </span>`;
                })
                .join("");
            userTableBody.innerHTML += `
                <tr>
                    <td>${permission.permissionID}</td>
                    <td>${permission.permissionDetails}</td>
                    <td>${links}</td>
                    <td>${permissionUserWithNames}</td>
                </tr>
            `;
        });
        // Here you can add code to handle the permissions data
    } catch (error) {
        console.error("Error fetching permissions:", error)};

    try {
        const response = await fetch("/api/getAllUsersIDAndName");
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("Users data:", data);
        data.forEach((user) => {
            const userName = user.userName;
            const userID = user.userID;
            const userOption = document.createElement("option");
            userOption.value = userID;
            userOption.textContent = `${userName} (${userID})`;
            document.getElementById("username").appendChild(userOption);
        });
    }
    catch (error) {
        console.error("Error fetching users:", error);
    };

    try {
        const response = await fetch("/api/getAllPermissions");
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log(data);
        data.forEach((permission) => {
            const option = document.createElement("option");
            option.value = permission.permissionID;
            option.textContent = `${permission.permissionID}. ${permission.permissionDetails}`;
            document.getElementById("permissionID").appendChild(option);
        });
    }
    catch (error) {
        console.error("Error fetching permissions:", error);
    };

    document.getElementById("newUserToPermission").addEventListener("click", async function () {
        const userModal = new bootstrap.Modal(document.getElementById('userModal'));
        userModal.show();
      })
}

document.onsubmit = async function (e) {
    e.preventDefault();
    const permissionID = document.getElementById("permissionID").value;
    const userID = document.getElementById("username").value;

    if (permissionID === "" || userID === "") {
        alert("請選擇使用者和權限");
        return;
    }

    const data = {
        permissionID: permissionID,
        userID: userID,
    };

    try {
        const response = await fetch("/api/addPermission", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error("Network response was not ok");
        }

        const result = await response.json();
        alert(result.message);
        window.location.reload();
    } catch (error) {
        console.error("Error adding permission:", error);
    }
}