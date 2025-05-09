import flet as ft
from core.table_logic import get_default_table, update_cell
from core.table_exporter import export_table_to_word

def table_editor_view(page: ft.Page):
    table_data = get_default_table()

    def get_ft_color(color_str):
        return ft.colors.BLACK if color_str == "black" else ft.colors.WHITE

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

                top_border = cell.get("border_top", {"color": "white", "thickness": 0})
                bottom_border = cell.get("border_bottom", {"color": "white", "thickness": 0})

                border = ft.border.only(
                    top=ft.BorderSide(width=top_border["thickness"], color=get_ft_color(top_border["color"]))
                        if top_border["color"] != "white" else None,
                    bottom=ft.BorderSide(width=bottom_border["thickness"], color=get_ft_color(bottom_border["color"]))
                        if bottom_border["color"] != "white" else None
                )

                visible = cell.get("visible", True)
                if not visible:
                    cells.append(ft.Container(width=0, height=0))
                    continue

                width = cell.get("width", 85)
                if is_last_row and col_idx == 0:
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

            row_container = ft.Row(
                controls=cells,
                spacing=0,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
            rows.append(ft.Container(content=row_container))

        return ft.Column(controls=rows, spacing=0)

    def handle_export(e):
        try:
            export_table_to_word(table_data)
            page.snack_bar = ft.SnackBar(
                ft.Text("✅ Word file exported successfully."),
                open=True
            )
        except Exception as ex:
            print("❌ Export error:", ex)
            page.snack_bar = ft.SnackBar(
                ft.Text("❌ Failed to export. Please try again."),
                open=True
            )
        page.update()

    return ft.View(
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text(
                "📋 APA Table Editor",
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
            ft.Row([
                ft.ElevatedButton(
                    text="Export to Word",
                    icon=ft.icons.DOWNLOAD,
                    on_click=handle_export,
                    style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=18, vertical=10))
                ),
                ft.ElevatedButton(
                    text="Back to Home",
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda e: page.go("/"),
                    style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=18, vertical=10))
                )
            ], alignment=ft.MainAxisAlignment.CENTER)
        ]
    )
