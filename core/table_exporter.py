import os
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_apa_paragraph_style(paragraph):
    paragraph.paragraph_format.line_spacing = Pt(12)
    run = paragraph.runs[0]
    run.font.name = "Times New Roman"
    run.font.size = Pt(11)

def set_cell_border(cell, top=False, bottom=False):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')

    if top:
        top_el = OxmlElement('w:top')
        top_el.set(qn('w:val'), 'single')
        top_el.set(qn('w:sz'), '4')  # 0.5pt
        top_el.set(qn('w:color'), '000000')
        tcBorders.append(top_el)

    if bottom:
        bottom_el = OxmlElement('w:bottom')
        bottom_el.set(qn('w:val'), 'single')
        bottom_el.set(qn('w:sz'), '4')
        bottom_el.set(qn('w:color'), '000000')
        tcBorders.append(bottom_el)

    tcPr.append(tcBorders)

def export_table_to_word(table_data, filename="exports/table_export_test.docx"):
    print("🟢 Export started...")
    os.makedirs("exports", exist_ok=True)

    doc = Document()
    n_rows = len(table_data)
    n_cols = len(table_data[0]) if n_rows > 0 else 0

    table = doc.add_table(rows=n_rows, cols=n_cols)
    table.autofit = True

    for i, row in enumerate(table_data):
        for j, cell in enumerate(row):
            val = str(cell.get("value", ""))
            doc_cell = table.cell(i, j)
            doc_cell.text = val

            # 정렬
            if val.replace(".", "", 1).isdigit():
                doc_cell.paragraphs[0].alignment = 1  # CENTER
            else:
                doc_cell.paragraphs[0].alignment = 0  # LEFT

            doc_cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

            # 스타일 적용
            set_apa_paragraph_style(doc_cell.paragraphs[0])

            # 선 처리
            top = (i == 0 or i == 2)
            bottom = (i == n_rows - 2)
            set_cell_border(doc_cell, top=top, bottom=bottom)

    # 마지막 행 병합 처리 (각주용)
    if n_rows > 0:
        merged = table.cell(n_rows - 1, 0)
        for j in range(1, n_cols):
            merged = merged.merge(table.cell(n_rows - 1, j))

    doc.save(filename)
    print(f"✅ Exported to {filename}")
    os.system(f"open '{filename}'")  # macOS Word 실행