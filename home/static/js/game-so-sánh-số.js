// Thêm vào cuối file minigames.html
let score = 0;
let questionIdx = 1;
let timeLeft = 1500;
let timerInterval;
let currentLeft, currentRight;

function startGame(type) {
    document.getElementById('game-menu').style.display = 'none';
    document.getElementById('game-area').style.display = 'block';
    nextQuestion();
}

function nextQuestion() {
    if (questionIdx > 10) {
        endRound(); // Nếu quá 10 câu thì kết thúc ngay
        return;     // Dừng hàm này lại, không chạy logic random số bên dưới nữa
    }
    
    // Random 2 số khác nhau
    currentLeft = Math.floor(Math.random() * 10);
    do {
        currentRight = Math.floor(Math.random() * 10);
    } while (currentRight === currentLeft);

    document.getElementById('num-left').innerText = currentLeft;
    document.getElementById('num-right').innerText = currentRight;
    
    startTimer();
}

function startTimer() {
    clearInterval(timerInterval);
    timeLeft = 1500; // Reset về số giây ban đầu cho mỗi câu hỏi
    
    timerInterval = setInterval(() => {
        timeLeft -= 10;
        
        // Hiển thị thời gian (chia 1000 để ra giây, lấy 3 chữ số thập phân cho mili giây)
        document.getElementById('timer').innerText = (timeLeft / 1000).toFixed(3);
        
        if (timeLeft <= 0) {
            handleChoice('timeout'); // Hết số giây thì tự động coi như sai
        }
    }, 10);
}

function handleChoice(choice) {
    clearInterval(timerInterval);
    let correct = false;
    
    if (choice === 'left' && currentLeft > currentRight) correct = true;
    if (choice === 'right' && currentRight > currentLeft) correct = true;

    if (correct) {
        score += 5;
        document.getElementById('current-pts').innerText = score;
    }

    questionIdx++;
    document.getElementById('question-count').innerText = Math.min(questionIdx, 10);
    setTimeout(nextQuestion, 200); // Nghỉ 0.2s giữa các câu
}

// Xử lý bàn phím cho Máy tính
window.addEventListener('keydown', (e) => {
    if (document.getElementById('game-area').style.display === 'block') {
        if (e.key === 'a' || e.key === 'ArrowLeft') handleChoice('left');
        if (e.key === 'd' || e.key === 'ArrowRight') handleChoice('right');
    }
});

function endRound() {
    clearInterval(timerInterval);
    
    // Lấy token từ thẻ ẩn mà Django vừa tạo ra
    const token = document.querySelector('[name=csrfmiddlewaretoken]').value;

    let formData = new FormData();
    formData.append('points', score);

    // Sử dụng đường dẫn tuyệt đối khớp với urls.py
    fetch('/minigames/save-game-score/', { 
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': token // Gửi token lên để giải quyết lỗi 403 đỏ lòm ở terminal
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert("Vòng chơi kết thúc! Tổng điểm hiện tại: " + data.total_score);
        }
        // Sau khi bấm OK ở alert, quay lại trang menu minigames.html
        window.location.href = '/game_so_sanh_so'; 
    })
    .catch(error => {
        console.error('Error:', error);
        // Ngay cả khi lỗi, vẫn phải cho người dùng về menu để không bị đơ màn hình
        window.location.href = '/game_so_sanh_so';
    });
}