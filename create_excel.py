import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

with open('calendar_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

wb = openpyxl.Workbook()
wb.remove(wb.active)

# Color definitions
HEADER_BG = "1F4E79"        # Navy blue
HEADER_TEXT = "FFFFFF"
ZEBRA_BG = "F9FAFB"         # Very soft light grey
BORDER_COLOR = "D1D5DB"     # Soft grey

font_title = Font(name="微軟正黑體", size=14, bold=True, color="1F4E79")
font_sub = Font(name="微軟正黑體", size=10, italic=True, color="4B5563")
font_header = Font(name="微軟正黑體", size=11, bold=True, color=HEADER_TEXT)
font_regular = Font(name="微軟正黑體", size=10)
font_bold = Font(name="微軟正黑體", size=10, bold=True)

fill_header = PatternFill(start_color=HEADER_BG, end_color=HEADER_BG, fill_type="solid")
fill_zebra = PatternFill(start_color=ZEBRA_BG, end_color=ZEBRA_BG, fill_type="solid")
fill_white = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

# Category fills
fills_tag = {
    "朝會": PatternFill(start_color="FED7AA", end_color="FED7AA", fill_type="solid"),     # Amber/Orange
    "週會": PatternFill(start_color="DDD6FE", end_color="DDD6FE", fill_type="solid"),     # Purple
    "訓育組": PatternFill(start_color="BAE6FD", end_color="BAE6FD", fill_type="solid"),   # Sky blue
    "考試測驗": PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid"), # Light red
    "放假節日": PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid"), # Light green
    "活動競賽": PatternFill(start_color="E0E7FF", end_color="E0E7FF", fill_type="solid"), # Light indigo
    "重要校務": PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid"), # Light amber
    "例行集會": PatternFill(start_color="F3F4F6", end_color="F3F4F6", fill_type="solid"), # Light grey
    "校務行政": PatternFill(start_color="EDE9FE", end_color="EDE9FE", fill_type="solid")  # Light purple
}
fonts_tag = {
    "朝會": Font(name="微軟正黑體", size=10, bold=True, color="9A3412"),
    "週會": Font(name="微軟正黑體", size=10, bold=True, color="5B21B6"),
    "訓育組": Font(name="微軟正黑體", size=10, bold=True, color="0369A1"),
    "考試測驗": Font(name="微軟正黑體", size=10, bold=True, color="991B1B"),
    "放假節日": Font(name="微軟正黑體", size=10, bold=True, color="166534"),
    "活動競賽": Font(name="微軟正黑體", size=10, bold=True, color="3730A3"),
    "重要校務": Font(name="微軟正黑體", size=10, bold=True, color="92400E"),
    "例行集會": Font(name="微軟正黑體", size=10, color="374151"),
    "校務行政": Font(name="微軟正黑體", size=10, color="5B21B6")
}

thin_side = Side(border_style="thin", color=BORDER_COLOR)
border_all = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_right = Alignment(horizontal="right", vertical="center")

# ==========================================
# Sheet 1: 行事曆事項檢索清單 (Search-Friendly)
# ==========================================
ws1 = wb.create_sheet(title="行事曆事項檢索清單")
ws1.views.sheetView[0].showGridLines = True

# Title block
ws1.merge_cells("A1:K1")
ws1["A1"] = "南投縣立南投國民中學 115學年度第一學期 行事曆事項檢索清單（含訓育組/朝會/週會分類）"
ws1["A1"].font = font_title
ws1["A1"].alignment = Alignment(horizontal="left", vertical="center")
ws1.row_dimensions[1].height = 28

ws1.merge_cells("A2:K2")
ws1["A2"] = "核定日期：115.08.28 | 本表已啟用「自動篩選」，點擊標題列箭頭即可依處室、組別、月份、類別(朝會/週會/訓育組等)或關鍵字即時篩選"
ws1["A2"].font = font_sub
ws1["A2"].alignment = Alignment(horizontal="left", vertical="center")
ws1.row_dimensions[2].height = 18

headers1 = ["編號", "週次", "月份", "日期區間", "負責處室", "主辦組別", "事項分類", "事項名稱", "起始日期", "結束日期", "原始公文記載備註"]
header_row1 = 4
ws1.row_dimensions[header_row1].height = 26

for col_idx, h in enumerate(headers1, start=1):
    cell = ws1.cell(row=header_row1, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = align_center
    cell.border = border_all

events = data["events"]
for idx, ev in enumerate(events, start=1):
    r = header_row1 + idx
    ws1.row_dimensions[r].height = 22
    is_zebra = (idx % 2 == 0)
    base_fill = fill_zebra if is_zebra else fill_white

    c1 = ws1.cell(row=r, column=1, value=ev["id"])
    c1.alignment = align_center
    
    c2 = ws1.cell(row=r, column=2, value=ev["week"])
    c2.alignment = align_center
    
    m_val = f"{ev['month']}月" if ev.get("month") else "-"
    c3 = ws1.cell(row=r, column=3, value=m_val)
    c3.alignment = align_center
    
    c4 = ws1.cell(row=r, column=4, value=ev["date_display"])
    c4.alignment = align_center
    c4.font = font_bold
    
    c5 = ws1.cell(row=r, column=5, value=ev["department"])
    c5.alignment = align_center

    # Column 6: 主辦組別
    sec = ev.get("section", "一般")
    c6 = ws1.cell(row=r, column=6, value=sec)
    c6.alignment = align_center
    if sec == "訓育組":
        c6.font = Font(name="微軟正黑體", size=10, bold=True, color="0369A1")
        c6.fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid")
    else:
        c6.font = font_regular
        c6.fill = base_fill
    
    # Column 7: 事項分類
    tag = ev["tag"]
    c7 = ws1.cell(row=r, column=7, value=tag)
    c7.alignment = align_center
    if tag in fills_tag:
        c7.fill = fills_tag[tag]
        c7.font = fonts_tag[tag]
    else:
        c7.font = font_regular
        c7.fill = base_fill

    c8 = ws1.cell(row=r, column=8, value=ev["title"])
    c8.alignment = align_left
    c8.font = font_regular
    
    c9 = ws1.cell(row=r, column=9, value=ev["start_date"] or "")
    c9.alignment = align_center
    c9.font = font_regular
    
    c10 = ws1.cell(row=r, column=10, value=ev["end_date"] or "")
    c10.alignment = align_center
    c10.font = font_regular
    
    c11 = ws1.cell(row=r, column=11, value=ev["original_text"])
    c11.alignment = align_left
    c11.font = font_regular

    for col_i in range(1, 12):
        c = ws1.cell(row=r, column=col_i)
        c.border = border_all
        if col_i not in [6, 7]:
            c.fill = base_fill

# Enable AutoFilter on header row
ws1.auto_filter.ref = f"A{header_row1}:K{header_row1 + len(events)}"
ws1.freeze_panes = f"A{header_row1 + 1}"

# Auto-fit column widths
col_widths1 = {1: 8, 2: 12, 3: 8, 4: 16, 5: 16, 6: 14, 7: 14, 8: 38, 9: 13, 10: 13, 11: 45}
for col_i, w in col_widths1.items():
    ws1.column_dimensions[get_column_letter(col_i)].width = w


# ==========================================
# Sheet 2: 週次行事曆總表 (Original Form Layout)
# ==========================================
ws2 = wb.create_sheet(title="週次行事曆總表")
ws2.views.sheetView[0].showGridLines = True

ws2.merge_cells("A1:L1")
ws2["A1"] = "南投縣立南投國民中學 115學年度第一學期 完整週次行事曆總表"
ws2["A1"].font = font_title
ws2["A1"].alignment = Alignment(horizontal="left", vertical="center")
ws2.row_dimensions[1].height = 28

ws2.merge_cells("A2:L2")
ws2["A2"] = "核定日期：115.08.28 | 還原學校紙本全校行事曆版面（依處室三欄呈現）"
ws2["A2"].font = font_sub
ws2["A2"].alignment = Alignment(horizontal="left", vertical="center")
ws2.row_dimensions[2].height = 18

headers2 = ["月份", "週次", "日", "一", "二", "三", "四", "五", "六", "教務處 / 進修部", "學務處", "輔導室 / 總務處"]
header_row2 = 4
ws2.row_dimensions[header_row2].height = 26

for col_idx, h in enumerate(headers2, start=1):
    cell = ws2.cell(row=header_row2, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = fill_header
    cell.alignment = align_center
    cell.border = border_all

weeks = data["weeks"]
for idx, w in enumerate(weeks, start=1):
    r = header_row2 + idx
    days = w["days"]
    raw_ev = w["raw_events"]
    
    lines_count = max(
        len(raw_ev.get("教務處.進修部", "").split('\n')),
        len(raw_ev.get("學務處", "").split('\n')),
        len(raw_ev.get("輔導室.總務處", "").split('\n')),
        1
    )
    ws2.row_dimensions[r].height = max(24, lines_count * 16 + 8)
    
    is_zebra = (idx % 2 == 0)
    base_fill = fill_zebra if is_zebra else fill_white
    
    # Month
    c_m = ws2.cell(row=r, column=1, value=w.get("month", "").strip())
    c_m.alignment = align_center
    c_m.font = font_bold
    
    # Week
    c_w = ws2.cell(row=r, column=2, value=f"第{w['week']}週")
    c_w.alignment = align_center
    c_w.font = font_bold
    
    # Days Sun ~ Sat
    day_keys = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for day_i, dk in enumerate(day_keys, start=3):
        c_day = ws2.cell(row=r, column=day_i, value=days.get(dk, ""))
        c_day.alignment = align_center
        c_day.font = font_regular
        if dk in ["Sun", "Sat"]:
            c_day.fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
    
    # 3 Departments
    c_edu = ws2.cell(row=r, column=10, value=raw_ev.get("教務處.進修部", ""))
    c_edu.alignment = align_left
    c_edu.font = font_regular
    
    c_stu = ws2.cell(row=r, column=11, value=raw_ev.get("學務處", ""))
    c_stu.alignment = align_left
    c_stu.font = font_regular
    
    c_cou = ws2.cell(row=r, column=12, value=raw_ev.get("輔導室.總務處", ""))
    c_cou.alignment = align_left
    c_cou.font = font_regular
    
    for c_i in range(1, 13):
        c = ws2.cell(row=r, column=c_i)
        c.border = border_all
        if c_i not in [3, 9]:
            c.fill = base_fill

ws2.freeze_panes = f"A{header_row2 + 1}"
col_widths2 = {1: 10, 2: 10, 3: 5, 4: 5, 5: 5, 6: 5, 7: 5, 8: 5, 9: 5, 10: 42, 11: 42, 12: 38}
for col_i, w in col_widths2.items():
    ws2.column_dimensions[get_column_letter(col_i)].width = w


# ==========================================
# Sheet 3: 重大時程速查表 (Key Milestones)
# ==========================================
ws3 = wb.create_sheet(title="重大時程速查")
ws3.views.sheetView[0].showGridLines = True

ws3.merge_cells("A1:E1")
ws3["A1"] = "南投國中 115學年度第一學期 重大校務與考試節日速查表"
ws3["A1"].font = font_title
ws3["A1"].alignment = Alignment(horizontal="left", vertical="center")
ws3.row_dimensions[1].height = 28

headers3 = ["重要分類", "活動/考試名稱", "預定日期 (民國115年/西元)", "週次", "主辦/負責處室"]
header_row3 = 3
ws3.row_dimensions[header_row3].height = 26

for col_idx, h in enumerate(headers3, start=1):
    cell = ws3.cell(row=header_row3, column=col_idx, value=h)
    cell.font = font_header
    cell.fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    cell.alignment = align_center
    cell.border = border_all

milestones = [
    ("開學典禮", "全校開學典禮暨友善校園宣導", "115.08.31 (一)", "第 1 週", "學務處 / 訓育組"),
    ("親師活動", "全校親師座談會", "115.09.19 (六)", "第 3 週", "輔導室 / 總務處"),
    ("國定假日", "中秋節放假", "115.09.25 (五)", "第 4 週", "國定假日"),
    ("國定假日", "國慶日補假", "115.10.09 (五)", "第 6 週", "國定假日"),
    ("定期評量", "第一次段考", "115.10.13 (二) ~ 10.14 (三)", "第 7 週", "教務處 / 學務處"),
    ("校外教學", "三年級戶外教育", "115.10.21 (三) ~ 10.23 (五)", "第 8 週", "學務處 / 訓育組"),
    ("學生體驗", "二年級隔宿露營", "115.10.27 (二) ~ 10.28 (三)", "第 9 週", "學務處 / 訓育組"),
    ("全縣賽會", "南投縣第74屆全縣運動會", "115.11.07 (六) ~ 11.10 (二)", "第 10 週", "學務處 / 體育組"),
    ("定期評量", "第二次段考", "115.12.02 (三) ~ 12.03 (四)", "第 14 週", "教務處 / 學務處"),
    ("全校活動", "全校運動會 (暫定)", "115.12.18 (五)", "第 16 週", "學務處 / 體育組"),
    ("紀念節日", "行憲紀念日", "115.12.25 (五)", "第 17 週", "國定節日"),
    ("國定假日", "中華民國開國紀念日 (元旦)", "116.01.01 (五)", "第 18 週", "國定假日"),
    ("定期評量", "第三次段考", "116.01.18 (一) ~ 01.19 (二)", "第 21 週", "教務處 / 學務處"),
    ("學期結束", "全校大掃除、休業式", "116.01.20 (三)", "第 21 週", "全校"),
    ("寒假假期", "寒假正式開始", "116.01.21 (四)", "-", "全校")
]

for idx, m in enumerate(milestones, start=1):
    r = header_row3 + idx
    ws3.row_dimensions[r].height = 24
    is_zebra = (idx % 2 == 0)
    base_fill = fill_zebra if is_zebra else fill_white

    c1 = ws3.cell(row=r, column=1, value=m[0])
    c1.alignment = align_center
    c1.font = font_bold
    
    c2 = ws3.cell(row=r, column=2, value=m[1])
    c2.alignment = align_left
    c2.font = font_bold
    if "段考" in m[1]:
        c2.font = Font(name="微軟正黑體", size=10, bold=True, color="991B1B")
        c2.fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
    elif "放假" in m[1] or "補假" in m[1] or "元旦" in m[1]:
        c2.font = Font(name="微軟正黑體", size=10, bold=True, color="166534")
        c2.fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
    else:
        c2.fill = base_fill

    c3 = ws3.cell(row=r, column=3, value=m[2])
    c3.alignment = align_center
    c3.font = font_bold
    c3.fill = base_fill

    c4 = ws3.cell(row=r, column=4, value=m[3])
    c4.alignment = align_center
    c4.font = font_regular
    c4.fill = base_fill

    c5 = ws3.cell(row=r, column=5, value=m[4])
    c5.alignment = align_center
    c5.font = font_regular
    c5.fill = base_fill

    for c_i in range(1, 6):
        ws3.cell(row=r, column=c_i).border = border_all
        if c_i != 2 or ("段考" not in m[1] and "放假" not in m[1] and "補假" not in m[1] and "元旦" not in m[1]):
            ws3.cell(row=r, column=c_i).fill = base_fill

col_widths3 = {1: 15, 2: 35, 3: 28, 4: 12, 5: 18}
for col_i, w in col_widths3.items():
    ws3.column_dimensions[get_column_letter(col_i)].width = w

# Save file
excel_filename = "南投國中115學年度第一學期行事曆.xlsx"
wb.save(excel_filename)
print(f"Excel file updated successfully: {excel_filename}")
