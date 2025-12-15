// 1. Khai báo Express
const express = require('express');
const path = require('path');
const app = express();

// 2. Thiết lập Cổng (PORT)
// Lấy cổng từ biến môi trường của Render (process.env.PORT), nếu không có thì dùng 3000 (cho local)
const PORT = process.env.PORT || 3000; 

// 3. Định nghĩa một API đơn giản (route)
// Khi người dùng truy cập đường dẫn gốc '/', server sẽ trả về câu chào.
app.get('/', (req, res) => {
  res.send('Chào mừng đến với Server Node.js/Express đã sẵn sàng cho Render!');
});

app.get('home/', (req, res) => {
  res.sendFile(path.join(__dirname, 'home', 'Templates', 'home.html'));
});

// 4. Khởi động Server (Server bắt đầu lắng nghe yêu cầu)
app.listen(PORT, () => {
  console.log(`✅ Server đang chạy thành công tại http://localhost:${PORT}`);
  console.log('Server này đã sẵn sàng để triển khai lên Render.');
});