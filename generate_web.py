import json

with open('calendar_data.json', 'r', encoding='utf-8') as f:
    cal_data = json.load(f)

json_str = json.dumps(cal_data, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>南投國中 115學年度第一學期行事曆</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          colors: {
            brand: {
              50: '#f0f9ff',
              100: '#e0f2fe',
              500: '#0284c7',
              600: '#0369a1',
              700: '#075985',
              800: '#0c4a6e',
            }
          }
        }
      }
    }
  </script>
  <style>
    @media print {
      .no-print { display: none !important; }
      body { background: white !important; color: black !important; font-size: 11pt; }
      .print-shadow-none { box-shadow: none !important; }
      table { page-break-inside: auto; }
      tr { page-break-inside: avoid; page-break-after: auto; }
      #passwordOverlay { display: none !important; }
      #appContent { filter: none !important; }
    }
    .badge-exam { background-color: #fee2e2; color: #991b1b; border: 1px solid #fecaca; }
    .badge-holiday { background-color: #dcfce7; color: #166534; border: 1px solid #bbf7d0; }
    .badge-activity { background-color: #e0e7ff; color: #3730a3; border: 1px solid #c7d2fe; }
    .badge-meeting { background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; }
    .badge-routine { background-color: #f3f4f6; color: #374151; border: 1px solid #e5e7eb; }
    .badge-admin { background-color: #ede9fe; color: #5b21b6; border: 1px solid #ddd6fe; }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #f1f5f9; }
    ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #94a3b8; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col font-sans antialiased selection:bg-brand-500 selection:text-white relative">

  <!-- Password Lock Overlay -->
  <div id="passwordOverlay" class="fixed inset-0 z-50 bg-slate-900/85 backdrop-blur-md flex items-center justify-center p-4 transition-opacity duration-300">
    <div class="bg-white rounded-3xl max-w-sm w-full p-6 sm:p-8 shadow-2xl border border-slate-100 text-center space-y-5">
      <div class="w-16 h-16 mx-auto rounded-2xl bg-sky-100 text-sky-700 flex items-center justify-center text-2xl shadow-inner">
        <i class="fa-solid fa-lock"></i>
      </div>
      <div>
        <h2 class="text-lg font-bold text-slate-800">南投國中 115學年度行事曆</h2>
        <p class="text-xs text-slate-500 mt-1">此為校內專屬系統，請輸入通行密碼以瀏覽</p>
      </div>
      <div class="space-y-3">
        <div class="relative">
          <input type="password" id="pwdInput" maxlength="20" placeholder="請輸入通行密碼"
            class="w-full text-center tracking-widest text-lg py-2.5 px-4 bg-slate-50 border border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-sky-500 focus:bg-white transition"
            onkeydown="if(event.key==='Enter') checkPassword()">
        </div>
        <p id="pwdError" class="hidden text-xs text-rose-600 font-medium">密碼錯誤，請重新輸入！</p>
        <button onclick="checkPassword()" class="w-full py-2.5 px-4 bg-sky-600 hover:bg-sky-700 active:scale-[0.98] text-white font-semibold rounded-xl text-sm transition shadow-sm">
          驗證進入
        </button>
      </div>
      <div class="text-[11px] text-slate-400">
        南投縣立南投國民中學
      </div>
    </div>
  </div>

  <div id="appContent" class="flex flex-col min-h-screen transition duration-300">
    <!-- Top Announcement / Bar -->
    <header class="bg-gradient-to-r from-sky-800 via-sky-700 to-indigo-900 text-white shadow-lg sticky top-0 z-30">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3 sm:py-4">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 rounded-xl bg-white/10 backdrop-blur border border-white/20 flex items-center justify-center text-xl shadow-inner">
              <i class="fa-solid fa-graduation-cap text-sky-200"></i>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs px-2 py-0.5 rounded-full bg-sky-500/30 text-sky-200 border border-sky-400/30 font-medium">115學年度 (2026~2027)</span>
                <span class="text-xs text-sky-200/80">南投縣立南投國民中學</span>
              </div>
              <h1 class="text-lg sm:text-xl font-bold tracking-tight">全校第一學期行事曆互動查詢系統</h1>
            </div>
          </div>

          <!-- Action tools -->
          <div class="flex items-center gap-2 self-start md:self-auto no-print">
            <a href="南投國中115學年度第一學期行事曆.xlsx" download class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-700/80 hover:bg-emerald-700 border border-emerald-400/40 text-xs font-medium text-white transition shadow-sm active:scale-95" title="下載精緻排版 Excel 表格 (.xlsx)">
              <i class="fa-solid fa-file-excel text-emerald-200"></i>
              <span>下載 Excel (.xlsx)</span>
            </a>
            <button onclick="downloadICS()" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sky-600/80 hover:bg-sky-600 border border-sky-400/40 text-xs font-medium text-white transition shadow-sm active:scale-95" title="匯入 Google 日曆 / Apple 行事曆">
              <i class="fa-solid fa-calendar-plus text-sky-200"></i>
              <span>匯出 .ICS</span>
            </button>
            <button onclick="window.print()" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-700/80 hover:bg-slate-700 border border-slate-500/40 text-xs font-medium text-white transition shadow-sm active:scale-95" title="友善排版列印">
              <i class="fa-solid fa-print text-slate-300"></i>
              <span>列印</span>
            </button>
            <button onclick="lockCalendar()" class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-slate-700/80 hover:bg-slate-700 border border-slate-500/40 text-xs font-medium text-white transition shadow-sm active:scale-95" title="鎖定頁面">
              <i class="fa-solid fa-lock text-slate-300"></i>
              <span class="hidden sm:inline">鎖定</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Key Dates Highlights Banner -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4 w-full no-print">
      <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200/80 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
        <div class="flex items-center gap-2 text-slate-700 text-sm font-semibold shrink-0">
          <span class="w-2.5 h-2.5 rounded-full bg-rose-500 animate-pulse"></span>
          <span>焦點時程速覽：</span>
        </div>
        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-5 gap-2.5 flex-1">
          <div class="bg-rose-50 border border-rose-200/80 rounded-xl p-2.5 text-center">
            <div class="text-[11px] font-bold text-rose-800">第一次段考</div>
            <div class="text-xs font-semibold text-rose-600">10/13(二) ~ 10/14(三)</div>
            <div class="text-[10px] text-rose-500">第 7 週</div>
          </div>
          <div class="bg-amber-50 border border-amber-200/80 rounded-xl p-2.5 text-center">
            <div class="text-[11px] font-bold text-amber-800">第二次段考</div>
            <div class="text-xs font-semibold text-amber-600">12/02(三) ~ 12/03(四)</div>
            <div class="text-[10px] text-amber-500">第 14 週</div>
          </div>
          <div class="bg-indigo-50 border border-indigo-200/80 rounded-xl p-2.5 text-center">
            <div class="text-[11px] font-bold text-indigo-800">第三次段考</div>
            <div class="text-xs font-semibold text-indigo-600">1/18(一) ~ 1/19(二)</div>
            <div class="text-[10px] text-indigo-500">第 21 週</div>
          </div>
          <div class="bg-emerald-50 border border-emerald-200/80 rounded-xl p-2.5 text-center">
            <div class="text-[11px] font-bold text-emerald-800">休業式 / 寒假</div>
            <div class="text-xs font-semibold text-emerald-600">1/20(三) 休業式</div>
            <div class="text-[10px] text-emerald-500">1/21 寒假開始</div>
          </div>
          <div class="hidden lg:block bg-purple-50 border border-purple-200/80 rounded-xl p-2.5 text-center">
            <div class="text-[11px] font-bold text-purple-800">全校運動會 (暫定)</div>
            <div class="text-xs font-semibold text-purple-600">12/18(五)</div>
            <div class="text-[10px] text-purple-500">第 16 週</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Control & Filter Area -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4 w-full no-print">
      <div class="bg-white rounded-2xl p-4 sm:p-5 shadow-sm border border-slate-200 space-y-4">
        
        <!-- Top Row: Search & View Toggle -->
        <div class="flex flex-col sm:flex-row items-center justify-between gap-3">
          <!-- Search Input -->
          <div class="relative w-full sm:max-w-md">
            <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
            <input type="text" id="searchInput" placeholder="搜尋事項、處室、關鍵字 (例如：段考、露營、體檢、補考...)" 
              class="w-full pl-9 pr-8 py-2 bg-slate-50 border border-slate-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-sky-500 focus:bg-white transition"
              oninput="handleSearch()">
            <button id="clearSearchBtn" onclick="clearSearch()" class="hidden absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
              <i class="fa-solid fa-xmark text-sm"></i>
            </button>
          </div>

          <!-- View Mode Switcher -->
          <div class="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 self-stretch sm:self-auto">
            <button id="viewWeeklyBtn" onclick="switchView('weekly')" class="flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-white text-sky-700 shadow-sm transition">
              <i class="fa-solid fa-table-cells"></i>
              <span>週次行事曆表</span>
            </button>
            <button id="viewTimelineBtn" onclick="switchView('timeline')" class="flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:text-slate-900 transition">
              <i class="fa-solid fa-list-check"></i>
              <span>清單卡片速查</span>
            </button>
          </div>
        </div>

        <!-- Filters: Department, Month, Tag -->
        <div class="pt-3 border-t border-slate-100 flex flex-wrap gap-2 items-center text-xs">
          <span class="text-slate-500 font-medium mr-1"><i class="fa-solid fa-filter mr-1"></i>處室篩選：</span>
          <div id="deptFilters" class="flex flex-wrap gap-1.5">
            <!-- Rendered dynamically -->
          </div>
        </div>

        <div class="flex flex-wrap gap-2 items-center text-xs">
          <span class="text-slate-500 font-medium mr-1"><i class="fa-regular fa-calendar mr-1"></i>月份切換：</span>
          <div id="monthFilters" class="flex flex-wrap gap-1.5">
            <!-- Rendered dynamically -->
          </div>
        </div>

        <div class="flex flex-wrap gap-2 items-center text-xs">
          <span class="text-slate-500 font-medium mr-1"><i class="fa-solid fa-tags mr-1"></i>事項分類：</span>
          <div id="tagFilters" class="flex flex-wrap gap-1.5">
            <!-- Rendered dynamically -->
          </div>
        </div>

        <!-- Result counter and active filter badges -->
        <div class="flex items-center justify-between text-xs text-slate-500 pt-1">
          <div id="filterSummary">顯示全部行事曆事項</div>
          <button onclick="resetFilters()" class="text-sky-600 hover:text-sky-700 hover:underline">
            <i class="fa-solid fa-rotate-left mr-1"></i>重設所有篩選
          </button>
        </div>
      </div>
    </section>

    <!-- Main Calendar Content Area -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5 flex-1 w-full">
      
      <!-- 1. Weekly Grid View (Matches original school schedule format) -->
      <div id="weeklyViewContainer" class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div class="p-4 bg-slate-50/80 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div class="flex items-center gap-2">
            <h2 class="font-bold text-slate-800 text-sm sm:text-base flex items-center gap-2">
              <i class="fa-solid fa-calendar-week text-sky-600"></i>
              <span>南投國中 115學年度第一學期 完整週次行事曆</span>
            </h2>
            <span class="text-xs px-2 py-0.5 rounded bg-sky-100 text-sky-800 font-medium">共 21 週</span>
          </div>
          <div class="text-xs text-slate-500 flex items-center gap-3">
            <span class="inline-flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-rose-500"></span> 考試測驗</span>
            <span class="inline-flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> 放假節日</span>
            <span class="inline-flex items-center gap-1"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span> 活動競賽</span>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs border-collapse">
            <thead>
              <tr class="bg-sky-900 text-white font-medium border-b border-sky-950">
                <th class="py-2.5 px-2 text-center w-14 border-r border-sky-800">月份</th>
                <th class="py-2.5 px-2 text-center w-12 border-r border-sky-800">週次</th>
                <th class="py-2.5 px-1.5 text-center w-8 border-r border-sky-800 bg-sky-950/40">日</th>
                <th class="py-2.5 px-1.5 text-center w-8 border-r border-sky-800">一</th>
                <th class="py-2.5 px-1.5 text-center w-8 border-r border-sky-800">二</th>
                <th class="py-2.5 px-1.5 text-center w-8 border-r border-sky-800">三</th>
                <th class="py-2.5 px-1.5 text-center w-8 border-r border-sky-800">四</th>
                <th class="py-2.5 px-1.5 text-center w-8 border-r border-sky-800">五</th>
                <th class="py-2.5 px-1.5 text-center w-8 border-r border-sky-800 bg-sky-950/40">六</th>
                <th class="py-2.5 px-3.5 border-r border-sky-800 w-[28%]">教務處 / 進修部</th>
                <th class="py-2.5 px-3.5 border-r border-sky-800 w-[30%]">學務處</th>
                <th class="py-2.5 px-3.5 w-[26%]">輔導室 / 總務處</th>
              </tr>
            </thead>
            <tbody id="weeklyTableBody" class="divide-y divide-slate-200">
              <!-- Rendered by JS -->
            </tbody>
          </table>
        </div>
      </div>

      <!-- 2. Timeline / Agenda List View -->
      <div id="timelineViewContainer" class="hidden space-y-4">
        <div id="timelineCards" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <!-- Rendered by JS -->
        </div>
        <div id="emptyResultsNotice" class="hidden text-center py-16 bg-white rounded-2xl border border-dashed border-slate-300">
          <i class="fa-solid fa-inbox text-4xl text-slate-300 mb-3"></i>
          <p class="text-slate-600 font-medium">沒有找到符合條件的行事曆事項</p>
          <p class="text-xs text-slate-400 mt-1">請嘗試變更搜尋關鍵字或清除篩選條件</p>
          <button onclick="resetFilters()" class="mt-4 px-4 py-1.5 bg-sky-600 text-white rounded-lg text-xs font-medium hover:bg-sky-700 transition">
            重設所有篩選
          </button>
        </div>
      </div>

    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200 py-6 mt-8 no-print">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs text-slate-500 space-y-1">
        <p class="font-medium text-slate-700">南投縣立南投國民中學 115學年度第一學期行事曆</p>
        <p>資料依據校方 115.08.28 核定完整版行事曆自動解析建置 • 支援手機、平板、電腦與一鍵匯入 Google 日曆</p>
      </div>
    </footer>
  </div>

  <!-- Detail Modal -->
  <div id="detailModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl border border-slate-100 transform transition-all">
      <div class="flex items-start justify-between pb-3 border-b border-slate-100">
        <div class="flex items-center gap-2">
          <span id="modalTag" class="px-2.5 py-0.5 rounded-full text-xs font-semibold badge-activity">活動</span>
          <span id="modalDept" class="text-xs text-slate-500 font-medium">學務處</span>
        </div>
        <button onclick="closeModal()" class="text-slate-400 hover:text-slate-600 p-1">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>
      <div class="py-4 space-y-3">
        <h3 id="modalTitle" class="text-base font-bold text-slate-900 leading-snug">事項名稱</h3>
        <div class="bg-slate-50 rounded-xl p-3 space-y-2 text-xs">
          <div class="flex items-center gap-2 text-slate-700">
            <i class="fa-regular fa-calendar-check text-sky-600 w-4"></i>
            <span class="font-medium">預定日期：</span>
            <span id="modalDate" class="font-semibold text-slate-900">-</span>
          </div>
          <div class="flex items-center gap-2 text-slate-700">
            <i class="fa-solid fa-timeline text-indigo-600 w-4"></i>
            <span class="font-medium">學期週次：</span>
            <span id="modalWeek" class="text-slate-800">-</span>
          </div>
        </div>
        <div>
          <span class="text-xs font-medium text-slate-500">原始公文記載內容：</span>
          <p id="modalOriginal" class="mt-1 p-3 bg-slate-100 rounded-xl text-xs text-slate-700 leading-relaxed font-mono whitespace-pre-wrap"></p>
        </div>
      </div>
      <div class="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
        <button onclick="addSingleEventToGoogle()" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-700 text-xs font-medium text-white transition">
          <i class="fa-brands fa-google"></i>
          <span>加入 Google 日曆</span>
        </button>
        <button onclick="closeModal()" class="px-3.5 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-xs font-medium text-slate-700 transition">
          關閉
        </button>
      </div>
    </div>
  </div>

  <!-- Raw Data Injection -->
  <script>
    const CALENDAR_DATA = """ + json_str + """;
  </script>

  <!-- Interactive Logic -->
  <script>
    const AUTH_KEY = 'ntjh_11501_authenticated';
    const PASSWORD = '049';

    function checkPassword() {
      const input = document.getElementById('pwdInput').value.trim();
      if (input === PASSWORD) {
        sessionStorage.setItem(AUTH_KEY, 'true');
        unlockCalendar();
      } else {
        const err = document.getElementById('pwdError');
        err.classList.remove('hidden');
        document.getElementById('pwdInput').focus();
        document.getElementById('pwdInput').select();
      }
    }

    function unlockCalendar() {
      const overlay = document.getElementById('passwordOverlay');
      overlay.classList.add('opacity-0', 'pointer-events-none');
      setTimeout(() => {
        overlay.style.display = 'none';
      }, 300);
      document.getElementById('appContent').classList.remove('blur-sm');
    }

    function lockCalendar() {
      sessionStorage.removeItem(AUTH_KEY);
      const overlay = document.getElementById('passwordOverlay');
      overlay.style.display = 'flex';
      setTimeout(() => {
        overlay.classList.remove('opacity-0', 'pointer-events-none');
      }, 10);
      document.getElementById('pwdInput').value = '';
      document.getElementById('pwdError').classList.add('hidden');
      document.getElementById('appContent').classList.add('blur-sm');
      document.getElementById('pwdInput').focus();
    }

    // Check authentication on initial page load
    (function initAuth() {
      if (sessionStorage.getItem(AUTH_KEY) === 'true') {
        const overlay = document.getElementById('passwordOverlay');
        overlay.style.display = 'none';
      } else {
        document.getElementById('appContent').classList.add('blur-sm');
        setTimeout(() => {
          const inp = document.getElementById('pwdInput');
          if (inp) inp.focus();
        }, 150);
      }
    })();

    let currentView = 'weekly'; // 'weekly' or 'timeline'
    let selectedDept = '全部';
    let selectedMonth = 'all';
    let selectedTag = '全部';
    let searchQuery = '';
    let currentModalEvent = null;

    // Initialize
    window.addEventListener('DOMContentLoaded', () => {
      renderFilters();
      renderCalendar();
    });

    function renderFilters() {
      // Departments
      const deptContainer = document.getElementById('deptFilters');
      deptContainer.innerHTML = CALENDAR_DATA.departments.map(dept => {
        const active = dept === selectedDept;
        return `<button onclick="setDept('${dept}')" class="px-2.5 py-1 rounded-lg transition font-medium ${
          active ? 'bg-sky-600 text-white shadow-sm' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
        }">${dept}</button>`;
      }).join('');

      // Months
      const monthContainer = document.getElementById('monthFilters');
      monthContainer.innerHTML = CALENDAR_DATA.months.map(m => {
        const active = m.id === selectedMonth;
        return `<button onclick="setMonth('${m.id}')" class="px-2.5 py-1 rounded-lg transition font-medium ${
          active ? 'bg-sky-600 text-white shadow-sm' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
        }">${m.label}</button>`;
      }).join('');

      // Tags
      const tagContainer = document.getElementById('tagFilters');
      tagContainer.innerHTML = CALENDAR_DATA.tags.map(t => {
        const active = t === selectedTag;
        return `<button onclick="setTag('${t}')" class="px-2.5 py-1 rounded-lg transition font-medium ${
          active ? 'bg-indigo-600 text-white shadow-sm' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
        }">${t}</button>`;
      }).join('');
    }

    function setDept(dept) { selectedDept = dept; renderFilters(); renderCalendar(); }
    function setMonth(mId) { selectedMonth = mId; renderFilters(); renderCalendar(); }
    function setTag(t) { selectedTag = t; renderFilters(); renderCalendar(); }

    function resetFilters() {
      selectedDept = '全部';
      selectedMonth = 'all';
      selectedTag = '全部';
      searchQuery = '';
      document.getElementById('searchInput').value = '';
      document.getElementById('clearSearchBtn').classList.add('hidden');
      renderFilters();
      renderCalendar();
    }

    function handleSearch() {
      const val = document.getElementById('searchInput').value.trim();
      searchQuery = val.toLowerCase();
      document.getElementById('clearSearchBtn').classList.toggle('hidden', !searchQuery);
      renderCalendar();
    }

    function clearSearch() {
      document.getElementById('searchInput').value = '';
      searchQuery = '';
      document.getElementById('clearSearchBtn').classList.add('hidden');
      renderCalendar();
    }

    function switchView(view) {
      currentView = view;
      const weeklyBtn = document.getElementById('viewWeeklyBtn');
      const timelineBtn = document.getElementById('viewTimelineBtn');
      const weeklyContainer = document.getElementById('weeklyViewContainer');
      const timelineContainer = document.getElementById('timelineViewContainer');

      if (view === 'weekly') {
        weeklyBtn.className = 'flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-white text-sky-700 shadow-sm transition';
        timelineBtn.className = 'flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:text-slate-900 transition';
        weeklyContainer.classList.remove('hidden');
        timelineContainer.classList.add('hidden');
      } else {
        timelineBtn.className = 'flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-semibold bg-white text-sky-700 shadow-sm transition';
        weeklyBtn.className = 'flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-medium text-slate-600 hover:text-slate-900 transition';
        weeklyContainer.classList.add('hidden');
        timelineContainer.classList.remove('hidden');
      }
      renderCalendar();
    }

    // Filter logic
    function getFilteredEvents() {
      return CALENDAR_DATA.events.filter(ev => {
        // Dept match
        if (selectedDept !== '全部' && ev.department !== selectedDept) return false;
        
        // Month match
        if (selectedMonth !== 'all') {
          if (!ev.month || ev.month.toString() !== selectedMonth) return false;
        }

        // Tag match
        if (selectedTag !== '全部' && ev.tag !== selectedTag) return false;

        // Search Query
        if (searchQuery) {
          const content = `${ev.title} ${ev.original_text} ${ev.department} ${ev.week} ${ev.date_display} ${ev.tag}`.toLowerCase();
          if (!content.includes(searchQuery)) return false;
        }

        return true;
      });
    }

    function getTagClass(tag) {
      switch (tag) {
        case '考試測驗': return 'badge-exam';
        case '放假節日': return 'badge-holiday';
        case '活動競賽': return 'badge-activity';
        case '重要校務': return 'badge-meeting';
        case '校務行政': return 'badge-admin';
        case '例行集會': return 'badge-routine';
        default: return 'bg-slate-100 text-slate-700 border border-slate-200';
      }
    }

    function renderCalendar() {
      const filteredEvents = getFilteredEvents();
      
      // Update summary text
      const summaryElem = document.getElementById('filterSummary');
      summaryElem.innerHTML = `符合條件事項：<strong class="text-sky-700 font-bold">${filteredEvents.length}</strong> 項 (共 ${CALENDAR_DATA.events.length} 項)`;

      if (currentView === 'weekly') {
        renderWeeklyTable(filteredEvents);
      } else {
        renderTimeline(filteredEvents);
      }
    }

    // Render Weekly Table
    function renderWeeklyTable(filteredEvents) {
      const tbody = document.getElementById('weeklyTableBody');
      const filteredEventIds = new Set(filteredEvents.map(e => e.id));

      const isFiltering = selectedDept !== '全部' || selectedMonth !== 'all' || selectedTag !== '全部' || searchQuery !== '';

      let html = '';
      CALENDAR_DATA.weeks.forEach((w, idx) => {
        const weekEvents = CALENDAR_DATA.events.filter(e => e.week_num === w.week_num);
        const matchingWeekEvents = weekEvents.filter(e => filteredEventIds.has(e.id));
        
        if (isFiltering && matchingWeekEvents.length === 0) {
          return;
        }

        const days = w.days;
        const isExamWeek = weekEvents.some(e => e.tag === '考試測驗');

        const rowBg = idx % 2 === 0 ? 'bg-white' : 'bg-slate-50/50';

        const formatDeptCell = (deptName) => {
          const deptEvents = weekEvents.filter(e => {
            if (deptName === '教務處/進修部') return e.department === '教務處/進修部' || e.department.includes('教務');
            if (deptName === '學務處') return e.department === '學務處';
            return e.department === '輔導室/總務處' || e.department.includes('輔導') || e.department.includes('總務');
          });

          if (deptEvents.length === 0) return '<span class="text-slate-300">-</span>';

          return deptEvents.map(e => {
            const isMatch = filteredEventIds.has(e.id);
            const opacityClass = isFiltering && !isMatch ? 'opacity-30' : 'opacity-100';
            const tagStyle = getTagClass(e.tag);
            
            return `
              <div onclick="openModal(${e.id})" class="mb-1.5 p-1.5 rounded-lg border text-left cursor-pointer transition hover:scale-[1.01] hover:shadow-sm ${opacityClass} ${
                isMatch ? 'bg-white shadow-xs' : 'bg-slate-50'
              }">
                <div class="flex items-center gap-1.5 mb-0.5 flex-wrap">
                  ${e.date_display ? `<span class="font-bold text-[11px] text-slate-800">${e.date_display}</span>` : ''}
                  <span class="text-[10px] px-1.5 py-0.2 rounded font-medium ${tagStyle}">${e.tag}</span>
                </div>
                <div class="text-xs text-slate-700 leading-snug font-normal">${highlightText(e.title, searchQuery)}</div>
              </div>
            `;
          }).join('');
        };

        html += `
          <tr class="${rowBg} hover:bg-sky-50/40 transition">
            <td class="py-3 px-2 text-center font-bold text-slate-600 border-r border-slate-200">
              ${w.month || ''}
            </td>
            <td class="py-3 px-2 text-center font-bold border-r border-slate-200 ${
              isExamWeek ? 'text-rose-600' : 'text-slate-800'
            }">
              第${w.week}週
            </td>
            <td class="py-2 px-1 text-center font-medium border-r border-slate-200 text-slate-400 bg-slate-50/50">${days.Sun || ''}</td>
            <td class="py-2 px-1 text-center font-medium border-r border-slate-200 text-slate-700">${days.Mon || ''}</td>
            <td class="py-2 px-1 text-center font-medium border-r border-slate-200 text-slate-700">${days.Tue || ''}</td>
            <td class="py-2 px-1 text-center font-medium border-r border-slate-200 text-slate-700">${days.Wed || ''}</td>
            <td class="py-2 px-1 text-center font-medium border-r border-slate-200 text-slate-700">${days.Thu || ''}</td>
            <td class="py-2 px-1 text-center font-medium border-r border-slate-200 text-slate-700">${days.Fri || ''}</td>
            <td class="py-2 px-1 text-center font-medium border-r border-slate-200 text-slate-400 bg-slate-50/50">${days.Sat || ''}</td>
            
            <td class="py-2.5 px-3 align-top border-r border-slate-200">
              ${formatDeptCell('教務處/進修部')}
            </td>
            <td class="py-2.5 px-3 align-top border-r border-slate-200">
              ${formatDeptCell('學務處')}
            </td>
            <td class="py-2.5 px-3 align-top">
              ${formatDeptCell('輔導室/總務處')}
            </td>
          </tr>
        `;
      });

      if (html === '') {
        tbody.innerHTML = `
          <tr>
            <td colspan="12" class="py-12 text-center text-slate-400">
              <i class="fa-solid fa-search text-3xl mb-2 text-slate-300 block"></i>
              沒有符合條件的週次事項
            </td>
          </tr>
        `;
      } else {
        tbody.innerHTML = html;
      }
    }

    // Render Timeline View
    function renderTimeline(filteredEvents) {
      const container = document.getElementById('timelineCards');
      const emptyNotice = document.getElementById('emptyResultsNotice');

      if (filteredEvents.length === 0) {
        container.innerHTML = '';
        emptyNotice.classList.remove('hidden');
        return;
      }

      emptyNotice.classList.add('hidden');

      container.innerHTML = filteredEvents.map(e => {
        const tagStyle = getTagClass(e.tag);
        const deptColor = e.department.includes('教務') ? 'text-sky-700 bg-sky-50 border-sky-200' :
                          e.department.includes('學務') ? 'text-amber-800 bg-amber-50 border-amber-200' :
                          'text-emerald-800 bg-emerald-50 border-emerald-200';

        return `
          <div onclick="openModal(${e.id})" class="bg-white rounded-2xl p-4 border border-slate-200/90 shadow-sm hover:shadow-md transition hover:-translate-y-0.5 cursor-pointer flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between gap-2 mb-2">
                <span class="text-xs px-2.5 py-0.5 rounded-full font-semibold ${tagStyle}">${e.tag}</span>
                <span class="text-xs px-2 py-0.5 rounded-md font-medium border ${deptColor}">${e.department}</span>
              </div>
              <h3 class="text-sm font-bold text-slate-900 leading-snug mb-2">${highlightText(e.title, searchQuery)}</h3>
              <p class="text-xs text-slate-500 line-clamp-2 leading-relaxed font-normal">${e.original_text}</p>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-600">
              <span class="flex items-center gap-1 font-semibold text-slate-800">
                <i class="fa-regular fa-clock text-sky-600"></i>
                ${e.date_display}
              </span>
              <span class="text-slate-400 font-medium">${e.week}</span>
            </div>
          </div>
        `;
      }).join('');
    }

    function highlightText(text, query) {
      if (!query) return text;
      const regex = new RegExp(`(${query})`, 'gi');
      return text.replace(regex, '<mark class="bg-amber-200 text-slate-900 px-0.5 rounded">$1</mark>');
    }

    // Modal
    function openModal(id) {
      const ev = CALENDAR_DATA.events.find(e => e.id === id);
      if (!ev) return;
      currentModalEvent = ev;

      document.getElementById('modalTitle').textContent = ev.title;
      document.getElementById('modalDept').textContent = ev.department;
      document.getElementById('modalTag').textContent = ev.tag;
      document.getElementById('modalTag').className = `px-2.5 py-0.5 rounded-full text-xs font-semibold ${getTagClass(ev.tag)}`;
      document.getElementById('modalDate').textContent = `${ev.date_display} (${ev.start_date || '依週次日程'})`;
      document.getElementById('modalWeek').textContent = ev.week;
      document.getElementById('modalOriginal').textContent = ev.original_text;

      document.getElementById('detailModal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('detailModal').classList.add('hidden');
      currentModalEvent = null;
    }

    // Google Calendar Link for single event
    function addSingleEventToGoogle() {
      if (!currentModalEvent) return;
      const ev = currentModalEvent;
      const title = encodeURIComponent(`[${ev.department}] ${ev.title}`);
      const details = encodeURIComponent(`${ev.original_text} (南投國中115學年度第一學期 ${ev.week})`);
      
      let datesParam = '';
      if (ev.start_date && ev.end_date) {
        const s = ev.start_date.replace(/-/g, '');
        const parts = ev.end_date.split('-');
        const endDateObj = new Date(parts[0], parts[1] - 1, parts[2]);
        endDateObj.setDate(endDateObj.getDate() + 1);
        const y = endDateObj.getFullYear();
        const m = String(endDateObj.getMonth() + 1).padStart(2, '0');
        const d = String(endDateObj.getDate()).padStart(2, '0');
        const e = `${y}${m}${d}`;
        datesParam = `&dates=${s}/${e}`;
      }
      
      const url = `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&details=${details}${datesParam}`;
      window.open(url, '_blank');
    }

    // Download Full ICS
    function downloadICS() {
      let icsContent = "BEGIN:VCALENDAR\\r\\nVERSION:2.0\\r\\nPRODID:-//NTJH//School Calendar 115-1//ZH-TW\\r\\nCALSCALE:GREGORIAN\\r\\nMETHOD:PUBLISH\\r\\nX-WR-CALNAME:南投國中115學年度第一學期行事曆\\r\\nX-WR-TIMEZONE:Asia/Taipei\\r\\n";

      CALENDAR_DATA.events.forEach(ev => {
        if (!ev.start_date) return;
        const s = ev.start_date.replace(/-/g, '');
        const parts = ev.end_date.split('-');
        const endDateObj = new Date(parts[0], parts[1] - 1, parts[2]);
        endDateObj.setDate(endDateObj.getDate() + 1);
        const y = endDateObj.getFullYear();
        const m = String(endDateObj.getMonth() + 1).padStart(2, '0');
        const d = String(endDateObj.getDate()).padStart(2, '0');
        const e = `${y}${m}${d}`;

        icsContent += `BEGIN:VEVENT\\r\\nUID:ntjh-115-1-${ev.id}@school\\r\\nDTSTAMP:20260901T000000Z\\r\\nDTSTART;VALUE=DATE:${s}\\r\\nDTEND;VALUE=DATE:${e}\\r\\nSUMMARY:[${ev.department}] ${ev.title}\\r\\nDESCRIPTION:${ev.original_text.replace(/\\n/g, ' ')} (${ev.week})\\r\\nCATEGORIES:${ev.tag}\\r\\nSTATUS:CONFIRMED\\r\\nEND:VEVENT\\r\\n`;
      });

      icsContent += "END:VCALENDAR";

      const blob = new Blob([icsContent], { type: 'text/calendar;charset=utf-8' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = '南投國中115學年度第一學期行事曆.ics';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("Generated index.html with password protection successfully!")
