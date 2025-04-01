const express = require('express');
const cors = require('cors'); // 引入 CORS 套件
const app = express();
const path = require('path');
const port = 8000;

// 啟用 CORS
app.use(cors());

// 提供靜態檔案
app.use('/static', express.static(path.join(__dirname, 'static')));

// 模擬科目資料
const subjects = [
  { "title": "半導體元件", "content": "二極體、BJT、MOSFET", "link": "#", "img": "/static/img/subject1.png" },
  { "title": "電路分析", "content": "基爾霍夫定律、網目分析", "link": "#", "img": "/static/img/subject2.png" },
  { "title": "電子學基礎", "content": "運算放大器、電源設計", "link": "#", "img": "/static/img/subject3.png" },
  { "title": "訊號與系統", "content": "傅立葉分析、拉普拉斯轉換", "link": "#", "img": "/static/img/subject4.png" },
  { "title": "數位電路", "content": "邏輯閘、時序電路", "link": "#", "img": "/static/img/subject5.png" },
  { "title": "微處理器", "content": "組合語言、嵌入式系統", "link": "#", "img": "/static/img/subject6.png" }
];

// 提供科目資料的 API
app.get('/api/subjects', (req, res) => {
  res.json(subjects);
});

document.addEventListener("DOMContentLoaded", function () {
  fetch('/api/authUser', { 
      method: 'GET',
      credentials: 'include' // 確保攜帶 cookies
  })
  .then(response => {
      if (!response.ok) {
          throw new Error(`HTTP 錯誤! 狀態碼: ${response.status}`);
      }
      return response.json();
  })
  .then(data => {
      if (data && data.message === "已登入") {
          console.log("用戶資料:", data.userData);
      } else {
          console.log("用戶未登入");
      }
  })
  .catch(error => console.error('Error fetching authUser:', error));
});


function handleCredentialResponse(response) {
    fetch('/api/googleLogin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential: response.credential })
    })
      .then(res => res.json())
      .then(data => {
        if (data.message === "登入成功") {
          // 直接更新前端狀態，避免刷新頁面
          updateUI(data.userData);
        }
      })
      .catch(error => console.error('登入失敗:', error));
  }
  
  // 更新 UI 的函數
  function updateUI(userData) {
    const loginButton = document.getElementById("loginBtn");
    const logoutButton = document.getElementById("logoutBtn");
    
    loginButton.style.display = "none";
    logoutButton.style.display = "block";
    console.log("即時用戶資料:", userData);
  }
  
  // 處理Google登入
app.post('/api/googleLogin', async (req, res) => {
    try {
      const ticket = await client.verifyIdToken({ idToken: req.body.credential });
      const payload = ticket.getPayload();
  
      // 儲存用戶資料到資料庫（若需）
      const user = await User.findOrCreate({ 
        where: { email: payload.email },
        defaults: { name: payload.name, avatar: payload.picture }
      });
  
      // 返回完整用戶資料
      res.json({ 
        message: "登入成功", 
        userData: { name: user.name, email: user.email } 
      });
    } catch (error) {
      res.status(401).json({ message: "登入失敗", error });
    }
  });
  
  
  // 檢查用戶狀態
  app.get('/api/authUser', (req, res) => {
    const session = req.cookies.userSession;
    res.json({ message: session ? "已登入" : "未登入" });
  });
  

// 啟動伺服器
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});