import docx
import json
import re

doc = docx.Document('calendar.docx')

weeks = []
week_names = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十',
              '十一', '十二', '十三', '十四', '十五', '十六', '十七', '十八', '十九', '二十', '二十一', '二十二', '二十三']

seen_weeks = set()

for t_idx, table in enumerate(doc.tables):
    for r_idx in range(1, len(table.rows)):
        row = table.rows[r_idx]
        cells = [c.text.strip() for c in row.cells]
        if len(cells) < 12:
            continue
        
        # Clean week name
        week_raw = cells[1].replace('\n', '').replace(' ', '')
        if not week_raw:
            continue
            
        match_week = None
        for wn in sorted(week_names, key=len, reverse=True):
            if wn == week_raw:
                match_week = wn
                break
        if not match_week:
            continue
            
        if match_week in seen_weeks:
            continue
        seen_weeks.add(match_week)
        
        month_raw = cells[0].replace('\n', ' ').strip()
        dates = [cells[i].replace('\n', '').strip() for i in range(2, 9)]
        edu_events = cells[9]
        stu_events = cells[10]
        counsel_events = cells[11]
        
        weeks.append({
            'week': match_week,
            'week_num': len(weeks) + 1,
            'month': month_raw,
            'days': {
                'Sun': dates[0],
                'Mon': dates[1],
                'Tue': dates[2],
                'Wed': dates[3],
                'Thu': dates[4],
                'Fri': dates[5],
                'Sat': dates[6]
            },
            'raw_events': {
                '教務處.進修部': edu_events,
                '學務處': stu_events,
                '輔導室.總務處': counsel_events
            }
        })

print(f"Extracted {len(weeks)} weeks")
with open('extracted_weeks.json', 'w', encoding='utf-8') as f:
    json.dump(weeks, f, ensure_ascii=False, indent=2)
