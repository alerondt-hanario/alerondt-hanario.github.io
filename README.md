# HanaApplication

**Hana Summer LMS** — Hệ thống Quản lý Học tập Mùa Hè cho con gái (1/6 – 10/8/2026)

Dashboard nhẹ, thân thiện dành cho **Hana (học sinh)** và **Bố Mẹ (phụ huynh giám sát)**, được thiết kế theo đúng bản đặc tả kỹ thuật trong tài liệu kiến trúc.

## 🎯 Mục tiêu

- Giúp Hana xây dựng thói quen học tập & sinh hoạt tốt trong hè (Pomodoro, uống nước, giới hạn màn hình).
- Hỗ trợ chấm bài viết tự động bằng LLM (Tiếng Anh + Tiếng Việt).
- Cung cấp công cụ giám sát hành vi máy tính + phê duyệt real-time cho bố mẹ qua Telegram.

## 📁 Cấu trúc hiện tại

```
HanaApplication/
├── docs/architecture/
│   └── Hana_Summer_LMS_Architecture_Blueprint.pdf   # Bản thiết kế gốc (10 trang)
├── PLAN.md                                          # Kế hoạch chi tiết xây Dashboard
├── frontend/
│   ├── hana/                                        # Dashboard cho con
│   └── parents/                                     # Dashboard cho bố mẹ
├── gas-backend/                                     # Google Apps Script
├── sheets-schema/                                   # Hướng dẫn tạo dữ liệu Google Sheets
└── scripts/                                         # Local monitoring agent (SLM)
```

## 📖 Tài liệu

- [PLAN.md](./PLAN.md) — Kế hoạch phát triển Dashboard chi tiết (đọc trước)
- Bản thiết kế kiến trúc gốc: `docs/architecture/Hana_Summer_LMS_Architecture_Blueprint.pdf`

## 🚀 Trạng thái hiện tại (31/05/2026)

- [x] Đã đọc toàn bộ 10 trang blueprint
- [x] **Kiến trúc cuối cùng đã chốt**: Hybrid (Supabase làm trung tâm + Google Sheets tối thiểu) + Offline-first + Làm song song 2 dashboards
- [x] Tạo `frontend/hana.html` và `frontend/parents.html` (Pure HTML + Tailwind CDN — Option A)
- [x] Tạo schema Supabase + hướng dẫn setup chi tiết
- [x] Đã commit + push commit đầu tiên

**Để xem demo ngay:**
```bash
open frontend/hana.html
open frontend/parents.html
```

## Yêu cầu tiếp theo (từ anh)

Mở [PLAN.md](./PLAN.md) và trả lời 5 câu hỏi ở phần cuối để mình bắt đầu xây dựng ngay.

---

**Stack mục tiêu (theo blueprint):**  
Google Sheets + Google Apps Script + Telegram + HTML/Tailwind/Vanilla JS (siêu nhẹ) + Local SLM (Ollama)

Dự án được xây dựng để dễ duy trì, dễ nhúng, và phù hợp với triết lý "hybrid serverless" tối ưu hệ sinh thái Google.
