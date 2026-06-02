import os
import requests
import json
from supabase import create_client, Client

# Cấu hình
SUPABASE_URL = "https://oytgbhytkddjlygafxjf.supabase.co"
# Sử dụng Service Role Key để có quyền update bài làm
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "****************************************************************************************************************************************************************************************************************")
# API Gateway cho LLM (ví dụ 9router hoặc OpenAI/Claude trực tiếp)
LLM_API_URL = "https://api.9router.ai/v1/chat/completions"
LLM_API_KEY = os.environ.get("LLM_API_KEY", "")

def get_ai_feedback(subject, title, content, student_answer, system_prompt):
    """Gọi LLM để chấm điểm và nhận xét bài làm"""
    if not LLM_API_KEY:
        return "Lỗi: Chưa cấu hình API Key cho AI. Vui lòng kiểm tra LLM_API_KEY.", 0
        
    prompt = f"""
Môn học: {subject}
Chủ đề: {title}
Đề bài: {content}

Bài làm của học sinh (Hana):
{student_answer}

HÃY CHẤM ĐIỂM DỰA TRÊN YÊU CẦU SAU:
{system_prompt}

---------------------------------------------------------------------------
YÊU CẦU QUAN TRỌNG (ÁP DỤNG CHO TẤT CẢ CÁC MÔN):
1. Phân tích chi tiết bài làm để tìm ra những điểm/kỹ năng Hana còn yếu hoặc cần cải thiện.
2. Đưa ra gợi ý cụ thể cho các bài tập tiếp theo để giúp con khắc phục những điểm yếu này.
3. Lời phê cần chân thành, mang tính khuyến khích và viết bằng tiếng Việt.
4. Cấu trúc câu trả lời:
   - [NHẬN XÉT CHI TIẾT]
   - [ĐIỂM CẦN CẢI THIỆN & GỢI Ý BÀI SAU]
   - [SCORE: XX/100] (Hãy trả về điểm số ở dòng cuối cùng theo đúng định dạng này)
"""

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "claude-3-5-sonnet-20240620", 
        "messages": [
            {"role": "system", "content": "Bạn là một giáo viên tận tâm, chuyên gia trong việc phát hiện lỗ hổng kiến thức và định hướng lộ trình học tập cá nhân hóa cho học sinh tiểu học."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(LLM_API_URL, headers=headers, json=data)
        result = response.json()
        full_response = result['choices'][0]['message']['content']
        
        # Trích xuất điểm số từ format [SCORE: XX/100]
        score = 0
        try:
            import re
            score_match = re.search(r"SCORE:\s*(\d+)", full_response, re.IGNORECASE)
            if score_match:
                score = int(score_match.group(1))
            else:
                # Fallback nếu AI quên định dạng
                score = 80 
        except:
            score = 80
            
        return full_response, score
    except Exception as e:
        return f"Lỗi gọi AI: {str(e)}", 0

def process_submissions():
    """Kiểm tra và chấm điểm các bài nộp chưa có feedback"""
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    # Lấy các bài nộp chưa có feedback
    response = supabase.table("submissions").select("*, tasks(*)").is_("ai_feedback", "null").execute()
    submissions = response.data
    
    if not submissions:
        print("Không có bài nộp mới cần chấm điểm.")
        return

    print(f"Tìm thấy {len(submissions)} bài nộp mới.")

    for sub in submissions:
        task = sub['tasks']
        print(f"Đang phân tích bài: {task['title']} của Hana...")
        
        feedback, score = get_ai_feedback(
            task['subject'],
            task['title'],
            task['content'],
            sub['student_answer'],
            task['system_prompt']
        )
        
        # Cập nhật feedback vào database
        supabase.table("submissions").update({
            "ai_feedback": feedback,
            "ai_score": score,
            "ai_model": "claude-3.5-sonnet"
        }).eq("id", sub['id']).execute()
        
        # Cập nhật trạng thái task thành 'graded'
        supabase.table("tasks").update({"status": "graded"}).eq("id", sub['task_id']).execute()
        
        print(f"Đã chấm xong bài {sub['id']} - Điểm: {score}. Đã lưu gợi ý cải thiện.")

if __name__ == "__main__":
    process_submissions()
