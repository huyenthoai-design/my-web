// 1.
const express = require('express');
const nunjucks = require('nunjucks');
const axios = require('axios');
const path = require('path');
const app = express();
// cho phép server đọc dữ liệu dạng JSON
app.use(express.json());
// cấu hình Nunjucks để đọc thư mục Templates
nunjucks.configure(path.join(__dirname, 'home', 'Templates'), {
  autoescape: true,
  express: app
});
// phục vụ thư mục staticfiles
app.use('/static', express.static(path.join(__dirname, 'staticfiles')));


// 2.
// Lấy cổng từ biến môi trường của Render (process.env.PORT), nếu không có thì dùng 3000 (cho local)
const PORT = process.env.PORT || 3000; 


// 3. Định nghĩa một API đơn giản (route)
// ví dụ: trả về một trang HTML
app.get('/', (req, res) => {
  res.render('base.html');   // Nunjucks sẽ render file base.html
});

app.get('/trangchu', (req, res) => {
  res.render('trangchu.html'); // Nunjucks sẽ xử lý {% extends "base.html" %}
});

app.get('/gioithieu', (req, res) => {
  res.render('gioithieu.html');
});

app.get('/lienhe', (req, res) => {
  res.render('lienhe.html');
});

app.get('/minigames', (req, res) => {
  res.render('minigames.html');
});

app.get('/monhoc', (req, res) => {
  res.render('monhoc.html');
});

app.get('/sinhhoc', (req, res) => {
  res.render('sinhhoc.html');
});

// 4. Khởi động Server (Server bắt đầu lắng nghe yêu cầu)
app.listen(PORT, () => {
  console.log(`✅ Server đang chạy thành công tại http://localhost:${PORT}`);
  console.log('Server này đã sẵn sàng để triển khai lên Render.');
});