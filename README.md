# 🎮 Cheat Menu & Auto-Repair Mod Cho Game Ren'Py

> **Universal All-in-One Mod (v3.1):** Bộ công cụ Cheat Menu đa ngôn ngữ và Cứu hộ tự động sửa lỗi kịch bản dành cho mọi game Ren'Py (tương thích Ren'Py 6, Ren'Py 7 - Python 2.7 và Ren'Py 8, 9 - Python 3.x).

---

## ✨ Điểm Nổi Bật

### 1. 🌐 Hỗ Trợ Đa Ngôn Ngữ (Multi-Language Support)
- **Mặc định là Tiếng Anh (English):** Giao diện chuẩn quốc tế, hiển thị rõ ràng và tương thích tối đa với mọi tựa game.
- **Chuyển đổi sang Tiếng Việt dễ dàng:** Người chơi có thể chuyển đổi ngôn ngữ bất kỳ lúc nào thông qua menu danh sách chọn ngôn ngữ (`[🌐 Language ▼]`) ở góc trên màn hình hoặc thẻ Cài đặt trong tab *Unlocks & System*.
- **Ghi nhớ tự động:** Lựa chọn ngôn ngữ được lưu tự động vào `persistent` của game, không bị mất đi khi khởi động lại game hay chuyển cảnh.

### 2. ⚡ Kết Nối 1-Click (1-Click Cloud Connector)
- Chỉ cần thả duy nhất file `cheat_connect.rpy` vào thư mục `game/` của bất kỳ game Ren'Py nào.
- **Nạp động tức thì (Dynamic Script Injection):** Cheat Menu được tự động tải về từ GitHub và nạp thẳng vào engine ngay trong vòng lặp nạp kịch bản đầu tiên

### 3. 🛡️ Tự Động Sửa Lỗi Tức Thì (Instant Auto-Healing Engine)
- **Tự sửa file Cheat Menu:** Nếu script bị xung đột cú pháp hoặc lỗi cache bytecode (`.rpyc`), hệ thống tự động dọn sạch cache và khôi phục bản sạch chuẩn từ GitHub Cloud.
- **Tự vá biến thiếu (NameError):** Khi game bị lỗi thiếu biến cốt truyện (lỗi lập trình phổ biến của dev game), hệ thống tự động khởi tạo biến tương ứng và lưu vào `cheat_autofix.rpy` giúp game không bị văng.
- **Bộ chống văng game (Anti-Crash Interceptor):** Bắt và cô lập các lỗi nghiêm trọng trong lúc chơi, tự động ghi log vào `cheat_crash_log.txt` và bảo vệ tiến trình chơi của bạn an toàn.

### 4. 🤝 Đóng Góp & Gửi Bản Vá Cho Chủ Sở Hữu (Community Patch System)
- **Cộng đồng cùng đóng góp:** Thay vì chỉ có một người bảo trì, bất kỳ người chơi hoặc lập trình viên nào phát hiện lỗi, tối ưu tính năng hay tạo ra bản sửa lỗi mới đều có thể **gửi file bản vá (patch file / script `.rpy` sửa đổi)** cho chủ sở hữu repository.
- **Cập nhật nhanh chóng:** Người chơi có thể gửi bản vá thông qua:
  - Tạo **Pull Request (PR)** trên GitHub.
  - Tạo **Issue** đính kèm file bản vá hoặc mô tả đoạn code sửa lỗi.
  - Gửi trực tiếp file bản vá cho chủ sở hữu repository.
- **Phát hành tự động đến toàn bộ người chơi:** Khi chủ sở hữu kiểm tra, chấp thuận và gộp (merge) bản vá lên kho lưu trữ GitHub Cloud, **toàn bộ cộng đồng người chơi khác khi mở game (hoặc bấm `Shift + F11`) sẽ tự động nhận được bản vá mới nhất** từ đám mây!

### 5. 🔄 Công Cụ Đồng Bộ Hàng Loạt Ngoại Tuyến (Offline Batch Sync Tools)
- Đi kèm bộ công cụ tự động hóa với tên file chuẩn Tiếng Anh: `Update_Cheat_Menu.bat` và `Update_Cheat_Menu.ps1`.
- Quét nhanh và đồng bộ file Cheat Menu mới nhất tới hàng loạt thư mục game Ren'Py trên máy tính chỉ với 1 thao tác kéo thả hoặc click chuột.

---

## 📁 Cấu Trúc File Trong Dự Án (All-English File Names)

| Tên file | Mô tả chức năng |
| :--- | :--- |
| `font.ttf` | Phông chữ chuẩn Unicode hiển thị mượt mà, tối ưu hóa giao diện Cheat Menu độc lập và sắc nét cho mọi tựa game. |
| `cheat_connect.rpy` | File kết nối GitHub Cloud, tự tải và nạp động Cheat Menu ngay lần mở đầu tiên. |
| `cheat_menu.rpy` | File mã nguồn lõi của Cheat Menu, giao diện Đa ngôn ngữ (English / Tiếng Việt), quản trị biến và bộ cứu hộ sự cố. |
| `Update_Cheat_Menu.bat` | Script Batch click đúp hoặc kéo-thả thư mục game vào để tự động đồng bộ Cheat Menu. |
| `Update_Cheat_Menu.ps1` | Script PowerShell tự động dò tìm toàn bộ thư mục `game/` trong máy và cập nhật bản mới nhất. |

---

## 🚀 Hướng Dẫn Sử Dụng

### Dành Cho Người Chơi (Gamers)
1. Tải file `cheat_connect.rpy` từ repository này.
2. Thả trực tiếp file vào thư mục `game/` của tựa game Ren'Py bạn muốn cheat.
3. Mở game lên và trải nghiệm ngay lập tức.
4. Để đổi sang Tiếng Việt: Bấm mở Cheat Menu, nhấn vào nút `[🌐 Language ▼]` ở thanh tiêu đề và chọn **Tiếng Việt**.

### Dành Cho Người Muốn Đóng Góp Bản Vá (Contributors)
1. Fork repository này về tài khoản GitHub của bạn hoặc tải mã nguồn về chỉnh sửa.
2. Tiến hành thử nghiệm, sửa lỗi hoặc thêm tính năng trong `cheat_menu.rpy`.
3. Gửi bản vá cho chủ sở hữu repository:
   - **Cách 1 (Khuyên dùng):** Tạo **Pull Request** trên GitHub mô tả chi tiết các thay đổi.
   - **Cách 2:** Mở một **Issue** mới, đính kèm file bản vá (`.rpy` hoặc patch diff) cùng thông tin lỗi được khắc phục.
4. Sau khi chủ sở hữu phê duyệt và gộp vào nhánh chính, tất cả người chơi trên toàn thế giới sẽ tự động nhận được cập nhật khi bật game!

---

## ⌨️ Bảng Phím Tắt Tiện Ích Trong Game

| Phím tắt | Chức năng |
| :--- | :--- |
| <kbd>Tab</kbd> / <kbd>F1</kbd> / <kbd>~</kbd> / <kbd>Shift</kbd> + <kbd>C</kbd> | Bật / Tắt Bảng điều khiển Cheat chính |
| <kbd>*</kbd> (Numpad) | Thu gọn / Mở rộng Thanh nổi bên phải màn hình |
| <kbd>Alt</kbd> + <kbd>*</kbd> | Bật / Tắt ẩn hoàn toàn Thanh nổi bên phải |
| <kbd>H</kbd> | Ẩn khung thoại (Hide UI) để xem trọn hình nền, CG |
| <kbd>S</kbd> | Bật / Tắt Tua nhanh không giới hạn (Force Skip Unseen Text) |
| <kbd>A</kbd> | Bật / Tắt Tự động đọc thoại (Auto-Forward) |
| <kbd>L</kbd> | Mở Nhật ký thoại & Điểm quay lại tương tác (History Log) |
| <kbd>Shift</kbd> + <kbd>O</kbd> | Mở Developer Console gõ lệnh Python trực tiếp của Ren'Py |
| <kbd>Shift</kbd> + <kbd>F11</kbd> | **Tải bản mới nhất từ GitHub Cloud & Tự động sửa lỗi ngay lập tức** |
| <kbd>Shift</kbd> + <kbd>F10</kbd> | **Xóa sạch Cache Bytecode (`.rpyc`) và khởi động lại game sạch sẽ** |
