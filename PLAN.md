# HanaApplication - Dashboard Project Plan

**Dự án:** Hana Summer LMS (Learning Management System)  
**Thời gian:** 1/6/2026 – 10/8/2026 (Summer program)  
**Người dùng chính:** Hana (học sinh ~9-10 tuổi) + Bố Mẹ (phụ huynh giám sát)

---

## 1. Mục tiêu tổng thể (từ Blueprint)

Xây dựng **2 Dashboard Web** nhẹ, thân thiện, dễ nhúng:

1. **Hana Dashboard** (Học sinh): Giúp con tập trung, tự giác, hoàn thành nhiệm vụ học tập + xây dựng thói quen sinh hoạt tốt (Pomodoro, uống nước, giới hạn màn hình).
2. **Parents Dashboard** (Phụ huynh): Giám sát real-time, phê duyệt thay đổi cấu hình, theo dõi học thuật chi tiết và hành vi sử dụng thiết bị.

Toàn bộ hệ thống backend dựa trên:
- Google Sheets làm Database trung tâm
- Google Apps Script (GAS) Web App làm API layer
- Telegram Bot làm kênh thông báo + phê duyệt tương tác (Inline Keyboard)
- LLM (qua 9router) chấm bài viết
- SLM cục bộ (local) giám sát hành vi máy tính của con

**Frontend phải cực kỳ nhẹ** (HTML + TailwindCSS + Vanilla JS) theo đúng tinh thần của tài liệu thiết kế, dễ tương thích với Antigravity / no-code tools.

---

## 2. Chi tiết 2 Dashboard

### 2.1. Hana Student Dashboard (Giao diện cho con)

**Phong cách:** Vui tươi, màu sắc ấm áp, khuyến khích, có yếu tố gamification nhẹ, ngôn ngữ thân mật “con”.

**Các khối chính (theo spec trang 9-10):**

| Khối | Mô tả | Tương tác |
|------|-------|---------|
| **Header / Greeting** | "Chào Hana! Hôm nay là [Thứ, dd/mm]. Thời gian dùng máy tính: **45 / 120 phút**" | Hiển thị real-time screen time |
| **Today's Missions** | Danh sách bài tập hôm nay (từ sheet `NganHang_BaiTap`, filter theo `Ngay_Giao`) dạng Card | Click mở → Textarea viết bài + nút "Nộp bài cho cô giáo AI" |
| **Pomodoro Clock** | Đồng hồ đếm ngược 25:00 (lấy từ `CauHinh_SinhHoat.Pomo_ThoiGianTapTrung`). Khi hết → Overlay bắt buộc nghỉ 5 phút + tự động log | Nút Start / Pause / Skip (có giới hạn) |
| **Water Tracker** | Hình ly nước động + thanh tiến độ (mục tiêu 1200ml). Nhắc nhở pop-up mỗi 90 phút | Nút "Con đã uống X ml" → cập nhật progress + log lên `NhatKy_SinhHoat` |
| **Request Change** | Nút "Xin Bố Mẹ cho con thêm giờ" | Form chọn tham số (Screen time / Pomodoro / Water), nhập lý do → Gửi request qua GAS → Telegram cho bố mẹ phê duyệt |

**Yêu cầu UX đặc biệt cho trẻ:**
- Font to, dễ đọc
- Nút lớn, màu rõ ràng
- Animation nhẹ nhàng, không gây phân tâm
- Chế độ "Focus Mode" khi đang làm Pomodoro (ẩn bớt yếu tố khác)

### 2.2. Parents Dashboard (Giao diện cho bố mẹ)

**Phong cách:** Calm, chuyên nghiệp, dữ liệu rõ ràng, cảnh báo nổi bật.

**Các khối chính:**

| Khối | Mô tả | Tương tác |
|------|-------|---------|
| **Live Configuration** | Form chỉnh sửa trực tiếp sheet `CauHinh_SinhHoat` (Pomodoro, giới hạn màn hình, mục tiêu nước, khoảng nhắc nhở) | Lưu → GAS cập nhật sheet → con nhận config mới ở lần sync tiếp theo |
| **Device Monitoring** | Bảng log từ sheet `NhatKy_ThietBi` (SLM analysis). Dòng có `Canh_Bao = TRUE` tô đỏ rực | Filter theo ngày, search, xem chi tiết SLM reason |
| **Academic Portfolio** | Danh sách tất cả bài nộp của Hana từ `NhatKy_HocTap` + `NganHang_BaiTap`. Hiển thị song song: **Bài làm của con** ↔ **Nhận xét + sửa lỗi chi tiết của LLM** | Click xem full, có thể export PDF |
| **Approval Requests** | Lịch sử các yêu cầu thay đổi cấu hình từ con (`YeuCau_Duyet`) + trạng thái | Có thể phê duyệt lại nếu cần (dự phòng) |

---

## 3. Google Sheets Schema (cần tái tạo)

Danh sách sheet tối thiểu để Dashboard hoạt động:

1. `CauHinh_SinhHoat` — Key/Value config (Pomo_*, Nuoc_*, Screen_*)
2. `YeuCau_Duyet` — Request thay đổi config từ con
3. `NganHang_BaiTap` — Đề bài (ID, Môn, Tiêu đề, Nội dung, System Prompt AI, Ngày giao)
4. `NhatKy_HocTap` — Bài làm + AI feedback
5. `NhatKy_SinhHoat` — Uống nước, hoàn thành Pomodoro
6. `NhatKy_ThietBi` — Log giám sát SLM (quan trọng cho Parents dashboard)

(Xem chi tiết trong file PDF gốc `docs/architecture/Hana_Summer_LMS_Architecture_Blueprint.pdf`)

---

## 4. API Contracts (Frontend ↔ GAS)

Frontend sẽ gọi các action sau qua `doGet` / `doPost` của GAS Web App:

**Hana side:**
- `GET ?action=getConfig`
- `GET ?action=getTasks&date=2026-06-05`
- `POST action=submitTask` → {taskId, subject, studentAnswer}
- `POST action=logActivity` → {type: "UongNuoc" | "HoanThanhPomo", value, note}
- `POST action=requestConfigChange` → {paramKey, oldValue, newValue, reason}

**Parents side:**
- `GET ?action=getConfig`
- `POST action=updateConfig` (có thể merge với request trên)
- `GET ?action=getDeviceLogs&from=...&to=...`
- `GET ?action=getAcademicPortfolio`

(Tất cả sẽ được mock chi tiết trong giai đoạn dev)

---

## 5. Tech Stack Đề Xuất (Tôn trọng tinh thần Blueprint)

**Nguyên tắc:** Giữ frontend **cực kỳ nhẹ**, dễ deploy tĩnh hoặc nhúng.

### Option A (Khuyến nghị cho MVP nhanh):
- **HTML + TailwindCSS (CDN)** + Vanilla JS + một số module nhỏ
- 2 file chính: `hana.html` và `parents.html` (hoặc 1 file với role switch cho demo)
- Dùng localStorage + mock data cho phase 1
- Sau này kết nối thật với GAS

**Ưu điểm:** Đúng 100% với spec "gọn nhẹ, không flex/grid nặng", dễ copy-paste vào Antigravity.

### Option B (Cân bằng DX + Production):
- Vite + Tailwind + TypeScript (nhẹ)
- Build ra self-contained HTML (inline CSS/JS) hoặc multi-file sạch
- Dễ maintain hơn khi mở rộng

**Quyết định cuối cùng cần user confirm.**

**Không dùng:** React, Vue, heavy component library, complex state management (ít nhất ở phase đầu).

---

## 6. Cấu trúc thư mục đề xuất

```
HanaApplication/
├── README.md
├── PLAN.md                          # Tài liệu này
├── docs/
│   └── architecture/
│       └── Hana_Summer_LMS_Architecture_Blueprint.pdf
├── frontend/
│   ├── hana/
│   │   ├── index.html               # Dashboard cho Hana
│   │   └── assets/                  # icons, illustrations (nếu có)
│   ├── parents/
│   │   └── index.html               # Dashboard cho Bố Mẹ
│   └── shared/
│       ├── styles.css               # Tailwind build hoặc custom
│       └── utils.js
├── gas-backend/
│   ├── Backend.gs                   # Code Google Apps Script (copy từ PDF + cải tiến)
│   └── README.md
├── sheets-schema/
│   └── create-sheets.md             # Hướng dẫn tạo Google Sheets + sample data
├── scripts/
│   └── agent_monitor.py             # SLM local monitoring agent (từ PDF)
├── .gitignore
└── package.json                     # (nếu chọn Option B - Vite)
```

---

## 7. Các Phase Phát triển (Đề xuất)

**Phase 0 – Foundation (1-2 ngày)**
- Khởi tạo repo + PLAN.md + copy PDF
- Tạo Google Sheets mẫu + seed data
- Deploy GAS Web App stub (mock data)

**Phase 1 – Hana Dashboard MVP (3-5 ngày)**
- Giao diện thân thiện cho con
- Pomodoro hoạt động tốt + force break
- Water tracker + reminder popup
- Today's Missions + submit flow (mock AI response)
- Nút request change config (gửi vào local log hoặc mock)

**Phase 2 – Parents Dashboard MVP**
- Config editor live
- Device monitoring table (với màu warning)
- Academic portfolio view

**Phase 3 – Kết nối thật**
- Thay mock bằng gọi GAS thật
- Telegram approval flow end-to-end
- Thêm localStorage persistence + sync

**Phase 4 – Polish + SLM Agent**
- Cải thiện UX cho trẻ
- Responsive + dark/light theo vai trò
- Hoàn thiện script agent_monitor.py + hướng dẫn chạy nền

**Phase 5 – Deployment & Documentation**
- Hướng dẫn deploy tĩnh (GitHub Pages / Cloudflare / Vercel)
- Hướng dẫn setup đầy đủ (Sheets + GAS + Telegram + 9router)

---

## 8. Rủi ro & Giả định quan trọng

- Google Apps Script quota (đặc biệt khi con nộp bài nhiều)
- SLM local (Ollama) có thể nặng máy con → cần tối ưu prompt + interval 2 phút như spec
- Trẻ có thể cố tình tắt agent → cần giải pháp chạy nền tốt (Task Scheduler / launchd + ẩn)
- Bảo mật: Web App GAS để `Anyone, even anonymous` → cần cơ chế xác thực đơn giản (secret token hoặc chỉ cho phép từ domain cụ thể)

---

## 9. Next Steps (Cần xác nhận từ anh)

1. **Tech stack** cho frontend: Option A (pure HTML+CDN Tailwind) hay Option B (Vite + Tailwind)?
2. Ưu tiên xây **Hana Dashboard trước** hay làm **cả 2 song song**?
3. Có cần hỗ trợ **offline-first** (localStorage sync khi có mạng) ngay từ đầu không?
4. Có muốn tích hợp **Calendar/Tasks Google** ngay phase 1 không (theo mention trong PDF)?
5. Ngôn ngữ UI: 100% tiếng Việt, hay có song ngữ?

---

**Tài liệu tham khảo chính:**  
`docs/architecture/Hana_Summer_LMS_Architecture_Blueprint.pdf` (10 trang, WeasyPrint)

---

*Plan này được tạo dựa trên việc đọc toàn bộ 10 trang blueprint ngày 31/05/2026.*
