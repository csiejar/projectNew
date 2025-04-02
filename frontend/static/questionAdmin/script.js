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
                    }, ${question.topicID}, '${question.question}', '${question.optionA}', '${question.optionB}', '${question.optionC}', '${question.optionD}', '${question.answer}', '${question.image}', '${question.source}')">
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
                    alert("刪除失敗！");
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
        let errorText = await response.text();
        alert("編輯失敗！錯誤：" + errorText);
    }
}

function init() {
    // 初始化時載入題目
    fetchTopics();
}
window.onload = init;

function addQuestionForm() {
    // 取得 Modal
    let modal = document.getElementById("addModal");

    // 清空 Modal 內容
    document.getElementById("addQuestion").value = "";
    document.getElementById("addOptionA").value = "";
    document.getElementById("addOptionB").value = "";
    document.getElementById("addOptionC").value = "";
    document.getElementById("addOptionD").value = "";
    document.getElementById("addAnswer").value = "";
    document.getElementById("addImage").value = "";
    document.getElementById("addSource").value = "";
    document.getElementById("addTopicID").innerHTML = ""; // 清空單元選項

    // 顯示 Modal
    modal.style.display = "block";

    // 取得單元資料來填充 <select id="addTopicID">
    fetch("/api/getAllTopics")
        .then(response => response.json())
        .then(data => {
            let topicSelect = document.getElementById("addTopicID");
            topicSelect.innerHTML = ""; // 清空選項

            data.forEach(topic => {
                let option = document.createElement("option");
                option.value = topic.topicID;
                option.textContent = topic.title;
                topicSelect.appendChild(option);
            });
        })
        .catch(error => console.error("無法載入單元資料", error));
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

        console.log(response); // 這次 response 是 Response 物件，而不是 Promise

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