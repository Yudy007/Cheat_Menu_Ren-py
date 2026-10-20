# 🎮 Cheat Menu & Auto-Repair Mod Cho Game Ren'Py

> **Universal All-in-One Mod:** Bộ công cụ Cheat Menu và Cứu hộ tự động sửa lỗi kịch bản dành cho mọi game Ren'Py (Ren'Py 6, Ren'Py 7 - Python 2, Ren'Py 8 & 9 - Python 3).

---

## ✨ Điểm Nổi Bật

1. **Kết Nối 1-Click (Chỉ 1 file duy nhất):**
   - Chỉ cần thả file `cheat_connect.rpy` (hoặc `00_cheat_connect.rpy`) vào thư mục `game/` của bất kỳ game Ren'Py nào.
   - Tự động nạp động (Dynamic Script Injection) ngay từ lần mở game đầu tiên — **không cần khởi động 2 lần**.
   - Tự động kết nối và kéo bản mới nhất trực tiếp từ GitHub Cloud.

2. **Tự Động Sửa Lỗi Tức Thì (Instant Auto-Healing Engine):**
   - **Tự sửa file Cheat Menu:** Nếu file bị hỏng cú pháp hoặc lỗi cache `.rpyc`, tự động dọn sạch cache và khôi phục bản sạch từ GitHub.
   - **Tự vá biến thiếu (NameError):** Khi game bị lỗi thiếu biến cốt truyện (lỗi kinh điển của dev game), hệ thống tự động khởi tạo biến và ghi vào file `00_cheat_autofix.rpy` để game không bị văng.
   - **Bộ chống văng game (Anti-Crash Interceptor):** Bắt và chặn các lỗi nghiêm trọng, mở Bảng Cứu Hộ bảo vệ tiến trình chơi.

3. **Tự Động Đồng Bộ & Đẩy Lên GitHub (GitHub Cloud Push):**
   - **Tự động đẩy bản sửa lỗi lên GitHub:** Khi chủ sở hữu kiểm tra game và phát hiện/sửa lỗi, hệ thống tự động đẩy file `cheat_menu.rpy` lên kho GitHub thông qua GitHub REST API.
   - Bất cứ khi nào có bản sửa lỗi trên GitHub, toàn bộ người chơi khác khi bật game sẽ tự động nhận bản vá mới nhất!

---

## 🚀 Hướng Dẫn Sử Dụng

### Dành cho Người chơi (Gamers):
1. Tải file `cheat_connect.rpy` từ repository này.
2. Thả trực tiếp vào thư mục `game/` của game Ren'Py.
3. Mở game lên và chơi ngay lập tức (không cần cài đặt gì thêm).

### Dành cho Chủ sở hữu / Modder (Đẩy bản sửa lỗi lên GitHub):
1. Truy cập [GitHub Settings Tokens](https://github.com/settings/tokens) và tạo một **Personal Access Token (PAT)**:
   - Chọn quyền: `repo` (hoặc Repository permissions: `Contents: Read and write`).
2. Lưu token vào file `github_token.txt` trong thư mục `game/` (hoặc thư mục gốc của game).
3. Khi bạn sửa code hoặc game tự sửa lỗi:
   - Nhấn <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F12</kbd> (hoặc bấm nút **🚀 Đẩy bản sửa lỗi lên GitHub** trong Bảng Cứu Hộ).
   - Hệ thống sẽ tự động gọi GitHub API để cập nhật file `cheat_menu.rpy` trực tiếp lên kho!

---

## ⌨️ Phím Tắt Tiện Ích Trong Game

| Phím tắt | Chức năng |
| :--- | :--- |
| <kbd>Tab</kbd> / <kbd>F1</kbd> / <kbd>~</kbd> | Bật / Tắt Menu Cheat Chính |
| <kbd>Shift</kbd> + <kbd>F11</kbd> | **Tải bản mới nhất từ GitHub & Tự sửa lỗi ngay lập tức** |
| <kbd>Shift</kbd> + <kbd>F10</kbd> | **Xóa sạch Cache Bytecode (`.rpyc`) và khởi động lại game sạch sẽ** |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>F12</kbd> | **[Chủ sở hữu] Đẩy bản sửa lỗi trực tiếp lên GitHub qua API** |

---

## 🛠️ Tác Giả & Đóng Góp

* **Tác giả:** [Yudy007](https://github.com/Yudy007)
* **Kho lưu trữ:** [Cheat_Menu_Ren-py](https://github.com/Yudy007/Cheat_Menu_Ren-py)
