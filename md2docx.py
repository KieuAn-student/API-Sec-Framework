import docx
import os
import re

doc = docx.Document()

# Mở file markdown
md_path = r"C:\Users\admin\.gemini\antigravity\brain\35b7362e-1321-4cea-a3e4-0758916bd93c\docs\final_report.md"
with open(md_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

in_table = False
table_data = []

def clean_markdown(text):
    # Xóa ký tự bold
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    # Xóa ký tự italic
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    # Xóa backtick code
    text = re.sub(r'(.*?)', r'\1', text)
    return text

for i, line in enumerate(lines):
    line_strip = line.strip()
    if not line_strip:
        if in_table:
            table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
            table.style = 'Table Grid'
            for r, row_data in enumerate(table_data):
                for c, cell_data in enumerate(row_data):
                    table.cell(r, c).text = clean_markdown(cell_data)
            in_table = False
            table_data = []
        continue
    
    # Bỏ qua dòng phân cách bảng
    if in_table and "---" in line_strip:
        continue
        
    if line_strip.startswith("|"):
        in_table = True
        row = [cell.strip() for cell in line_strip.split("|")[1:-1]]
        if "---" not in line_strip:
            table_data.append(row)
        continue
    else:
        if in_table:
            # Table ended but without empty line
            table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
            table.style = 'Table Grid'
            for r, row_data in enumerate(table_data):
                for c, cell_data in enumerate(row_data):
                    table.cell(r, c).text = clean_markdown(cell_data)
            in_table = False
            table_data = []
            
        if line_strip.startswith("# "):
            doc.add_heading(clean_markdown(line_strip[2:]), 0)
        elif line_strip.startswith("## "):
            doc.add_heading(clean_markdown(line_strip[3:]), 1)
        elif line_strip.startswith("### "):
            doc.add_heading(clean_markdown(line_strip[4:]), 2)
        elif line_strip.startswith("- "):
            doc.add_paragraph(clean_markdown(line_strip[2:]), style='List Bullet')
        elif re.match(r'^\d+\. ', line_strip):
            # Lấy text sau số
            text = re.sub(r'^\d+\. ', '', line_strip)
            doc.add_paragraph(clean_markdown(text), style='List Number')
        elif line_strip.startswith("`"):
            pass
        elif line_strip.startswith("{") or line_strip.startswith("}") or line_strip.startswith('"'):
            p = doc.add_paragraph(line_strip)
            p.style = 'No Spacing'
        else:
            doc.add_paragraph(clean_markdown(line_strip))

# Flush final table if EOF reached
if in_table and table_data:
    table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
    table.style = 'Table Grid'
    for r, row_data in enumerate(table_data):
        for c, cell_data in enumerate(row_data):
            table.cell(r, c).text = clean_markdown(cell_data)

doc.save(r"C:\Users\admin\.gemini\antigravity\scratch\API-Sec-Framework\Bao_Cao_Do_An_Chi_Tiet.docx")
print("Saved DOCX")

