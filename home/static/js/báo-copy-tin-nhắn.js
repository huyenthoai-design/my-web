document.querySelectorAll('.copy-btn').forEach(button => {
    button.addEventListener('click', function() {
        const text = this.getAttribute('data-copy');
        const toast = document.getElementById('copy-toast');

        // Thực hiện copy
        navigator.clipboard.writeText(text).then(() => {
            // Hiện thông báo
            toast.classList.add('show');
            
            // Ẩn thông báo sau 2 giây
            setTimeout(() => {
                toast.classList.remove('show');
            }, 2000);
        });
    });
});