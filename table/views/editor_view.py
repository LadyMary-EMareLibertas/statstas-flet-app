from table.core.exporter import export_table_to_word
import flet as ft
from table.logic.structure import (
    update_cell,
    toggle_border_color,
)
from table.logic.template import get_default_table
from table.logic.style import (
    get_border_style,
    get_text_alignment,
)
from table.logic.ui_state import *


def table_editor_view(page: ft.Page):  # 메인 테이블 편집기 뷰 함수
    table_data = get_default_table()  # 표 데이터 구조 초기화
    table_column = ft.Column(spacing=0)  # 테이블 행들을 수직으로 배치할 컬럼
    mode_buttons = ft.Container()  # 모드 전환 버튼이 들어갈 컨테이너
    editing_mode = "structure"  # 초기 모드는 구조 수정 모드
    selected_cell = None  # 선택된 셀 (i, j 좌표)

    def enable_text_mode(e):  # 텍스트 수정 모드로 전환
        nonlocal editing_mode
        editing_mode = "text"
        mode_buttons.content = build_mode_buttons()
        table_column.controls = build_table_rows()
        page.update()

    def enable_structure_mode(e):  # 구조 수정 모드로 전환
        nonlocal editing_mode
        editing_mode = "structure"
        mode_buttons.content = build_mode_buttons()
        table_column.controls = build_table_rows()
        page.update()

    def handle_border_toggle(i, j):  # 셀 클릭 시 테두리 토글 핸들러
        def handler(e):
            nonlocal selected_cell
            if editing_mode != "structure":
                return
            selected_cell = (i, j)
            toggle_border_color(table_data, i, j, direction="top")
            table_column.controls = build_table_rows()
            page.update()
        return handler

    def make_on_change(i, j):  # 텍스트 입력 시 셀 값 업데이트 핸들러
        def handler(e):
            update_cell(table_data, i, j, e.control.value)
        return handler

    def build_table_rows():  # 현재 상태에 따라 테이블 행 전체를 구성
        rows = []
        for i, row in enumerate(table_data):
            cells = []
            for j, cell in enumerate(row):
                if not cell.get("visible", True):
                    if editing_mode == "text" and cell.get("editable", False):
                        pass
                    else:
                        cells.append(ft.Container(width=0, height=0))
                        continue

                val = cell.get("value", "")
                width = cell.get("width", 85)
                border_top = get_border_style(cell, "top")
                border_bottom = get_border_style(cell, "bottom")
                align = cell.get("align", "left")
                editable = cell.get("editable", True)

                border = ft.border.only(
                    top=ft.BorderSide(width=border_top["thickness"], color=getattr(ft.colors, border_top["color"].upper(), ft.colors.TRANSPARENT)),
                    bottom=ft.BorderSide(width=border_bottom["thickness"], color=getattr(ft.colors, border_bottom["color"].upper(), ft.colors.TRANSPARENT))
                )

                if editing_mode == "text" and editable:
                    content = ft.TextField(
                        value=val,
                        text_size=12,
                        height=26,
                        text_align=get_text_alignment(align),
                        content_padding=ft.padding.symmetric(vertical=2, horizontal=4),
                        border=ft.InputBorder.NONE,
                        bgcolor=ft.colors.TRANSPARENT,
                        on_change=make_on_change(i, j),
                        autofocus=False
                    )
                    cell_container = ft.Container(
                        width=width,
                        height=42,
                        bgcolor=ft.colors.WHITE,
                        border=border,
                        alignment=ft.alignment.center_left,
                        content=content
                    )
                else:
                    content = ft.Text(val, size=12, text_align=get_text_alignment(align))
                    is_selected = (editing_mode == "structure" and selected_cell == (i, j))
                    cell_container = ft.GestureDetector(
                        on_tap=handle_border_toggle(i, j),
                        content=ft.Container(
                            width=width,
                            height=42,
                            bgcolor=ft.colors.BLUE_100 if is_selected else ft.colors.WHITE,
                            border=border,
                            alignment=ft.alignment.center_left,
                            content=content
                        )
                    )

                cells.append(cell_container)
            rows.append(ft.Row(controls=cells, spacing=0))
        return rows

    def build_mode_buttons():  # 텍스트/구조 전환 버튼 UI 생성
        return ft.Row([
            ft.ElevatedButton(
                "Edit Text",
                on_click=enable_text_mode,
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_100 if editing_mode == "text" else ft.colors.GREY_200)
            ),
            ft.ElevatedButton(
                "Edit Structure",
                on_click=enable_structure_mode,
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_100 if editing_mode == "structure" else ft.colors.GREY_200)
            )
        ], spacing=10)

    mode_buttons.content = build_mode_buttons()
    table_column.controls = build_table_rows()

    tools_column = []
    if editing_mode == "structure":
        tools_column.append(
            ft.Column([
                ft.Row([
                    ft.ElevatedButton("➕ Add Row", on_click=lambda e: handle_add_row(table_data, selected_cell, table_column, build_table_rows, page)),
                    ft.ElevatedButton("➖ Delete Row", on_click=lambda e: handle_delete_row(table_data, selected_cell, table_column, build_table_rows, page)),
                    ft.ElevatedButton("↩️ Undo", on_click=lambda e: None),
                ], spacing=10),
                ft.Row([
                    ft.ElevatedButton("➕ Add Column", on_click=lambda e: handle_add_column(table_data, selected_cell, table_column, build_table_rows, page)),
                    ft.ElevatedButton("➖ Delete Column", on_click=lambda e: handle_delete_column(table_data, selected_cell, table_column, build_table_rows, page)),
                    ft.ElevatedButton("🔄 Reverse Undo", on_click=lambda e: None),
                    ft.ElevatedButton("🔳 Toggle Bold Line", on_click=lambda e: handle_toggle_bold(table_data, selected_cell, table_column, build_table_rows, page)),
                ], spacing=10)
            ], spacing=10)
        )

    return ft.View(  # 최종적으로 전체 뷰를 반환
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("APA Table Editor", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_400),
            ft.Text("StatStas does not support font settings or text alignment.\n"
                    "Please export your table to Word and complete the final formatting there.\n"
                    "Lines that look slightly misaligned in the editor will be cleanly aligned in the exported document.",
                    size=12, color=ft.colors.GREY_600, italic=True),
            ft.Container(height=12),
            mode_buttons,
            *tools_column,
            ft.Container(
                content=table_column,
                padding=6,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=6
            ),
            ft.Row([
                ft.ElevatedButton("⬅️ Back", on_click=lambda e: page.go("/"), style=ft.ButtonStyle(bgcolor=ft.colors.GREY_200)),
                ft.Container(expand=True),
                ft.ElevatedButton("📤 Export to Word", on_click=lambda e: export_table_to_word(table_data), style=ft.ButtonStyle(bgcolor=ft.colors.CYAN_200))
            ])
        ]
    )