let imgUrl = "";
document.getElementById("submit").addEventListener("click", function(event) {
    event.preventDefault(); // 防止表單提交後頁面刷新

    // 獲取題目與選項的值
    let question = document.getElementById("questionContent").value;
    let optionA = document.getElementById("optionA").value;
    let optionB = document.getElementById("optionB").value;
    let optionC = document.getElementById("optionC").value;
    let optionD = document.getElementById("optionD").value;

    // 獲取選中的正確答案
    let correctAnswer = document.querySelector('input[name="correctAnswer"]:checked');

    // 確保有選擇正確答案，否則給予提示
    if (!correctAnswer) {
        console.log("請選擇正確答案！");
        return;
    }
    if (question === "") {
        question = imgUrl.toString();
    }
    console.log(question);
    console.log("題目:", question);
    console.log("選項A:", optionA);
    console.log("選項B:", optionB);
    console.log("選項C:", optionC);
    console.log("選項D:", optionD);
    console.log("正確答案:", correctAnswer.value);
});

document.getElementById("questionImage").addEventListener("change", function(event) {
    const file = event.target.files[0];
    const shoudeBeDisabledOptions = document.getElementsByClassName("optionInput");
    const shoudeBeDisabledContent = document.getElementById("questionContent")
    if (file) {
        imgUrl = URL.createObjectURL(file);
        console.log("imgUrl:", imgUrl);
        shoudeBeDisabledContent.disabled = true;
        for (let i = 0; i < shoudeBeDisabledOptions.length; i++) {
            shoudeBeDisabledOptions[i].disabled = true;
        }
        const reader = new FileReader();
        reader.onload = function(e) {
            const imgPreview = document.getElementById("imgPreview");
            imgPreview.src = e.target.result;
            imgPreview.style.display = "block"; // 顯示圖片預覽
        };
        reader.readAsDataURL(file);
    }
}
);

document.addEventListener("DOMContentLoaded", function() {
    fetch("/api/getAllQuestions", {
        method: "GET",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => {
        console.log("所有題目:", data);
        const questionList = document.getElementById("questionList");
        data.forEach(question => {
            const li = document.createElement("li");
            li.textContent = question.question;
            questionList.appendChild(li);
        });
    })
    .catch(error => {
        console.error("Fetch error:", error);
    });
})