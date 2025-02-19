document.addEventListener("DOMContentLoaded", function () {
    let currentQuestion = null;
    
    // 漢堡選單
    document.getElementById("menuBtn").addEventListener("click", function () {
        document.getElementById("sidebar").classList.add("show");
    });
    document.getElementById("closeSidebar").addEventListener("click", function () {
        document.getElementById("sidebar").classList.remove("show");
    });

    // 獲取題目
    function loadQuestion() {
        answered = false;
        fetch("/api/questions")
            .then(response => response.json())
            .then(data => {
                currentQuestion = data.questions[Math.floor(Math.random() * data.questions.length)];
                document.getElementById("questionText").textContent = currentQuestion.question;
                let optionsList = document.getElementById("optionsList");
                optionsList.innerHTML = "";
                
                currentQuestion.options.forEach(option => {
                    let li = document.createElement("li");
                    let radio = document.createElement("input");
                    radio.type = "radio";
                    radio.name = "quizOption";
                    radio.value = option;
                    radio.classList.add("option-radio");
                    
                    let label = document.createElement("label");
                    label.appendChild(radio);
                    label.appendChild(document.createTextNode(" " + option));
                    label.classList.add("option-label");
                    
                    li.appendChild(label);
                    li.classList.add("option-item");
                    li.addEventListener("click", function () {
                        if (!answered) {
                            checkAnswer(option);
                        }
                    });
                    optionsList.appendChild(li);
                });
            });
    }

    // 檢查答案
    function checkAnswer(selectedOption) {
        answered = true;
        let message = document.createElement("p");
        if (selectedOption === currentQuestion.answer) {
            message.textContent = "✅ 正確！";
            message.style.color = "green";
        } else {
            message.textContent = "❌ 錯誤，正確答案是：" + currentQuestion.answer;
            message.style.color = "red";
        }
        document.getElementById("optionsList").appendChild(message);

        // 禁止選擇其他答案
        document.querySelectorAll(".option-radio").forEach(radio => {
            radio.disabled = true;
        });

        // 顯示下一題按鈕
        let nextButton = document.createElement("button");
        nextButton.textContent = "下一題";
        nextButton.classList.add("btn", "btn-primary", "mt-3");
        nextButton.addEventListener("click", function () {
            loadQuestion();
            nextButton.remove();
            message.remove();
        });
        document.getElementById("optionsList").appendChild(nextButton);
    }

    document.getElementById("getQuestionBtn").addEventListener("click", function () {
        loadQuestion();
        this.style.display = "none";
    });

    
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
});



