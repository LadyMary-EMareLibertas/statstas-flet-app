import flet as ft
from core.table_logic import get_default_table, update_cell

# ✅ 텍스트 기반 APA 스타일 테이블 뷰 (수정 기능 포함, 줄바꿈, 가운데 정렬, 병합 시뮬레이션)
def table_editor_view(page: ft.Page):
    table_data = get_default_table()

    def build_template_table():
        rows = []

        def make_on_change(i, j):
            def handler(e):
                update_cell(table_data, i, j, e.control.value)
                page.update()
            return handler

        for row_idx, row in enumerate(table_data):
            cells = []
            is_last_row = (row_idx == len(table_data) - 1)

            for col_idx, cell in enumerate(row):
                val = cell.get("value", "")
                align = ft.TextAlign.START if is_last_row else ft.TextAlign.CENTER

                editable = cell.get("editable", True)
                top = (row_idx == 0 or row_idx == 2 or (row_idx == 1 and col_idx in {2, 3, 4, 5}))
                bottom = (row_idx == 5)

                if is_last_row:
                    top = False
                    bottom = False
                    border_color = ft.colors.WHITE
                else:
                    border_color = ft.colors.BLACK

                border = ft.border.only(
                    top=ft.BorderSide(1, border_color) if top else None,
                    bottom=ft.BorderSide(1, border_color) if bottom else None
                )

                # ✅ 병합 시뮬레이션: 첫 셀만 전체 너비로 확장, 나머지는 None 처리
                if is_last_row:
                    if col_idx == 0:
                        width = 85 * len(row)
                        content = ft.TextField(
                            value=val,
                            multiline=True,
                            min_lines=1,
                            max_lines=6,
                            text_align=align,
                            text_size=12,
                            border=ft.InputBorder.NONE,
                            filled=False,
                            bgcolor=None,
                            content_padding=ft.padding.symmetric(horizontal=1, vertical=0),
                            on_change=make_on_change(row_idx, col_idx)
                        )
                        cell_container = ft.Container(
                            content=content,
                            padding=ft.padding.symmetric(horizontal=1, vertical=0),
                            width=width,
                            expand=True,
                            bgcolor=ft.colors.WHITE,
                            border=border,
                            alignment=ft.alignment.top_left
                        )
                        cells.append(cell_container)
                    else:
                        cells.append(ft.Container(width=0, height=0))
                else:
                    width = 85
                    if editable:
                        content = ft.TextField(
                            value=val,
                            multiline=True,
                            min_lines=1,
                            max_lines=6,
                            text_align=align,
                            text_size=12,
                            border=ft.InputBorder.NONE,
                            filled=False,
                            bgcolor=None,
                            content_padding=ft.padding.symmetric(horizontal=1, vertical=0),
                            on_change=make_on_change(row_idx, col_idx)
                        )
                    else:
                        content = ft.Text(val, text_align=align, size=12)

                    cell_container = ft.Container(
                        content=content,
                        padding=ft.padding.symmetric(horizontal=1, vertical=0),
                        width=width,
                        expand=True,
                        bgcolor=ft.colors.WHITE,
                        border=border,
                        alignment=ft.alignment.top_left
                    )
                    cells.append(cell_container)

            row_container = ft.Row(
                controls=cells,
                spacing=0,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
            rows.append(ft.Container(content=row_container))

        return ft.Column(controls=rows, spacing=0)

    return ft.View(
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text(
                "📋 APA Table Template",
                size=26,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_400
            ),
            ft.Container(height=12),
            ft.Container(
                content=build_template_table(),
                padding=6,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=6
            ),
            ft.Container(height=16),
            ft.ElevatedButton(
                text="Back",
                icon=ft.icons.ARROW_BACK,
                on_click=lambda e: page.go("/"),
                style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=18, vertical=10))
            )
        ]
    )