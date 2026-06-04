import sys
import subprocess
from supabase import create_client, Client

SUPABASE_URL = "https://oytgbhytkddjlygafxjf.supabase.co"
HTML_FILE = "/media/vpsg16gb/Workspace1/HanaApplication/frontend/index.html"

def get_supabase_key():
    try:
        cmd = f"sed -n \"s/.*const SUPABASE_ANON_KEY = '\\(.*\\)';.*/\\1/p\" {HTML_FILE}"
        key = subprocess.check_output(cmd, shell=True).decode().strip()
        if key.startswith('eyJ'):
            return key
    except:
        pass
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95dGdiaHl0a2Rkamx5Z2FmeGpmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAyMzUyNjIsImV4cCI6MjA5NTgxMTI2Mn0.ez0NvMJsZKrjRp5d71LxbPUfYjermDw2FoiC7jcH4lY"

def reset_db():
    key = get_supabase_key()
    supabase: Client = create_client(SUPABASE_URL, key)

    print("1. Deleting all submissions...")
    try:
        res = supabase.table("submissions").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("Submissions deleted successfully.")
    except Exception as e:
        print(f"Error deleting submissions: {e}")

    print("2. Deleting all daily activities...")
    try:
        res = supabase.table("daily_activities").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("Daily activities deleted successfully.")
    except Exception as e:
        print(f"Error deleting daily activities: {e}")

    print("3. Deleting all device logs...")
    try:
        res = supabase.table("device_logs").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("Device logs deleted successfully.")
    except Exception as e:
        print(f"Error deleting device logs: {e}")

    print("4. Deleting all approval requests...")
    try:
        res = supabase.table("approval_requests").delete().neq("id", "00000000-0000-0000-0000-000000000000").execute()
        print("Approval requests deleted successfully.")
    except Exception as e:
        print(f"Error deleting approval requests: {e}")

    print("5. Resetting all tasks status and scheduled date...")
    try:
        res = supabase.table("tasks").update({
            "status": "pending",
            "scheduled_date": "2026-06-01"
        }).neq("id", "").execute()
        print("Tasks reset successfully.")
    except Exception as e:
        print(f"Error resetting tasks: {e}")

if __name__ == "__main__":
    reset_db()
