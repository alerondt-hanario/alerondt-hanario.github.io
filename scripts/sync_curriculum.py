import os
import frontmatter
from supabase import create_client, Client
import subprocess

# Cấu hình Supabase
SUPABASE_URL = "https://oytgbhytkddjlygafxjf.supabase.co"
CURRICULUM_DIR = "/media/vpsg16gb/Workspace1/HanaApplication/curriculum"
HTML_FILE = "/media/vpsg16gb/Workspace1/HanaApplication/frontend/hana.html"

def get_supabase_key():
    try:
        # Cố gắng trích xuất key từ file HTML để đảm bảo luôn dùng key mới nhất
        cmd = f"sed -n \"s/.*const SUPABASE_ANON_KEY = '\\(.*\\)';.*/\\1/p\" {HTML_FILE}"
        key = subprocess.check_output(cmd, shell=True).decode().strip()
        if key.startswith('eyJ'):
            return key
    except:
        pass
    # Fallback key (cần cập nhật thủ công nếu key trên lỗi)
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95dGdiaHl0a2Rkamx5Z2FmeGpmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAyMzUyNjIsImV4cCI6MjA5NTgxMTI2Mn0.ez0NvMJsZKrjRp5d71LxbPUfYjermDw2FoiC7jcH4lY"

def sync_curriculum():
    key = get_supabase_key()
    supabase: Client = create_client(SUPABASE_URL, key)
    
    if not os.path.exists(CURRICULUM_DIR):
        print(f"Lỗi: Thư mục {CURRICULUM_DIR} không tồn tại.")
        return

    files = [f for f in os.listdir(CURRICULUM_DIR) if f.endswith('.md')]
    if not files:
        print("Không tìm thấy file .md nào.")
        return

    print(f"Tìm thấy {len(files)} bài học để đồng bộ.")
    
    for filename in files:
        filepath = os.path.join(CURRICULUM_DIR, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
                task_id = post.get('id') or os.path.splitext(filename)[0]
                
                task_data = {
                    "id": task_id,
                    "subject": post.get('subject', 'Chưa phân loại'),
                    "title": post.get('title', 'Không có tiêu đề'),
                    "content": post.content.strip(),
                    "system_prompt": post.get('system_prompt', ''),
                    "scheduled_date": str(post.get('scheduled_date', ''))
                }
                
                print(f"Đang đồng bộ: {task_data['title']} ({task_id})...")
                supabase.table("tasks").upsert(task_data).execute()
                print(f"Thành công: {task_id}")
        except Exception as e:
            print(f"Lỗi {filename}: {str(e)}")

if __name__ == "__main__":
    sync_curriculum()
