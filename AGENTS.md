# HƯỚNG DẪN CHO AGENT SOẠN THẢO NỘI DUNG (CURRICULUM AGENT)

Chào các Agent đồng nghiệp! Để nội dung bài học được hiển thị chính xác trên **Hana Summer LMS**, các bạn cần tuân thủ tuyệt đối cấu trúc file Markdown (.md) dưới đây.

## 1. Cấu trúc định dạng bắt buộc
Mỗi bài học phải được lưu thành một file `.md` riêng biệt với phần **Frontmatter** (nằm giữa hai dấu `---`).

### Các trường dữ liệu (Fields):
- `id`: Mã định danh duy nhất (ví dụ: `ENG_WR_001`, `MATH_005`).
- `subject`: Tên môn học chính xác (chọn từ danh sách bên dưới).
- `title`: Tiêu đề bài học ngắn gọn, hấp dẫn.
- `scheduled_date`: Ngày giao bài (Định dạng: `YYYY-MM-DD`).
- `system_prompt`: Hướng dẫn cụ thể cho AI chấm điểm bài làm này. **Quan trọng:** Yêu cầu AI tìm điểm yếu và gợi ý bài tập tiếp theo.

## 2. Danh sách Môn học (Subjects)
Sử dụng chính xác các tên sau để hệ thống nhận diện đúng màu sắc và icon:
- `English` (Tự động kèm link Flyers.vn & Giọng đọc AI)
- `Tiếng Trung` (Kèm giọng đọc AI)
- `Toán`
- `Lịch sử`
- `Địa lý`
- `Tiếng Việt`
- `Cảm thụ văn học`
- `Science`
- `Đọc sách (English)`
- `Đọc sách (Tiếng Việt)`

## 3. Ví dụ mẫu (ENG_WR_101.md)
\`\`\`markdown
---
id: ENG_WR_101
subject: English
title: My Summer Vacation Plan
scheduled_date: 2026-06-15
system_prompt: >
  Bạn là giáo viên Tiếng Anh. Hãy chấm bài dựa trên ngữ pháp và từ vựng. 
  ĐẶC BIỆT: Phân tích xem Hana còn yếu ở thì nào (quá khứ/tương lai) 
  để gợi ý bài tập củng cố thì đó cho ngày mai. Trả lời bằng tiếng Việt.
---

Chào Hana! Con hãy viết một đoạn văn ngắn (50-70 từ) kể về 
kế hoạch đi chơi hè của con cùng gia đình nhé.
\`\`\`

## 4. Lưu ý quan trọng
- **Nội dung (Body):** Viết ngay sau dấu `---` kết thúc. Có thể dùng Markdown (in đậm, danh sách).
- **Phản hồi của AI:** Hệ thống đã được cấu hình mặc định để tìm điểm yếu, nhưng bạn nên viết thêm yêu cầu cụ thể trong `system_prompt` để AI chấm sát hơn.
