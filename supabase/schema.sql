-- ============================================================
-- HANA SUMMER LMS - Supabase Schema (Đơn giản hóa tối đa)
-- ============================================================
-- Phù hợp với quyết định: Hybrid + Supabase làm trung tâm + Offline-first
-- ============================================================

-- Bật extension cần thiết
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================
-- ENUMS
-- ============================================================
CREATE TYPE task_status AS ENUM ('pending', 'in_progress', 'submitted', 'graded');
CREATE TYPE activity_type AS ENUM ('pomodoro_complete', 'water_intake', 'screen_time_log', 'break_taken');
CREATE TYPE approval_status AS ENUM ('pending', 'approved', 'rejected');
CREATE TYPE device_warning_level AS ENUM ('ok', 'warning', 'critical');

-- ============================================================
-- BẢNG: profiles (Người dùng - Hana + Bố Mẹ)
-- ============================================================
CREATE TABLE profiles (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  role TEXT NOT NULL CHECK (role IN ('student', 'parent')),
  display_name TEXT NOT NULL,
  email TEXT,
  avatar_url TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE profiles IS 'Hana (student) và Bố Mẹ (parent)';

-- ============================================================
-- BẢNG: daily_configs (Cấu hình sinh hoạt - sync từ Google Sheets)
-- ============================================================
CREATE TABLE daily_configs (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  config_date DATE NOT NULL DEFAULT CURRENT_DATE,
  pomo_focus_minutes INTEGER DEFAULT 25,
  pomo_break_minutes INTEGER DEFAULT 5,
  water_goal_ml INTEGER DEFAULT 1200,
  water_reminder_interval_minutes INTEGER DEFAULT 90,
  screen_limit_minutes INTEGER DEFAULT 120,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(config_date)
);

COMMENT ON TABLE daily_configs IS 'Config sinh hoạt theo ngày. Bố mẹ chỉnh qua Google Sheets hoặc dashboard';

-- ============================================================
-- BẢNG: tasks (Nhiệm vụ học tập - sync từ Google Sheets)
-- ============================================================
CREATE TABLE tasks (
  id TEXT PRIMARY KEY,                    -- Giữ ID từ Google Sheets (ENG_WR_001, ...)
  subject TEXT NOT NULL,                  -- Tiếng Anh / Tiếng Việt
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  system_prompt TEXT,
  scheduled_date DATE NOT NULL,
  status task_status DEFAULT 'pending',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE tasks IS 'Ngân hàng đề bài. Bố mẹ dán từ NotebookLM vào Google Sheets → sync vào đây';

-- ============================================================
-- BẢNG: submissions (Bài làm của Hana + Feedback AI)
-- ============================================================
CREATE TABLE submissions (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  task_id TEXT REFERENCES tasks(id),
  student_answer TEXT NOT NULL,
  ai_feedback TEXT,
  ai_score INTEGER,                       -- 0-100
  ai_model TEXT,                          -- ví dụ: claude-3.5-sonnet, llama-3.1-etc
  submitted_at TIMESTAMPTZ DEFAULT NOW(),
  synced_at TIMESTAMPTZ,                  -- Dùng cho offline sync
  is_synced BOOLEAN DEFAULT FALSE
);

COMMENT ON TABLE submissions IS 'Bài làm + nhận xét AI. Bảng này cần mạnh nên để Supabase';

-- ============================================================
-- BẢNG: daily_activities (Nhật ký sinh hoạt - Uống nước, Pomodoro...)
-- ============================================================
CREATE TABLE daily_activities (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  activity_date DATE NOT NULL DEFAULT CURRENT_DATE,
  activity_type activity_type NOT NULL,
  value NUMERIC,                          -- ml nước, số phút, ...
  note TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  is_synced BOOLEAN DEFAULT FALSE,
  synced_at TIMESTAMPTZ
);

COMMENT ON TABLE daily_activities IS 'Log Pomodoro, uống nước, screen time. Hỗ trợ offline sync';

-- ============================================================
-- BẢNG: device_logs (Log giám sát từ SLM Agent - local)
-- ============================================================
CREATE TABLE device_logs (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  timestamp TIMESTAMPTZ NOT NULL,
  active_window TEXT,
  running_processes TEXT[],
  slm_report TEXT,
  warning_level device_warning_level DEFAULT 'ok',
  is_synced BOOLEAN DEFAULT FALSE,
  synced_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE device_logs IS 'Log từ agent SLM chạy local trên máy con. Rất nhiều dữ liệu → cần Supabase mạnh';

-- ============================================================
-- BẢNG: approval_requests (Xin thay đổi config - gửi qua Telegram)
-- ============================================================
CREATE TABLE approval_requests (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  param_key TEXT NOT NULL,                -- Ví dụ: Screen_GioiHanMoiNgay
  old_value TEXT NOT NULL,
  new_value TEXT NOT NULL,
  reason TEXT,
  status approval_status DEFAULT 'pending',
  requested_at TIMESTAMPTZ DEFAULT NOW(),
  responded_at TIMESTAMPTZ,
  responded_by TEXT,                      -- email hoặc tên bố mẹ
  telegram_message_id BIGINT            -- Dùng để edit message sau khi approve/reject
);

COMMENT ON TABLE approval_requests IS 'Request thay đổi config từ Hana. Gửi qua Telegram để bố mẹ duyệt';

-- ============================================================
-- BẢNG: schedules (Lịch + Checklist - hỗ trợ Calendar)
-- ============================================================
CREATE TABLE schedules (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  schedule_date DATE NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  is_completed BOOLEAN DEFAULT FALSE,
  completed_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

COMMENT ON TABLE schedules IS 'Lịch hàng ngày/tuần/tháng. Hana thấy đơn giản, Bố Mẹ thấy tổng quan';

-- ============================================================
-- BẢNG: sync_queue (Hỗ trợ Offline-first)
-- ============================================================
CREATE TABLE sync_queue (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  table_name TEXT NOT NULL,
  record_id TEXT NOT NULL,
  action TEXT NOT NULL CHECK (action IN ('insert', 'update', 'delete')),
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  processed_at TIMESTAMPTZ,
  error TEXT
);

COMMENT ON TABLE sync_queue IS 'Queue để frontend lưu khi offline, sau sync lên Supabase';

-- ============================================================
-- INDEXES (Tối ưu query thường dùng)
-- ============================================================
CREATE INDEX idx_tasks_scheduled_date ON tasks(scheduled_date);
CREATE INDEX idx_submissions_task_id ON submissions(task_id);
CREATE INDEX idx_daily_activities_date ON daily_activities(activity_date);
CREATE INDEX idx_device_logs_timestamp ON device_logs(timestamp DESC);
CREATE INDEX idx_approval_requests_status ON approval_requests(status);
CREATE INDEX idx_schedules_date ON schedules(schedule_date);

-- ============================================================
-- ROW LEVEL SECURITY (Tạm thời đơn giản hóa)
-- ============================================================
-- Giai đoạn đầu: Tắt RLS để dev nhanh.
-- Sau này có thể bật lại với policy rõ ràng cho student vs parent.

ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_configs ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE device_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE approval_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE schedules ENABLE ROW LEVEL SECURITY;

-- Policy đơn giản cho phase dev (sau này refine)
-- Tạm cho phép anon đọc/ghi (sẽ thay bằng logic app sau)
CREATE POLICY "Allow all for development" ON daily_configs FOR ALL USING (true);
CREATE POLICY "Allow all for development" ON tasks FOR ALL USING (true);
CREATE POLICY "Allow all for development" ON submissions FOR ALL USING (true);
CREATE POLICY "Allow all for development" ON daily_activities FOR ALL USING (true);
CREATE POLICY "Allow all for development" ON device_logs FOR ALL USING (true);
CREATE POLICY "Allow all for development" ON approval_requests FOR ALL USING (true);
CREATE POLICY "Allow all for development" ON schedules FOR ALL USING (true);

-- ============================================================
-- SEED DATA (Dữ liệu mẫu ban đầu)
-- ============================================================
INSERT INTO daily_configs (config_date, pomo_focus_minutes, pomo_break_minutes, water_goal_ml, screen_limit_minutes)
VALUES (CURRENT_DATE, 25, 5, 1200, 120);

INSERT INTO profiles (role, display_name) VALUES 
('student', 'Hana'),
('parent', 'Bố Mẹ');

-- ============================================================
-- NOTES
-- ============================================================
-- 1. Bảng daily_configs và tasks sẽ được sync từ Google Sheets qua GAS (giữ tối thiểu).
-- 2. submissions, daily_activities, device_logs, schedules là dữ liệu chính → Supabase quản lý.
-- 3. sync_queue dùng cho cơ chế offline-first ở frontend.
-- 4. Sau này có thể thêm trigger để tự động cập nhật updated_at.
