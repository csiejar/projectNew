function checkAuthStatus() {
    fetch("/api/authUser", { method: "GET", credentials: "include" })
        .then((response) => response.json())
        .then((data) => {
            if (data.message === "已登入") {
                fetch("/api/getUserAnswerRecord", { method: "GET", credentials: "include" })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.message === "success") {
                            const userAnswerRecord = data.records;
                            if (userAnswerRecord.length === 0) {
                                alert("目前沒有答題紀錄！");
                                window.location.href = "/"; // 導回首頁
                            }
                            const answerRecordTableBody = document.getElementById("answerRecordTableBody");
                            answerRecordTableBody.innerHTML = ""; // 清空表格內容
                            userAnswerRecord.forEach((record) => {
                                const row = document.createElement("tr");
                                const totalAnswerCount = record.totalAnswersCount;
                                const correctAnswerCount = record.correctAnswersCount;
                                let correctRate = ((correctAnswerCount / totalAnswerCount) * 100).toFixed(1);
                                if (correctRate == 0) {
                                    correctRate = 0;
                                }
                                let goodOrBad = correctRate >= 50 ? "✅" : "❌";
                                if (correctRate == 0) {
                                    goodOrBad = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;☠️";
                                }
                                row.innerHTML = `
                                    <td>${record.recordID}</td>
                                    <td>${record.timestamp}</td>
                                    
                                    <td><span title="答對題數 / 總題數\n ${correctAnswerCount} / ${totalAnswerCount}">${correctRate} % ${goodOrBad} </span></td>
                                    <td>
                                    <button class="btn btn-outline-dark" onclick="window.location.href='/answerRecord/${record.recordID}'">
                                        <i class="bi bi-arrow-clockwise"></i>
                                    </button>
                                    </td>
                                `;
                                answerRecordTableBody.appendChild(row);
                            });
                        } else {
                            alert("無法獲取答題紀錄！");
                        }
                    })
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