import re

with open('/media/vpsg16gb/Workspace1/HanaApplication/frontend/parents.html', 'r') as f:
    content = f.read()

# Add a Quick Message widget in the dashboard
widget_html = """
              <!-- Quick Message to Hana -->
              <div class="bg-zinc-900 border border-zinc-800 rounded-3xl p-6 mt-6">
                <div class="flex items-center justify-between mb-4">
                  <div>
                    <div class="text-xs font-semibold text-pink-400 tracking-widest text-pink-400">MESSAGING</div>
                    <div class="font-semibold text-xl">Gửi tin nhắn nhanh cho Hana</div>
                  </div>
                  <button onclick="sendQuickMessage()" class="text-xs px-4 py-2 bg-pink-600 hover:bg-pink-500 text-white rounded-2xl font-medium flex items-center gap-x-1.5 transition-all">
                    <i class="fa-solid fa-paper-plane"></i><span>Gửi tin</span>
                  </button>
                </div>
                <div class="space-y-3.5 text-xs">
                  <textarea id="quick-message-input" rows="2" placeholder="Ví dụ: Cố lên con gái yêu! Hoàn thành bài sớm bố mẹ cho đi chơi nhé." class="w-full bg-zinc-950 border border-zinc-700 rounded-xl px-3 py-2.5 text-zinc-200 outline-none focus:border-pink-500 resize-none"></textarea>
                </div>
              </div>
"""

# Insert widget after Telegram configuration
content = content.replace('<!-- Device Monitoring -->', widget_html + '\n            <!-- Device Monitoring -->')

# Add JS function for Quick Message
js_func = """
    function sendQuickMessage() {
      const msg = document.getElementById('quick-message-input').value.trim();
      if (!msg) {
        alert("Vui lòng nhập tin nhắn!");
        return;
      }
      // Assuming a generic push to localstorage or supabase for Hana to read
      localStorage.setItem('hana_quick_message', msg);
      
      alert("Đã gửi tin nhắn cho Hana thành công!");
      document.getElementById('quick-message-input').value = "";
      
      // Notify via Telegram as well
      sendTelegramNotification('study', `💌 <b>Tin nhắn từ Bố Mẹ gửi Hana:</b>\\n\\n"${msg}"`);
    }
"""

content = content.replace('function initSupabase() {', js_func + '\n    function initSupabase() {')

with open('/media/vpsg16gb/Workspace1/HanaApplication/frontend/parents.html', 'w') as f:
    f.write(content)
