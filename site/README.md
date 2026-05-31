# Hana Summer LMS - GitHub Pages

This folder contains the static files ready to deploy to GitHub Pages.

## Current Deployment

**Live URL:**

**https://alerondt-hanario.github.io/hana-summer-lms.github.io**

- Full site: https://alerondt-hanario.github.io/hana-summer-lms.github.io
- Hana Dashboard: .../hana.html
- Parents Dashboard: .../parents.html

**Important:** The clean domain `https://hana-summer-lms.github.io` is not available because the GitHub username is `alerondt-hanario`. GitHub Pages only gives the short form when the username matches the repo name.

### How to update / redeploy

1. Make sure you're working in the repo `alerondt-hanario/hana-summer-lms.github.io`

2. Copy the entire contents of this `site/` folder into the root of that repo.

3. Commit and push to the `main` branch.

4. GitHub Pages will automatically update from the `main` branch (Source = `/ (root)`).

No custom domain is currently set.

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
