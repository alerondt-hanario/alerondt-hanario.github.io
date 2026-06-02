# NHIỆM VỤ CHO PHIÊN LÀM VIỆC TIẾP THEO

Anh đã chuẩn bị xong cấu trúc bài học và giao diện cho Hana. Khi anh có **Supabase Token (Service Role Key)**, hãy thực hiện các bước sau để kích hoạt hệ thống:

## 1. Cập nhật Token
- Mở file `frontend/hana.html` và tìm biến `SUPABASE_ANON_KEY`. Thay thế giá trị `***` bằng Token anh có.
- (Tương tự cho `parents.html` nếu cần).

## 2. Đồng bộ bài học (Sync Curriculum)
- Chạy lệnh sau trong terminal để đẩy toàn bộ bài học từ thư mục `curriculum/` lên database:
  ```bash
  python3 scripts/sync_curriculum.py
  ```

## 3. Kiểm tra kết quả
- Mở `frontend/hana.html` trên trình duyệt.
- Kiểm tra xem danh sách bài học (English, Cảm thụ văn học, ...) đã hiện ra ở cột bên trái chưa.
- Thử chọn một bài và nhấn **START** để xem bộ đếm giờ và đề bài.

---
*Ghi chú: Em đã cài đặt sẵn môi trường Python và các thư viện cần thiết (`supabase`, `python-frontmatter`).*
