import flet as ft
from core.table_logic import get_default_table

# ✅ 텍스트만 보여주는 템플릿 뷰 버전 (수정 불가)
table_data = get_default_table()

def table_editor_view(page: ft.Page):
    def build_safe_table():
        rows = []

        for row_idx, row in enumerate(table_data):
            cells = []
            for col_idx, cell in enumerate(row):
                val = cell.get("value", "")
                raw_align = cell.get("align", "left").strip().lower()
                if raw_align == "center":
                    align = ft.TextAlign.CENTER
                elif raw_align == "right":
                    align = ft.TextAlign.END
                else:
                    align = ft.TextAlign.START

                top = cell.get("border_top", False)
                bottom = cell.get("border_bottom", False)

                border = ft.border.only(
                    top=ft.BorderSide(1, ft.colors.BLACK) if top else None,
                    bottom=ft.BorderSide(1, ft.colors.BLACK) if bottom else None
                )

                content = ft.Text(val, text_align=align, size=13)

                cells.append(
                    ft.Container(
                        content=content,
                        padding=ft.padding.symmetric(horizontal=4, vertical=2),
                        width=95,
                        bgcolor=ft.colors.WHITE,
                        border=border
                    )
                )

            row_container = ft.Container(
                content=ft.Row(controls=cells, spacing=0)
            )
            rows.append(row_container)

        return ft.Column(controls=rows, spacing=0)

    return ft.View(
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("📋 APA Table Template", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_400),
            ft.Container(height=20),
            ft.Container(
                content=build_safe_table(),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=6
            ),
            ft.Container(height=30),
            ft.ElevatedButton(
                text="Back",
                icon=ft.icons.ARROW_BACK,
                on_click=lambda e: page.go("/"),
                style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=20, vertical=12))
            )
        ]
    )