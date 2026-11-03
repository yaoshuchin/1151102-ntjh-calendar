import json
import re

with open('extracted_weeks.json', 'r', encoding='utf-8') as f:
    weeks = json.load(f)

def get_year(month):
    return 2027 if month == 1 else 2026

# Pattern matching
range_pattern = re.compile(r'^(\d{1,2})/(\d{1,2})(?:\([^\)]+\))?\s*(?:~|-)\s*(\d{1,2})/(\d{1,2})(?:\([^\)]+\))?\s*(.*)$', re.DOTALL)
dot_range_pattern = re.compile(r'^(\d{1,2})/(\d{1,2}(?:\.\d{1,2})+)(?:\([^\)]+\))?\s*(.*)$', re.DOTALL)
weird_range_pattern = re.compile(r'^(\d{1,2})/(\d{1,2})(?:\([^\)]+\))?\s*-\s*/?(\d{1,2})/(\d{1,2})(?:\([^\)]+\))?\s*(.*)$', re.DOTALL)
single_date_pattern = re.compile(r'^(\d{1,2})/(\d{1,2})(?:\([^\)]+\))?\s*(.*)$', re.DOTALL)
month_only_pattern = re.compile(r'^(\d{1,2})月\s*(.*)$', re.DOTALL)

events = []
event_id = 1

# Process each week
for w in weeks:
    week_name = f"第{w['week']}週"
    week_num = w['week_num']
    
    # Calculate approximate week Monday-Friday dates
    mon_day = w['days']['Mon']
    fri_day = w['days']['Fri']
    
    for dept, raw_content in w['raw_events'].items():
        if not raw_content.strip():
            continue
            
        lines = [l.strip() for l in raw_content.split('\n') if l.strip()]
        
        merged_items = []
        for line in lines:
            is_new = (
                re.match(r'^\d{1,2}/\d{1,2}', line) or 
                re.match(r'^\d{1,2}月', line) or
                line.startswith('進修部') or
                re.match(r'^\d{1,2}\.\d{1,2}', line)
            )
            if is_new or len(merged_items) == 0:
                merged_items.append(line)
            else:
                merged_items[-1] += " " + line
                
        for item in merged_items:
            item_clean = item.strip()
            title = item_clean
            start_date = None
            end_date = None
            date_display = ""
            tag = "重要校務"
            
            # Classification
            if any(k in item_clean for k in ['段考', '複習考', '補考', '期中考', '期末考', '測驗', '智力測驗']):
                tag = "考試測驗"
            elif any(k in item_clean for k in ['放假', '補假', '中秋節', '國慶日', '開國紀念日', '行憲紀念日']):
                tag = "放假節日"
            elif any(k in item_clean for k in ['晨讀', '朝會', '週會', '宣導', '儀態形象']):
                tag = "例行集會"
            elif any(k in item_clean for k in ['比賽', '競賽', '美展', '運動會', '博覽會', '露營', '戶外教育', '得勝者', '技藝課程', '講座', '演講', '音樂比賽', '舞蹈比賽', '環境知識']):
                tag = "活動競賽"
            elif any(k in item_clean for k in ['會議', '會報', '親師座談', '家長委員', '截止', '註冊', '減免', '開學', '休業式', '大掃除', '體檢', '疫苗', '收件', '領取', '退件', '贈報']):
                tag = "校務行政"
                
            m_range = range_pattern.match(item_clean) or weird_range_pattern.match(item_clean)
            if m_range:
                m1, d1, m2, d2, rest = m_range.groups()
                m1, d1, m2, d2 = int(m1), int(d1), int(m2), int(d2)
                y1 = get_year(m1)
                y2 = get_year(m2)
                start_date = f"{y1:04d}-{m1:02d}-{d1:02d}"
                end_date = f"{y2:04d}-{m2:02d}-{d2:02d}"
                date_display = f"{m1}/{d1} ~ {m2}/{d2}"
                title = rest.strip()
            else:
                m_dot = dot_range_pattern.match(item_clean)
                if m_dot:
                    m, dots, rest = m_dot.groups()
                    m = int(m)
                    days = [int(x) for x in dots.split('.')]
                    y = get_year(m)
                    start_date = f"{y:04d}-{m:02d}-{days[0]:02d}"
                    end_date = f"{y:04d}-{m:02d}-{days[-1]:02d}"
                    date_display = f"{m}/{days[0]} ~ {m}/{days[-1]}" if len(days) > 1 else f"{m}/{days[0]}"
                    title = rest.strip()
                else:
                    m_single = single_date_pattern.match(item_clean)
                    if m_single:
                        m, d, rest = m_single.groups()
                        m, d = int(m), int(d)
                        y = get_year(m)
                        start_date = f"{y:04d}-{m:02d}-{d:02d}"
                        end_date = start_date
                        date_display = f"{m}/{d}"
                        title = rest.strip()
                    else:
                        m_month = month_only_pattern.match(item_clean)
                        if m_month:
                            m, rest = m_month.groups()
                            m = int(m)
                            y = get_year(m)
                            date_display = f"{m}月份"
                            start_date = f"{y:04d}-{m:02d}-01"
                            end_date = f"{y:04d}-{m:02d}-28"
                            title = item_clean
                        else:
                            # Fallback using week info
                            title = item_clean
                            date_display = f"第{w['week']}週"
                            # Guess month from week
                            if week_num <= 5:
                                y, m = 2026, 9
                            elif week_num <= 9:
                                y, m = 2026, 10
                            elif week_num <= 13:
                                y, m = 2026, 11
                            elif week_num <= 18:
                                y, m = 2026, 12
                            else:
                                y, m = 2027, 1
                            if mon_day and mon_day.isdigit():
                                start_date = f"{y:04d}-{m:02d}-{int(mon_day):02d}"
                                end_date = f"{y:04d}-{m:02d}-{int(fri_day):02d}" if (fri_day and fri_day.isdigit() and int(fri_day) >= int(mon_day)) else start_date

            title = re.sub(r'^[~:\-\s]+', '', title).strip()
            if not title:
                title = item_clean

            # Normalize department
            clean_dept = dept
            if '教務' in dept:
                clean_dept = '教務處/進修部'
            elif '學務' in dept:
                clean_dept = '學務處'
            elif '輔導' in dept or '總務' in dept:
                clean_dept = '輔導室/總務處'

            events.append({
                'id': event_id,
                'week': week_name,
                'week_num': week_num,
                'department': clean_dept,
                'tag': tag,
                'title': title,
                'original_text': item_clean,
                'date_display': date_display,
                'start_date': start_date,
                'end_date': end_date,
                'month': int(start_date.split('-')[1]) if start_date else None
            })
            event_id += 1

# Generate ICS
def generate_ics(events):
    ics_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//NTJH//School Calendar 115-1//ZH-TW",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:南投國中115學年度第一學期行事曆",
        "X-WR-TIMEZONE:Asia/Taipei"
    ]
    for ev in events:
        if not ev['start_date']:
            continue
        s_date = ev['start_date'].replace('-', '')
        e_date = ev['end_date'].replace('-', '')
        
        # All-day event end date in ICS is exclusive (+1 day)
        # If single day, DTEND can be s_date + 1 day
        import datetime
        dt_start = datetime.date.fromisoformat(ev['start_date'])
        dt_end = datetime.date.fromisoformat(ev['end_date']) + datetime.timedelta(days=1)
        
        ics_lines.extend([
            "BEGIN:VEVENT",
            f"UID:ntjh-115-1-{ev['id']}@school",
            f"DTSTAMP:20260901T000000Z",
            f"DTSTART;VALUE=DATE:{dt_start.strftime('%Y%m%d')}",
            f"DTEND;VALUE=DATE:{dt_end.strftime('%Y%m%d')}",
            f"SUMMARY:[{ev['department']}] {ev['title']}",
            f"DESCRIPTION:{ev['original_text']} ({ev['week']})",
            f"CATEGORIES:{ev['tag']}",
            "STATUS:CONFIRMED",
            "END:VEVENT"
        ])
    ics_lines.append("END:VCALENDAR")
    return "\r\n".join(ics_lines)

ics_content = generate_ics(events)
with open('ntjh_calendar_11501.ics', 'w', encoding='utf-8') as f:
    f.write(ics_content)

full_data = {
    'title': '南投縣立南投國民中學 115學年度第一學期行事曆',
    'subtitle': '核定日期：115.08.28 | 民國115年 (2026 Fall ~ 2027 Winter)',
    'weeks': weeks,
    'events': events,
    'departments': ['全部', '教務處/進修部', '學務處', '輔導室/總務處'],
    'tags': ['全部', '重要校務', '考試測驗', '放假節日', '例行集會', '活動競賽', '校務行政'],
    'months': [
        {'id': 'all', 'label': '全部月份'},
        {'id': '8', 'label': '8月 (2026)'},
        {'id': '9', 'label': '9月 (2026)'},
        {'id': '10', 'label': '10月 (2026)'},
        {'id': '11', 'label': '11月 (2026)'},
        {'id': '12', 'label': '12月 (2026)'},
        {'id': '1', 'label': '1月 (2027)'}
    ]
}

with open('calendar_data.json', 'w', encoding='utf-8') as f:
    json.dump(full_data, f, ensure_ascii=False, indent=2)

print("Saved calendar_data.json and ntjh_calendar_11501.ics")
