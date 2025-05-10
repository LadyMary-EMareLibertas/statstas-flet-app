# 셀 객체 생성 함수
def cell(val, align="center", editable=True, top=False, bottom=False, width=85, visible=True):
    return {
        "value": val,
        "align": align,
        "editable": editable,
        "visible": visible,
        "width": width,
        "border_top": {
            "color": "black" if top else "white",
            "thickness": 1
        },
        "border_bottom": {
            "color": "black" if bottom else "white",
            "thickness": 1
        }
    }

# 초기 템플릿 테이블 반환
def get_default_table():
    return [
        [cell("Variable", align="left", top=True),
         cell("Visual", align="left", top=True),
         cell("", align="left", top=True),
         cell("Infrared", align="left", top=True),
         cell("", align="left", top=True),
         cell("F", align="left", top=True),
         cell("η", align="left", top=True)],
        [cell("", align="left", top=False),
         cell("M", align="left", top=True),
         cell("SD", align="left", top=True),
         cell("M", align="left", top=True),
         cell("SD", align="left", top=True),
         cell("", align="left", top=False),
         cell("", align="left", top=False)],
        [cell("Row 1", align="left", top=True),
         cell("3.6", align="left", top=True),
         cell(".49", align="left", top=True),
         cell("9.3", align="left", top=True),
         cell("1.02", align="left", top=True),
         cell("69.9***", align="left", top=True),
         cell(".12", align="left", top=True)],
        [cell("Row 2", align="left", top=False),
         cell("2.4", align="left", top=False),
         cell(".67", align="left", top=False),
         cell("10.1", align="left", top=False),
         cell(".08", align="left", top=False),
         cell("42.7***", align="left", top=False),
         cell(".23", align="left", top=False)],
        [cell("Row 3", align="left", top=False),
         cell("1.2", align="left", top=False),
         cell(".78", align="left", top=False),
         cell("3.6", align="left", top=False),
         cell(".46", align="left", top=False),
         cell("53.9***", align="left", top=False),
         cell(".34", align="left", top=False)],
        [cell("Row 4", align="left", top=False),
         cell("0.8", align="left", top=False),
         cell("93", align="left", top=False),
         cell("4.7", align="left", top=False),
         cell(".71", align="left", top=False),
         cell("21.1***", align="left", top=False),
         cell(".45", align="left", top=False)],
        [cell("***p < .01.", "left", editable=True, width=680, top=True)] +
            [cell("", editable=False, visible=False, top=True) for _ in range(6)]
    ]

# 셀의 값 업데이트
def update_cell(data, row, col, new_value):
    data[row][col]["value"] = new_value
    return data

# 테두리 색상 토글 (흰 ↔ 검)
def toggle_border_color(data, row, col, direction="top"):
    border_key = f"border_{direction}"
    border = data[row][col].get(border_key, {"color": "white", "thickness": 1})
    current = border.get("color", "white")
    data[row][col][border_key] = {
        "color": "black" if current == "white" else "white",
        "thickness": border.get("thickness", 1)
    }
    return data

# 테두리 스타일 추출
def get_border_style(cell, direction):
    return cell.get(f"border_{direction}", {"color": "white", "thickness": 0})

# 텍스트 정렬 문자열을 Flet TextAlign으로 변환
def get_text_alignment(align_str):
    from flet import TextAlign
    return getattr(TextAlign, align_str.upper(), TextAlign.LEFT)

# 행 복사 삽입
def add_row(data, row_index, template_row=None):
    from copy import deepcopy
    if template_row is None:
        template_row = data[row_index]
    new_row = [deepcopy(cell) for cell in template_row]
    data.insert(row_index + 1, new_row)
    return data

# 열 복사 삽입
def add_column(data, col_index, template_column=None):
    from copy import deepcopy
    for i, row in enumerate(data):
        if template_column is None:
            new_cell = deepcopy(row[col_index])
        else:
            new_cell = deepcopy(template_column[i])
        row.insert(col_index + 1, new_cell)
    return data

# 테두리 두께 토글 (1 <-> 2)
def toggle_border_thickness(data, row, col, direction="top"):
    border_key = f"border_{direction}"
    border = data[row][col].get(border_key, {"color": "white", "thickness": 1})
    current_thickness = border.get("thickness", 1)
    data[row][col][border_key] = {
        "color": border.get("color", "white"),
        "thickness": 2 if current_thickness == 1 else 1
    }
    return data