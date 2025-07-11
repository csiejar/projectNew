let topicsMap = {}; // 存 topicID -> title
let topicsArray = []; // 存 topic 物件，方便下拉選單使用
let currentEditID = null; // 目前正在編輯的題目 ID

async function fetchTopics() {
    try {
        let response = await fetch("/api/getAllTopics");
        let data = await response.json();

        data.forEach((topic) => {
            topicsMap[topic.topicID] = topic.title;
        });

        topicsArray = data; // 儲存完整 topic 陣列
        fetchQuestions();
    } catch (error) {
        console.error("載入單元失敗:", error);
    }
}

async function fetchQuestions() {
    try {
        let response = await fetch("/api/getAllQuestions");
        let data = await response.json();

        let tableBody = document.querySelector("#questionsTable tbody");
        tableBody.innerHTML = ""; // 清空舊資料

        data.forEach((question) => {
            let row = document.createElement("tr");

            row.innerHTML = `
                <td>${question.questionID}</td>
                <td>${topicsMap[question.topicID] || "未知單元"}</td>
                <td>${question.question}</td>
                <td>${question.optionA}</td>
                <td>${question.optionB}</td>
                <td>${question.optionC}</td>
                <td>${question.optionD}</td>
                <td>${question.answer}</td>
                <td>${
                    question.image
                        ? `<img src="${question.image}" width="50">`
                        : "無"
                }</td>
                <td>${question.source}</td>
                <td>
                    <button class="btn btn-link p-0 edit-btn" onclick="openEditModal(${
                        question.questionID
                    }, ${question.topicID}, '${question.question}', '${
                question.optionA
            }', '${question.optionB}', '${question.optionC}', '${
                question.optionD
            }', '${question.answer}', '${question.image}', '${
                question.source
            }')">
                        <i class="bi bi-pencil-square"></i>
                    </button>
                    <button class="btn btn-link p-0 delete-btn" onclick="deleteQuestion(${
                        question.questionID
                    })">
                        <i class="bi bi-trash3-fill"></i>
                    </button>
                </td>
            `;

            tableBody.appendChild(row);
        });
    } catch (error) {
        console.error("載入題目失敗:", error);
    }
}

function deleteQuestion(questionID) {
    if (confirm("確定要刪除這個問題嗎？")) {
        fetch("/api/deleteQuestion", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ questionID: Number(questionID) }),
        })
            .then((response) => {
                if (response.ok) {
                    alert("刪除成功！");
                    fetchQuestions();
                } else {
                    let errorText = response.statusText;
                    alert("刪除失敗！錯誤：" + errorText);
                }
            })
            .catch((error) => console.error("刪除問題失敗:", error));
            
    }
}

function openEditModal(
    questionID,
    topicID,
    question,
    optionA,
    optionB,
    optionC,
    optionD,
    answer,
    image,
    source
) {
    currentEditID = questionID;
    document.getElementById("editQuestionID").value = questionID;
    document.getElementById("editQuestion").value = question;
    document.getElementById("editOptionA").value = optionA;
    document.getElementById("editOptionB").value = optionB;
    document.getElementById("editOptionC").value = optionC;
    document.getElementById("editOptionD").value = optionD;
    document.getElementById("editImage").value = image;
    document.getElementById("editSource").value = source;

    // 設定下拉選單的預設答案
    document.getElementById("editAnswer").value = answer;

    // 生成單元選擇
    let topicSelect = document.getElementById("editTopicID");
    topicSelect.innerHTML = ""; // 清空舊選項
    topicsArray.forEach((topic) => {
        let option = document.createElement("option");
        option.value = topic.topicID;
        option.textContent = topic.title;
        if (topic.topicID == topicID) {
            option.selected = true;
        }
        topicSelect.appendChild(option);
    });

    document.getElementById("editModal").style.display = "block";
}
function closeModal() {
    document.getElementById("editModal").style.display = "none";
}

async function saveEdit() {
    let questionID = currentEditID;
    let topicID = document.getElementById("editTopicID").value;
    let question = document.getElementById("editQuestion").value;
    let optionA = document.getElementById("editOptionA").value;
    let optionB = document.getElementById("editOptionB").value;
    let optionC = document.getElementById("editOptionC").value;
    let optionD = document.getElementById("editOptionD").value;
    let answer = document.getElementById("editAnswer").value;
    let image = document.getElementById("editImage").value;
    let source = document.getElementById("editSource").value;

    let response = await fetch("/api/editQuestion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            questionID: Number(questionID), // 確保是數字
            topicID: Number(topicID), // 確保是數字
            question: question,
            optionA: optionA,
            optionB: optionB,
            optionC: optionC,
            optionD: optionD,
            answer: answer,
            image: image,
            source: source,
        }),
    });

    if (response.ok) {
        alert("編輯成功！");
        closeModal();
        fetchQuestions();
    } else {
        let errorText = await response.statusText;
        alert("編輯失敗！錯誤：" + errorText);
    }
}

function init() {
    // 初始化時載入題目
    fetchTopics();
}
// window.onload = init;

function addQuestionForm() {
    // 取得 Modal
    let modal = document.getElementById("addModal");

    // 清空 Modal 內容並重新啟用所有輸入框
    document.getElementById("addQuestion").value = "";
    document.getElementById("addQuestion").disabled = false;
    
    document.getElementById("addOptionA").value = "";
    document.getElementById("addOptionA").disabled = false;
    
    document.getElementById("addOptionB").value = "";
    document.getElementById("addOptionB").disabled = false;
    
    document.getElementById("addOptionC").value = "";
    document.getElementById("addOptionC").disabled = false;
    
    document.getElementById("addOptionD").value = "";
    document.getElementById("addOptionD").disabled = false;
    
    document.getElementById("addAnswer").value = "";
    document.getElementById("addImage").value = "";
    document.getElementById("addSource").value = "";
    document.getElementById("addTopicID").innerHTML = ""; // 清空單元選項
    
    // 清空檔案輸入
    document.getElementById("addFileInput").value = "";
    uploadedFile = null;

    // 顯示 Modal
    modal.style.display = "block";

    // 取得單元資料來填充 <select id="addTopicID">
    fetch("/api/getAllTopics")
        .then((response) => response.json())
        .then((data) => {
            let topicSelect = document.getElementById("addTopicID");
            topicSelect.innerHTML = ""; // 清空選項

            data.forEach((topic) => {
                let option = document.createElement("option");
                option.value = topic.topicID;
                option.textContent = topic.title;
                topicSelect.appendChild(option);
            });
        })
        .catch((error) => console.error("無法載入單元資料", error));
}

// 關閉 Modal
function closeAddModal() {
    document.getElementById("addModal").style.display = "none";
}

async function saveAdd() {
    let topicID = document.getElementById("addTopicID").value;
    let question = document.getElementById("addQuestion").value;
    let optionA = document.getElementById("addOptionA").value;
    let optionB = document.getElementById("addOptionB").value;
    let optionC = document.getElementById("addOptionC").value;
    let optionD = document.getElementById("addOptionD").value;
    let answer = document.getElementById("addAnswer").value;
    let image = document.getElementById("addImage").value;
    let source = document.getElementById("addSource").value;
    let files = document.getElementById("addFileInput").files;
    
    // 檢查是否已選擇答案
    if (!answer || answer === "") {
        alert("請選擇正確答案！");
        return;
    }
    if (!topicID || topicID === "") {
        alert("請選擇單元！");
        return;
    }

    if (!question || question === "") {
        alert("請輸入題目！");
        return;
    }
    if (!optionA || optionA === "") {
        alert("請輸入選項 A！");
        return;
    }
    if (!optionB || optionB === "") {
        alert("請輸入選項 B！");
        return;
    }
    if (!optionC || optionC === "") {
        alert("請輸入選項 C！");
        return;
    }
    if (!optionD || optionD === "") {
        alert("請輸入選項 D！");
        return;
    }

    if (files.length > 0) {
        alert("正在上傳檔案，請稍候...");
        let saveBtn = document.getElementById("saveAddBtn");
        saveBtn.disabled = true; // 禁用按鈕，防止重複
        //有上傳檔案
        // 先上傳檔案到伺服器
        let uploadedFile = files[0];
        let formData = new FormData();
        formData.append("file", uploadedFile); // 注意這裡要叫 "file"，和 FastAPI 的參數名稱一致

        fetch("/uploadfile", {
            method: "POST",
            body: formData,
        })
            .then((response) => {
                if (response.ok) {
                    return fetch("/uploadToDrive", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            topicID: Number(topicID), // 確保是數字
                            fileName: uploadedFile.name, // 這裡是上傳的檔案名稱
                        }),
                    })
                        .then((response) => {
                            if (response.ok) {
                                response.json().then((data) => {
                                    url = data.url; // 更新 image 變數為 Google Drive 的檔案 URL
                                    // TODO 新增題目並上傳到資料庫
                                    return fetch("/api/addQuestion", {
                                        method: "POST",
                                        headers: {
                                            "Content-Type": "application/json",
                                        },
                                        body: JSON.stringify({
                                            topicID: Number(topicID), // 確保是數字
                                            question: "詳如照片",
                                            optionA: "詳如照片",
                                            optionB: "詳如照片",
                                            optionC: "詳如照片",
                                            optionD: "詳如照片",
                                            answer: answer,
                                            image: url, // 使用 Google Drive 的檔案 URL
                                            source: source,
                                        }),
                                    })
                                        .then((response) => {
                                            if (response.ok) {
                                                alert("新增成功！");
                                                closeAddModal(); // 關閉 Modal
                                                fetchQuestions(); // 重新載入題目列表
                                            } else {
                                                alert("新增失敗！");
                                            }
                                        })
                                        .catch((error) =>
                                            console.error(
                                                "新增題目失敗:",
                                                error
                                            )
                                        );
                                });
                            } else {
                                alert("檔案上傳到 專題室電腦 失敗！");
                            }
                        })
                        .catch((error) =>
                            console.error(
                                "檔案上傳到 專題室電腦 失敗！",
                                error
                            )
                        );
                } else {
                    response.json().then((data) => {
                        console.error("上傳失敗細節：", data);
                        alert("檔案上傳失敗！");
                    });
                }
            })
            .catch((error) => console.error("檔案上傳失敗:", error));
    } else {
        //沒有上傳檔案 完成
        try {
            let response = await fetch("/api/addQuestion", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    topicID: Number(topicID), // 確保是數字
                    question: question,
                    optionA: optionA,
                    optionB: optionB,
                    optionC: optionC,
                    optionD: optionD,
                    answer: answer,
                    image: image,
                    source: source,
                }),
            });

            if (response.ok) {
                alert("新增成功！");
                closeAddModal(); // 關閉 Modal
                fetchQuestions(); // 重新載入題目列表
            } else {
                let errorText = await response.text(); // ❗ 這裡也要 `await`
                alert("新增失敗！錯誤：" + errorText);
            }
        } catch (error) {
            console.error("發生錯誤：", error);
            alert("新增失敗！請檢查網路或伺服器狀態。");
        }
    }
}

let uploadedFile = null; // 用來儲存選取的檔案

// 當按下「上傳檔案」按鈕
document
    .getElementById("addQuestionByUploadingFile")
    .addEventListener("click", function () {
        document.getElementById("addFileInput").click();
    });

// 當使用者選擇檔案
document
    .getElementById("addFileInput")
    .addEventListener("change", function (event) {
        uploadedFile = event.target.files[0];
        if (uploadedFile) {
            alert("已選擇檔案：" + uploadedFile.name);
            
            // 禁用輸入框並設置為"詳如照片"
            document.getElementById("addQuestion").value = "詳如照片";
            document.getElementById("addQuestion").disabled = true;
            
            document.getElementById("addOptionA").value = "詳如照片";
            document.getElementById("addOptionA").disabled = true;
            
            document.getElementById("addOptionB").value = "詳如照片";
            document.getElementById("addOptionB").disabled = true;
            
            document.getElementById("addOptionC").value = "詳如照片";
            document.getElementById("addOptionC").disabled = true;
            
            document.getElementById("addOptionD").value = "詳如照片";
            document.getElementById("addOptionD").disabled = true;
        }
    });

document.addEventListener("DOMContentLoaded", function () {
    // 檢查 URL 是否包含刷新標記
    const urlParams = new URLSearchParams(window.location.search);
    const refreshed = urlParams.get("refreshed");

    if (refreshed === "true") {
        console.log("已刷新過頁面，執行檢查登入狀態");
        checkAuthStatus(); // 檢查登入狀態
    } else {
        checkAuthStatus(); // 初始化檢查登入狀態
    }

    // 統一檢查登入狀態的函數
    function checkAuthStatus() {
        fetch("/api/authUser", { method: "GET", credentials: "include" })
            .then((response) => response.json())
            .then((data) => {
                if (data.message === "已登入") {
                    document.getElementById("nameDisplay").textContent += data.userData.name; // 顯示使用者名稱
                    // 確認是否有權限 編輯題庫
                    fetch("/api/isPermitted?link=questionAdmin", {
                        method: "GET",
                        headers: { "Content-Type": "application/json" },
                        credentials: "include",
                    })
                        .then((response) => response.json())
                        .then((data) => {
                            if (data.message === "有權限") {
                                // 有權限，載入題目
                                init();
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
});
