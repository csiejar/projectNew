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

// 啟動伺服器
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});