import flet as ft
# 셀 테두리 스타일 및 텍스트 정렬 함수 불러오기
from table.logic.style import get_border_style, get_text_alignment
# 편집 모드 종류 (텍스트 편집 / 구조 편집) 상수 불러오기
from table.logic.state import TEXT_MODE, STRUCTURE_MODE

# 하나의 셀을 렌더링하는 함수
def render_cell(cell, i, j, state, ui, page, handle_border_toggle, make_on_change):
    # 셀 표시 여부 체크: 숨겨진 셀은 None 또는 빈 박스로 처리함
    if not cell.get("visible", True):
        # 텍스트 편집 모드이고, 편집 가능한 셀일 경우만 예외 허용
        if state.editing_mode == TEXT_MODE and cell.get("editable", False):
            pass  # 렌더링 계속 진행함
        else:
            # 완전히 숨김 처리
            return ft.Container(width=0, height=0)

    # 셀의 텍스트 값, 너비, 테두리 스타일, 정렬 방식, 편집 가능 여부 추출
    val = cell.get("value", "")
    width = cell.get("width", 85)
    border_top = dict(get_border_style(cell, "top"))
    border_bottom = dict(get_border_style(cell, "bottom"))
    align = cell.get("align", "left")
    editable = cell.get("editable", True)

    # 테두리 스타일 생성 (상단, 하단만 사용)
    border = ft.border.only(
        top=ft.BorderSide(width=border_top["thickness"], color=getattr(ft.colors, border_top["color"].upper(), ft.colors.TRANSPARENT)),
        bottom=ft.BorderSide(width=border_bottom["thickness"], color=getattr(ft.colors, border_bottom["color"].upper(), ft.colors.TRANSPARENT))
    )

    # 텍스트 편집 모드 & 편집 가능한 셀일 경우: TextField로 렌더링
    if state.editing_mode == TEXT_MODE and editable:
        return ft.Container(
            width=width,
            height=42,
            bgcolor=ft.colors.WHITE,
            border=border,
            alignment=ft.alignment.center_left,
            content=ft.TextField(
                value=val,
                text_size=12,
                height=26,
                text_align=get_text_alignment(align),
                content_padding=ft.padding.symmetric(vertical=2, horizontal=4),
                border=ft.InputBorder.NONE,
                bgcolor=ft.colors.TRANSPARENT,
                on_change=make_on_change(state, ui, page)(i, j),  # 값 변경 시 호출될 콜백 등록
                autofocus=False
            )
        )
    else:
        # 구조 편집 모드에서 선택된 셀인지 여부 확인
        is_selected = (state.editing_mode == STRUCTURE_MODE and state.selected_cell == (i, j))
        # 셀 클릭 시 테두리 토글 처리 (GestureDetector 사용)
        return ft.GestureDetector(
            on_tap=handle_border_toggle(state, ui, page)(i, j),
            content=ft.Container(
                width=width,
                height=42,
                bgcolor=ft.colors.CYAN_100 if is_selected else ft.colors.WHITE,
                border=border,
                alignment=ft.alignment.center,
                content=ft.Text(val, size=12)
            )
        )

# 전체 테이블을 행 단위로 렌더링하는 함수
def build_table_rows(state, ui, page, handle_border_toggle, make_on_change):
    rows = []  # 화면에 들어갈 전체 Row 리스트
    for i, row in enumerate(state.table_data["rows"]):  # 행마다 반복
        row_controls = []
        for j, cell in enumerate(row["cells"]):  # 각 셀마다 반복
            # 각 셀을 렌더링해서 리스트에 추가
            row_controls.append(render_cell(
                cell, i, j, state, ui, page, handle_border_toggle, make_on_change
            ))
        # 완성된 한 행(Row)을 리스트에 추가
        rows.append(ft.Row(controls=row_controls, spacing=0))
    return rows  # 최종적으로 테이블 전체 반환