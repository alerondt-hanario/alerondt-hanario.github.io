import re

with open('/media/vpsg16gb/Workspace1/HanaApplication/frontend/index.html', 'r') as f:
    content = f.read()

# Add a "Message from Parents" notification area
message_html = """
        <!-- Message from Parents -->
        <div id="parent-message-container" class="hidden bg-indigo-50 border border-indigo-100 p-4 rounded-3xl mb-6 shadow-sm animate-bounce">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 bg-white rounded-2xl flex items-center justify-center text-indigo-500 shadow-xs">
              <i class="fa-solid fa-heart"></i>
            </div>
            <div>
              <span class="text-[9px] font-extrabold text-indigo-500 uppercase tracking-widest">TIN NHẮN TỪ BỐ MẸ</span>
              <p id="parent-message-text" class="text-xs font-bold text-indigo-900 mt-0.5 italic"></p>
            </div>
          </div>
        </div>
"""

# Insert before TOP SUMMARY WIDGETS ROW
content = content.replace('<!-- TOP SUMMARY WIDGETS ROW', message_html + '\n    <!-- TOP SUMMARY WIDGETS ROW')

# Add JS logic to check for parent message
js_logic = """
    function checkParentMessage() {
      const msg = localStorage.getItem('hana_quick_message');
      if (msg) {
        document.getElementById('parent-message-text').textContent = msg;
        document.getElementById('parent-message-container').classList.remove('hidden');
        // Clear after showing? Maybe keep it for the session
      } else {
        document.getElementById('parent-message-container').classList.add('hidden');
      }
    }
"""

content = content.replace('function init() {', js_logic + '\n    function init() {')
content = content.replace('setLang(\'vi\');', 'setLang(\'vi\');\n      checkParentMessage();')

with open('/media/vpsg16gb/Workspace1/HanaApplication/frontend/index.html', 'w') as f:
    f.write(content)
