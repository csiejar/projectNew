function selectOption(option) {
    if (option.classList.contains("selected")) {
        // If the option is already selected, deselect it
        option.classList.remove("selected");
        return;
    }
    // Deselect all options
    document.getElementById("optionA").classList.remove("selected");
    document.getElementById("optionB").classList.remove("selected");
    document.getElementById("optionC").classList.remove("selected");
    document.getElementById("optionD").classList.remove("selected");
    // Select the clicked option
    option.classList.add("selected");
}

let questions = [];      // 題目資料
let currentIndex = 0;    // 目前題號索引
let usersAnswer = {}; // 使用者答案
// 使用者答案物件，key 為題目 ID，value 為使用者選擇的答案
// 例如：{ "Q1": "A", "Q2": "B" }

function getUsersAnswer() {
    usersAnswer[questions[currentIndex].questionID] = document.querySelector(".selected") ? document.querySelector(".selected").textContent.charAt(0) : null;
}

function onsubmitCheck() {
    console.log(usersAnswer);
    let hasNull = false;

    Object.entries(usersAnswer).forEach(([questionID, answer]) => {
        if (answer === null) {
            hasNull = true;
        }
    });

    if (hasNull) {
        alert("還有題目還沒回答");
        // TODO 開啟頁面讓用戶重新回答未回答問題
    } else {
        fetch('/api/submitAnswer', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "usersAnswer": usersAnswer
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "提交答案成功") {
                alert("提交成功！");
                window.location.href = "/";
            }
            else {
                alert("提交失敗，請稍後再試！");
            }
            // 處理回應
        })
        .catch(error => {
            console.error('Error submitting answers:', error);
            alert("提交失敗，請稍後再試！");
        });
    }
}

function displayQuestion(index) {
    const questionText = document.querySelector(".question-text");
    const questionCount = document.querySelector(".question-count");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const questionImage = document.querySelector(".img-fluid");
    const questionID = document.getElementById("questionID");
    const optionA = document.getElementById("optionA");
    const optionB = document.getElementById("optionB");
    const optionC = document.getElementById("optionC");
    const optionD = document.getElementById("optionD");


    if (questions.length === 0) {
        questionText.textContent = "沒有題目資料。";
        questionCount.textContent = "";
        prevBtn.disabled = true;
        nextBtn.disabled = true;
        return;
    }

    // 限制 index 不超出範圍
    if (index < 0) currentIndex = 0;
    else if (index >= questions.length) currentIndex = questions.length - 1;
    else currentIndex = index;

    // 顯示題目內容
    const q = questions[currentIndex];
    questionText.textContent = q.question;
    questionID.textContent = q.questionID;
    optionA.textContent = "A. " + q.optionA;
    optionB.textContent = "B. " + q.optionB;
    optionC.textContent = "C. " + q.optionC;
    optionD.textContent = "D. " + q.optionD;
    if (q.image) {
        questionImage.src = q.image;
        questionImage.style.display = "block"; // 顯示圖片
    }
    else {
        questionImage.style.display = "none"; // 隱藏圖片
    }

    // 顯示第幾題 / 總題數
    questionCount.textContent = `第 ${currentIndex + 1} 題 / 共 ${questions.length} 題`;

    // 控制按鈕啟用狀態
    prevBtn.disabled = currentIndex === 0;
    if (currentIndex < questions.length - 1){
        document.getElementById("submitBtn").style.display = "none";
        nextBtn.style.display = "block";
    }
    if (currentIndex === questions.length - 1){
        document.getElementById("submitBtn").style.display = "block";
        nextBtn.style.display = "none";
    }

}

function getQuestions() {
    fetch("/api/getQuestionsForQuestionPage")
        .then(response => response.json())
        .then(data => {
            questions = data;
            displayQuestion(currentIndex); // 顯示第一題
        })
        .catch(error => {
            console.error('Error fetching questions:', error);
            document.querySelector(".question-text").textContent = "載入題目失敗。";
        });
}

function unselectAllOptions() {
    const optionA = document.getElementById("optionA");
    const optionB = document.getElementById("optionB");
    const optionC = document.getElementById("optionC");
    const optionD = document.getElementById("optionD");
    optionA.classList.remove("selected");
    optionB.classList.remove("selected");   
    optionC.classList.remove("selected");
    optionD.classList.remove("selected");
}

function loadUserAnswer() {
    const questionID = questions[currentIndex].questionID;
    const userAnswer = usersAnswer[questionID];
    if (userAnswer) {
        unselectAllOptions();
        const selectedOption = document.getElementById("option" + userAnswer);
        if (selectedOption) {
            selectedOption.classList.add("selected");
        }
    }
    else {
        unselectAllOptions();
    }
}

function checkAuthStatus() {
    fetch("/api/authUser", { method: "GET", credentials: "include" })
        .then((response) => response.json())
        .then((data) => {
            if (data.message === "已登入") {
                
            } else {
                alert("請先登入！");
                window.location.href = "/"; // 導回首頁
            }
        })
        .catch((error) => console.error("Error fetching authUser:", error));
}

document.addEventListener("DOMContentLoaded", function () {
    checkAuthStatus(); // 檢查登入狀態
    getQuestions();
    document.getElementById("optionA").addEventListener("click", function () {
        selectOption(this);
    });

    document.getElementById("optionB").addEventListener("click", function () {
        selectOption(this);
    });

    document.getElementById("optionC").addEventListener("click", function () {
        selectOption(this);
    });

    document.getElementById("optionD").addEventListener("click", function () {
        selectOption(this);
    });
    // 綁定按鈕事件
    document.getElementById("prevBtn").addEventListener("click", () => {
        getUsersAnswer();
        unselectAllOptions();
        displayQuestion(currentIndex - 1);
        loadUserAnswer();
    });

    document.getElementById("nextBtn").addEventListener("click", () => {
        getUsersAnswer();
        unselectAllOptions();
        displayQuestion(currentIndex + 1);
        loadUserAnswer();
    });

    document.getElementById("submitBtn").addEventListener("click", () => {
        getUsersAnswer()
        onsubmitCheck()
    })
  });
