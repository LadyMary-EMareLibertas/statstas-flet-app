# 셀 객체 생성 함수: 텍스트 값, 정렬, 편집 가능 여부, 테두리 색/두께 등 설정
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
        [cell("", "left"), cell("M", bottom=True), cell("SD", bottom=True), cell("M", bottom=True),
         cell("SD", bottom=True), cell("", bottom=True), cell("", bottom=True)],
        [cell("Row 1", "left"), cell("3.6"), cell(".49"), cell("9.2"), cell("1.02"), cell("69.9***"), cell(".12")],
        [cell("Row 2", "left"), cell("2.4"), cell(".67"), cell("10.1"), cell(".08"), cell("42.7***"), cell(".23")],
        [cell("Row 3", "left"), cell("1.2"), cell(".78"), cell("3.6"), cell(".46"), cell("53.9***"), cell(".34")],
        [cell("Row 4", "left"), cell("0.8"), cell(".93"), cell("4.7"), cell(".71"), cell("21.1***"), cell(".45", bottom=True)],
        [cell("***p < .01.", "left", editable=True, width=680)] + [cell("", editable=False, visible=False) for _ in range(6)]
    ]

# 셀의 텍스트 값 업데이트
def update_cell(data, row, col, new_value):
    data[row][col]["value"] = new_value
    return data

# 셀의 테두리 색상 토글 (흰색 <-> 검정)
def toggle_border_color(data, row, col, direction="top"):
    border_key = f"border_{direction}"
    border = data[row][col].get(border_key, {"color": "white", "thickness": 1})
    current = border.get("color", "white")
    data[row][col][border_key] = {
        "color": "black" if current == "white" else "white",
        "thickness": border.get("thickness", 1)
    }
    return data

# 테두리 스타일 불러오기 (없을 경우 기본값 반환)
def get_border_style(cell, direction):
    return cell.get(f"border_{direction}", {"color": "white", "thickness": 0})

# 정렬 문자열을 Flet 정렬 열거형으로 변환
def get_text_alignment(align_str):
    from flet import TextAlign
    return getattr(TextAlign, align_str.upper(), TextAlign.LEFT)

# 선택된 행 아래에 새 행 추가
def add_row(data, row_index, template_row=None):
    """Insert new row below the given row index."""
    from copy import deepcopy
    if template_row is None:
        template_row = data[row_index]
    new_row = [deepcopy(cell) for cell in template_row]
    data.insert(row_index + 1, new_row)
    return data

# 선택된 열 오른쪽에 새 열 추가
def add_column(data, col_index, template_column=None):
    """Insert new column to the right of the given column index."""
    from copy import deepcopy
    for i, row in enumerate(data):
        if template_column is None:
            new_cell = deepcopy(row[col_index])
        else:
            new_cell = deepcopy(template_column[i])
        row.insert(col_index + 1, new_cell)
    return data

# 셀 테두리 두께 토글 (1 <-> 2)
def toggle_border_thickness(data, row, col, direction="top"):
    """Toggle the thickness of a cell border between 1 and 2."""
    border_key = f"border_{direction}"
    border = data[row][col].get(border_key, {"color": "white", "thickness": 1})
    current_thickness = border.get("thickness", 1)
    data[row][col][border_key] = {
        "color": border.get("color", "white"),
        "thickness": 2 if current_thickness == 1 else 1
    }
    return data