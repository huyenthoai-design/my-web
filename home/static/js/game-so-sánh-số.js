let score = 0;
let questionIdx = 1;
let timeLeft = 1000;
let timerInterval;
let currentLeft, currentRight;
let isCounting = false;
let gameStarted = false;

// 1. KHI BẤM NÚT Ở MENU HIỆN LỚP PHỦ
function showInstructions() {
    document.getElementById('start-overlay').style.display = 'flex';
    document.getElementById('game-menu').style.display = 'none';
}

// Hàm để thoát khỏi màn hình hướng dẫn quay về Menu
function exitToMenu() {
    // 1. Ẩn lớp phủ hướng dẫn (overlay)
    document.getElementById('start-overlay').style.display = 'none';
    
    // 2. Hiện lại Menu chính của game
    document.getElementById('game-menu').style.display = 'block';
    
    // 3. Đảm bảo trạng thái đếm ngược được reset (nếu cần)
    isCounting = false;
}

// 2. BẮT ĐẦU ĐẾM NGƯỢC
function startCountdown() {
    if (isCounting) return;
    isCounting = true;
    
    const instructionBox = document.getElementById('instruction-box');
    const countdownDisplay = document.getElementById('countdown-number');
    
    instructionBox.style.display = 'none';
    countdownDisplay.style.display = 'block';
    
    let count = 4;
    countdownDisplay.innerText = count;

    let timer = setInterval(() => {
        count--;
        if (count > 0) {
            countdownDisplay.innerText = count;
            document.getElementById('sound-beep').play();
        } else {
            clearInterval(timer);
            document.getElementById('start-overlay').style.display = 'none';
            startGame(); 
        }
    }, 1000);
}

// 3. BẮT ĐẦU CHƠI
function startGame() {
    gameStarted = true;
    score = 0;
    questionIdx = 1;
    
    document.getElementById('game-area').style.display = 'block';
    document.getElementById('current-pts').innerText = "0";
    document.getElementById('question-count').innerText = "1";
    
    nextQuestion();
}

// 4. TẠO CÂU HỎI TIẾP THEO
function nextQuestion() {
    if (questionIdx > 10) {
        endRound();
        return;
    }
    
    currentLeft = Math.floor(Math.random() * 10);
    do {
        currentRight = Math.floor(Math.random() * 10);
    } while (currentRight === currentLeft);

    document.getElementById('num-left').innerText = currentLeft;
    document.getElementById('num-right').innerText = currentRight;
    
    startTimer();
}

// 5. BỘ ĐẾM GIỜ CHO MỖI CÂU
function startTimer() {
    clearInterval(timerInterval);
    timeLeft = 1000; 
    
    timerInterval = setInterval(() => {
        timeLeft -= 10;
        document.getElementById('timer').innerText = (timeLeft / 1000).toFixed(3);
        
        if (timeLeft <= 0) {
            handleChoice('timeout');
        }
    }, 10);
}

// 6. XỬ LÝ KHI NGƯỜI DÙNG CHỌN
function handleChoice(choice) {
    if (!gameStarted || questionIdx > 10) return;
    clearInterval(timerInterval);
    
    let correct = false;
    if (choice === 'left' && currentLeft > currentRight) correct = true;
    if (choice === 'right' && currentRight > currentLeft) correct = true;

    if (correct) { // lưu điểm
        document.getElementById('sound-correct').play();
        score += 3;
        document.getElementById('current-pts').innerText = score;
        if (score === 30) shootConfetti(); 
    } else {
        document.getElementById('sound-wrong').play();
        const gameArea = document.getElementById('game-area');
        gameArea.classList.add('shake');
        
        gameArea.style.backgroundColor = 'rgba(255, 0, 0, 0.2)';
        setTimeout(() => { 
            gameArea.classList.remove('shake');
            gameArea.style.backgroundColor = 'transparent'; 
        }, 300);
    }

    questionIdx++;
    if (questionIdx <= 10) {
        document.getElementById('question-count').innerText = questionIdx;
        setTimeout(nextQuestion, 300); 
    } else {
        // Delay nhẹ để người dùng kịp thấy điểm câu cuối trước khi hiện thông báo
        setTimeout(endRound, 500);
    }
}

// 7. HÀM BẮN PHÁO HOA
function shootConfetti() {
    var duration = 3 * 1000;
    var end = Date.now() + duration;

    (function frame() {
        confetti({
            particleCount: 3,
            angle: 60,
            spread: 55,
            origin: { x: 0 },
            colors: ['#ffcc00', '#28a745', '#261d8a']
        });
        confetti({
            particleCount: 3,
            angle: 120,
            spread: 55,
            origin: { x: 1 },
            colors: ['#ffcc00', '#28a745', '#261d8a']
        });

        if (Date.now() < end) {
            requestAnimationFrame(frame);
        }
    }());
}

// 8. ĐIỀU KHIỂN BÀN PHÍM
window.addEventListener('keydown', (e) => {
    // Nếu đang hiện overlay và nhấn phím bất kỳ -> Đếm ngược
    const overlay = document.getElementById('start-overlay');
    if (overlay && overlay.style.display === 'flex' && !isCounting) {
        startCountdown();
        return;
    }

    // Nếu đang trong game -> Chọn trái/phải
    if (gameStarted && document.getElementById('game-area').style.display === 'block') {
        if (e.key === 'a' || e.key === 'ArrowLeft') handleChoice('left');
        if (e.key === 'd' || e.key === 'ArrowRight') handleChoice('right');
    }
});

// 9. KẾT THÚC VÀ PHÂN LOẠI LƯU ĐIỂM
function endRound() {
    gameStarted = false;
    isCounting = false; // Reset trạng thái để có thể chơi lại
    clearInterval(timerInterval);
    document.getElementById('sound-finish').play();

    // KIỂM TRA LÀ KHÁCH HAY THÀNH VIÊN
    // (Biến IS_GUEST được định nghĩa trong file HTML như đã hướng dẫn trước đó)
    if (typeof IS_GUEST !== 'undefined' && IS_GUEST === true) {
        alert("Vòng chơi kết thúc!\nĐiểm của bạn là: " + score + "\n\nBạn đang chơi với tư cách Khách. Hãy đăng ký để lưu điểm nhé!");
        window.location.reload();
        return;
    }

    // NẾU LÀ THÀNH VIÊN -> TIẾN HÀNH LƯU ĐIỂM
    const csrfTokenElement = document.querySelector('[name=csrfmiddlewaretoken]');
    if (!csrfTokenElement) {
        window.location.reload();
        return;
    }

    const token = csrfTokenElement.value;
    let formData = new FormData();
    formData.append('points', score);

    fetch('/minigames/save-game-score/', { 
        method: 'POST',
        body: formData,
        headers: { 'X-CSRFToken': token }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert("Vòng chơi kết thúc! Bạn ghi được: " + score + " điểm.\nTổng điểm tích lũy mới: " + data.total_score);
        }
        window.location.reload(); 
    })
    .catch(error => {
        console.error('Lỗi lưu điểm:', error);
        window.location.reload();
    });
}