// script.js
document.addEventListener("DOMContentLoaded", function() {
  // Lấy tất cả các phần tử toggle
  const toggles = document.querySelectorAll(".tree .toggle");

  toggles.forEach(toggle => {
    toggle.addEventListener("click", function(e) {
      e.stopPropagation(); // tránh ảnh hưởng đến các cấp cha

      const nextUl = this.nextElementSibling;

      if (nextUl && nextUl.tagName === "UL") {
        // Nếu đang mở thì đóng lại
        if (nextUl.classList.contains("show")) {
          nextUl.classList.remove("show");
          this.classList.remove("open");
        } else {
          // Nếu đang đóng thì mở ra
          nextUl.classList.add("show");
          this.classList.add("open");
        }
      }
    });
  });
});