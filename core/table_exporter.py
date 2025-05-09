import os
from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.shared import Pt

def export_table_to_word(table_data, filename="exports/table_export_test.docx"):
    print("🟢 Export started...")

    os.makedirs("exports", exist_ok=True)
    doc = Document()

    n_rows = len(table_data)
    n_cols = len(table_data[0]) if n_rows > 0 else 0
    table = doc.add_table(rows=n_rows, cols=n_cols)
    table.style = 'Table Grid'

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

            # 스타일 (APA용 기본값)
            run = doc_cell.paragraphs[0].runs[0]
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)

    doc.save(filename)
    print(f"✅ Exported to {filename}")

    # ✅ macOS에서 Word 자동 실행
    os.system(f"open '{filename}'")