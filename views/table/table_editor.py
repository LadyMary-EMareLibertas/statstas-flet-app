import flet as ft
from core.table_logic import get_default_table, update_cell

# ✅ View 내부 상태 초기화용 변수
# (항상 최신 템플릿을 가져오도록 함)

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
                raw_align = cell.get("align", "left").strip().lower()
                if raw_align == "center":
                    align = ft.TextAlign.CENTER
                elif raw_align == "right":
                    align = ft.TextAlign.END
                else:
                    align = ft.TextAlign.START

                editable = cell.get("editable", True)
                top = (row_idx == 0 or row_idx == 2 or (row_idx == 1 and col_idx in {2, 3, 4, 5}))
                bottom = (row_idx == 5)

                if is_last_row:
                    top = False
                    bottom = False
                    border_color = ft.colors.WHITE
                    editable = (col_idx == 0)  # 마지막 줄: 첫 셀만 수정 가능
                else:
                    border_color = ft.colors.BLACK

                border = ft.border.only(
                    top=ft.BorderSide(1, border_color) if top else None,
                    bottom=ft.BorderSide(1, border_color) if bottom else None
                )

                # ✅ 병합처럼 보이게 첫 셀만 넓힘
                width = 95
                if is_last_row and col_idx == 0:
                    width = 95 * len(row)

                if editable:
                    content = ft.TextField(
                        value=val,
                        dense=True,
                        height=36,
                        width=width,
                        text_align=align,
                        text_size=13,
                        border=ft.InputBorder.NONE,
                        filled=False,
                        bgcolor=None,
                        on_change=make_on_change(row_idx, col_idx)
                    )
                else:
                    content = ft.Text(val, text_align=align, size=13)

                cells.append(
                    ft.Container(
                        content=content,
                        padding=ft.padding.symmetric(horizontal=4, vertical=2),
                        width=width,
                        bgcolor=ft.colors.WHITE,
                        border=border
                    )
                )

            rows.append(ft.Container(content=ft.Row(controls=cells, spacing=0)))

        return ft.Column(controls=rows, spacing=0)

    return ft.View(
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text(
                "📋 APA Table Template",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_400
            ),
            ft.Container(height=20),
            ft.Container(
                content=build_template_table(),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=6
            ),
            ft.Container(height=30),
            ft.ElevatedButton(
                text="Back",
                icon=ft.icons.ARROW_BACK,
                on_click=lambda e: (page.views.pop(), page.go("/")),
                style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=20, vertical=12))
            )
        ]
    )