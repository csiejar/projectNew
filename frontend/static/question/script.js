let incompleteQuestionIndices = [];
let incompleteIndexPointer = 0;
let questions = [];
let currentIndex = 0;
let usersAnswer = {};

function selectOption(option) {
    if (option.classList.contains("selected")) {
        option.classList.remove("selected");
        return;
    }
    unselectAllOptions();
    option.classList.add("selected");

    getUsersAnswer(); // 更新答案
    checkAllAnsweredAndToggleSubmit(); // 檢查是否該顯示提交按鈕
}

function unselectAllOptions() {
    document.getElementById("optionA").classList.remove("selected");
    document.getElementById("optionB").classList.remove("selected");
    document.getElementById("optionC").classList.remove("selected");
    document.getElementById("optionD").classList.remove("selected");
}

function getUsersAnswer() {
    const answer = document.querySelector(".selected") ? document.querySelector(".selected").textContent.charAt(0) : null;
    usersAnswer[questions[currentIndex].questionID] = answer;
}

function showIncompleteAlert() {
    alert("您尚未完成所有題目，請繼續作答！");
}

function onsubmitCheck() {
    getUsersAnswer();

    incompleteQuestionIndices = [];
    incompleteIndexPointer = 0;

    for (let i = 0; i < questions.length; i++) {
        const qID = questions[i].questionID;
        const answer = usersAnswer[qID];
        if (!answer) {
            incompleteQuestionIndices.push(i);
        }
    }

    if (incompleteQuestionIndices.length > 0) {
        displayQuestion(incompleteQuestionIndices[0]);
        loadUserAnswer();
        showIncompleteAlert();
    } else {
        document.getElementById("submitBtn").disabled = true; // 禁用提交按鈕
        fetch('/api/submitAnswer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usersAnswer })
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === "提交答案成功") {
                alert("提交成功！");
                window.location.href = "/answerRecord/" + data.recordID;
            } else {
                alert("提交失敗，請稍後再試！");
            }
        })
        .catch(error => {
            console.error('Error submitting answers:', error);
            alert("提交失敗，請稍後再試！");
        });
    }
}

function checkAllAnsweredAndToggleSubmit() {
    const allAnswered = questions.every(q => usersAnswer[q.questionID]);
    if (allAnswered) {
        document.getElementById("submitBtn").style.display = "block";
        document.getElementById("nextBtn").style.display = "none";
    } else {
        if (currentIndex === questions.length - 1) {
            document.getElementById("submitBtn").style.display = "block";
            document.getElementById("nextBtn").style.display = "none";
        } else {
            document.getElementById("submitBtn").style.display = "none";
            document.getElementById("nextBtn").style.display = "block";
        }
    }
}

function displayQuestion(index) {
    if (questions.length === 0) return;

    currentIndex = Math.min(Math.max(index, 0), questions.length - 1);

    const q = questions[currentIndex];
    document.querySelector(".question-text").textContent = q.question;

    document.getElementById("optionText").innerHTML =
        "A. " + q.optionA + "<br>" +
        "B. " + q.optionB + "<br>" +
        "C. " + q.optionC + "<br>" +
        "D. " + q.optionD;

    const img = document.querySelector(".img-fluid");
    if (q.image) {
        img.src = q.image;
        img.style.display = "block";
    } else {
        img.style.display = "none";
    }

    document.querySelector(".question-count").textContent = `第 ${currentIndex + 1} 題 / 共 ${questions.length} 題`;
    document.getElementById("prevBtn").disabled = currentIndex === 0;

    loadUserAnswer();
    checkAllAnsweredAndToggleSubmit();
}

function loadUserAnswer() {
    const userAnswer = usersAnswer[questions[currentIndex].questionID];
    unselectAllOptions();
    if (userAnswer) {
        const selectedOption = document.getElementById("option" + userAnswer);
        if (selectedOption) selectedOption.classList.add("selected");
    }
}

function getQuestions() {
    fetch("/api/getQuestionsForQuestionPage")
        .then(res => res.json())
        .then(data => {
            questions = data;
            displayQuestion(currentIndex);
        })
        .catch(err => {
            console.error('Error fetching questions:', err);
            document.querySelector(".question-text").textContent = "載入題目失敗。";
        });
}

function checkAuthStatus() {
    fetch("/api/authUser", { method: "GET", credentials: "include" })
        .then(res => res.json())
        .then(data => {
            if (data.message === "已登入") {
                getQuestions();
            } else {
                alert("請先登入！");
                window.location.href = "/";
            }
        })
        .catch(err => console.error("Error fetching authUser:", err));
}

document.addEventListener("DOMContentLoaded", function () {
    checkAuthStatus();

    ["A", "B", "C", "D"].forEach(letter => {
        document.getElementById("option" + letter).addEventListener("click", function () {
            selectOption(this);
        });
    });

    document.getElementById("prevBtn").addEventListener("click", () => {
        getUsersAnswer();
        if (incompleteQuestionIndices.length > 0 && incompleteIndexPointer > 0) {
            incompleteIndexPointer--;
            displayQuestion(incompleteQuestionIndices[incompleteIndexPointer]);
        } else {
            incompleteQuestionIndices = [];
            displayQuestion(currentIndex - 1);
        }
    });

    document.getElementById("nextBtn").addEventListener("click", () => {
        getUsersAnswer();
        if (incompleteQuestionIndices.length > 0) {
            incompleteIndexPointer++;
            if (incompleteIndexPointer < incompleteQuestionIndices.length) {
                displayQuestion(incompleteQuestionIndices[incompleteIndexPointer]);
            } else {
                incompleteQuestionIndices = [];
                displayQuestion(currentIndex + 1);
            }
        } else {
            displayQuestion(currentIndex + 1);
        }
    });

    document.getElementById("submitBtn").addEventListener("click", () => {
        getUsersAnswer();
        onsubmitCheck();
    });
});
