# Hướng dẫn Tạo Supabase Project cho Hana Summer LMS

## 1. Tạo Supabase Project Mới

1. Truy cập: [https://supabase.com](https://supabase.com)
2. Đăng nhập bằng GitHub (khuyến nghị) hoặc Email.
3. Nhấn nút **"New Project"**.

### Cài đặt khuyến nghị:

| Trường                  | Giá trị gợi ý                          | Ghi chú |
|-------------------------|----------------------------------------|-------|
| **Name**                | `hana-summer-lms`                      | Tên project |
| **Database Password**   | Tạo password mạnh (lưu lại thật kỹ)    | Rất quan trọng |
| **Region**              | **Singapore** (ap-southeast-1)         | Gần Việt Nam nhất, latency thấp |
| **Plan**                | Free (Starter)                         | Đủ dùng cho dự án hè |

Sau khi tạo xong, chờ khoảng 1-2 phút để database khởi tạo.

---

## 2. Lấy thông tin kết nối (quan trọng)

Sau khi project sẵn sàng, vào **Project Settings** → **API**:

Copy 3 giá trị sau và lưu tạm (sau này sẽ để vào file `.env` hoặc hardcode trong phase dev):

- **Project URL** (dạng: `https://xxxxxxxxxxxx.supabase.co`)
- **anon public** key (bắt đầu bằng `eyJ...`)
- **service_role** key (chỉ dùng cho server-side, cẩn thận)

---

## 3. Bật các tính năng cần thiết

Vào **Database** → **Extensions**, bật các extension sau (nếu chưa có):

- `uuid-ossp` (đã bật mặc định thường)
- `pgcrypto`

Vào **Authentication** → **Providers**:
- Email (bật)
- Có thể tắt tất cả provider khác để giữ đơn giản

---

## 4. Tạo Schema (Bước tiếp theo)

Sau khi tạo project xong, anh copy toàn bộ nội dung file sau và chạy trong **SQL Editor** của Supabase:

→ [supabase/schema.sql](../supabase/schema.sql)

File này đã được thiết kế theo hướng **đơn giản hóa tối đa** + hỗ trợ **offline-first**.

---

## 5. Row Level Security (RLS) - Đơn giản hóa

Vì muốn đơn giản hóa tối đa, giai đoạn đầu chúng ta sẽ:

- **Tắt RLS** tạm thời trên một số bảng (hoặc chỉ bật cơ bản).
- Sử dụng `service_role` key cho backend script (nếu có).
- Frontend dùng `anon` key + thêm một lớp bảo vệ đơn giản (secret token hoặc password).

Sau này nếu cần bảo mật cao hơn thì bật RLS chi tiết.

---

## 6. Bước tiếp theo sau khi tạo Supabase

Khi anh đã:
- [x] Tạo project xong
- [x] Copy `Project URL` + `anon key`
- [x] Chạy file `schema.sql` thành công

Hãy báo mình biết. Lúc đó mình sẽ:
- Tạo file cấu hình kết nối
- Bắt đầu viết 2 file dashboard (`hana.html` + `parents.html`)
- Thiết kế cơ chế offline + sync queue

---

**Lưu ý quan trọng:**
- Password database Supabase **không được để lộ**.
- `service_role` key **không được để trong frontend**.
- Region Singapore giúp giảm độ trễ khi con dùng ở Việt Nam.

Nếu gặp lỗi gì trong quá trình tạo project, chụp màn hình hoặc copy lỗi gửi mình.
