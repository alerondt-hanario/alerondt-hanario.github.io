# Hana Summer LMS - GitHub Pages

This folder contains the static files ready to deploy to GitHub Pages.

## Cách triển khai lên hana-summer-lms.github.io

### Cách 1: Tạo repo riêng (Khuyến nghị - URL đẹp nhất)

1. Tạo một repository mới trên GitHub với tên chính xác:
   ```
   hana-summer-lms.github.io
   ```
   (Dưới tài khoản `alerondt-hanario`)

2. Copy toàn bộ nội dung thư mục `site/` này vào repo mới.

3. Push lên branch `main`.

4. Vào repo → **Settings → Pages**:
   - Source: **Deploy from a branch**
   - Branch: `main`
   - Folder: `/ (root)`
   - Save

5. Sau vài phút, trang sẽ live tại:
   **https://hana-summer-lms.github.io**

### Cách 2: Deploy từ repo hiện tại (hanaapp)

Nếu bạn muốn giữ nguyên repo `hanaapp`:

1. Vào repo `hanaapp` → **Settings → Pages**
2. Source: `main` branch
3. Folder: `/site`
4. URL sẽ là: `https://alerondt-hanario.github.io/hanaapp/site/`

---

## Cấu trúc thư mục

```
site/
├── index.html          ← Landing page (chọn dashboard)
├── hana.html           ← Dashboard cho con
├── parents.html        ← Dashboard cho bố mẹ
└── .nojekyll
```

## Lưu ý

- Hai dashboard kết nối trực tiếp đến Supabase (client-side), nên hoạt động bình thường khi deploy.
- Hỗ trợ offline tốt.
- Không cần build step.

---

**Tạo repo `hana-summer-lms.github.io` là cách sạch và chuyên nghiệp nhất.**
