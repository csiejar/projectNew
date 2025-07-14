let currentIndex = 0;
let questions = [];

let originalAnswers = {};
let checkedAnswers = {};

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

    const q = questions[currentIndex];
    const qID = q.questionID.toString();

    questionText.textContent = q.question;
    questionID.textContent = q.questionID;
    if (q.optionA === "詳如照片") {
        optionA.textContent = "A. ";
        optionB.textContent = "B. ";
        optionC.textContent = "C. ";
        optionD.textContent = "D. ";
    }
    else {
    optionA.textContent = "A. " + q.optionA;
    optionB.textContent = "B. " + q.optionB;
    optionC.textContent = "C. " + q.optionC;
    optionD.textContent = "D. " + q.optionD;
}

    // 顯示圖片或隱藏
    if (q.image) {
        questionImage.src = q.image;
        questionImage.style.display = "block";
    } else {
        questionImage.style.display = "none";
    }

    // 顯示第幾題 / 總題數
    questionCount.textContent = `第 ${currentIndex + 1} 題 / 共 ${questions.length} 題`;

    // 控制按鈕啟用狀態
    prevBtn.disabled = currentIndex === 0;
    if (currentIndex < questions.length - 1) {
        nextBtn.disabled = false;
        nextBtn.style.display = "block";
    } else {
        nextBtn.disabled = true;
    }

    // 👉 清除先前樣式
    [optionA, optionB, optionC, optionD].forEach(btn => {
        btn.classList.remove("option-correct", "option-wrong");
    });

    // ✅ 根據 originalAnswers 與 checkedAnswers 標記選項
    const userAnswer = originalAnswers[qID];
    const correctAnswer = checkedAnswers[qID]; // 若 undefined 則代表答對了

    if (userAnswer) {
        const optionMap = { A: optionA, B: optionB, C: optionC, D: optionD };

        if (correctAnswer) {
            // 答錯了：userAnswer 是錯的、correctAnswer 是正確的
            if (optionMap[userAnswer]) optionMap[userAnswer].classList.add("option-wrong");
            if (optionMap[correctAnswer]) optionMap[correctAnswer].classList.add("option-correct");
        } else {
            // 答對了：標綠色
            if (optionMap[userAnswer]) optionMap[userAnswer].classList.add("option-correct");
        }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    prevBtn.addEventListener("click", () => {
        displayQuestion(currentIndex - 1);
    });

    nextBtn.addEventListener("click", () => {
        displayQuestion(currentIndex + 1);
    });

    const questionID = document.body.dataset.questionId;

    // 載入答題紀錄
    fetch(`/api/getAnswerRecord/${questionID}`)
        .then(response => response.json())
        .then(data => {
            if (data.message === "success") {
                originalAnswers = data.record["originalAnswers"];
                checkedAnswers = data.record["checkedAnswers"];
            } else {
                alert("無法獲取答題紀錄，請稍後再試！");
            }
        })
        .catch(error => {
            console.error('Error fetching answer record:', error);
            alert("無法獲取答題紀錄，請稍後再試！");
        });

    // 載入題目
    fetch(`/api/getQuestionsForAnswerRecord/${questionID}`)
        .then(response => response.json())
        .then(data => {
            if (data.message === "success") {
                questions = data.questions;
                displayQuestion(currentIndex);
            } else {
                alert("無法獲取題目列表，請稍後再試！");
            }
        })
        .catch(error => {
            console.error('Error fetching questions:', error);
            alert("無法獲取題目列表，請稍後再試！");
        });
});