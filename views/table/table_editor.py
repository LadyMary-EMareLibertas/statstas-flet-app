import flet as ft
from core.table_logic import get_default_table, update_cell
from core.table_exporter import export_table_to_word

def table_editor_view(page: ft.Page):
    table_data = get_default_table()
    selected_borders = []
    table_column = ft.Column(spacing=0)

    def get_ft_color(color_str):
        return ft.colors.BLACK if color_str == "black" else ft.colors.WHITE

    def is_selected_border(i, j, direction):
        return {"row": i, "col": j, "direction": direction} in selected_borders

    def select_border(i, j, direction="top"):
        def handler(e):
            border = {"row": i, "col": j, "direction": direction}
            if border in selected_borders:
                selected_borders.remove(border)
            else:
                selected_borders.append(border)
            print("🔵 Selected borders:", selected_borders)
            table_column.controls = build_table_rows()
            page.update()
        return handler

    def build_table_rows():
        rows = []
        for row_idx, row in enumerate(table_data):
            cells = []
            for col_idx, cell in enumerate(row):
                val = cell.get("value", "") or "\u200B"
                visible = cell.get("visible", True)
                width = cell.get("width", 85)
                highlight_height = 6

                if not visible:
                    cells.append(ft.Container(width=0, height=0))
                    continue

                top_border = cell.get("border_top", {"color": "white", "thickness": 0})
                bottom_border = cell.get("border_bottom", {"color": "white", "thickness": 0})

                border = ft.border.only(
                    top=ft.BorderSide(width=1, color=get_ft_color(top_border["color"])),
                    bottom=ft.BorderSide(width=1, color=get_ft_color(bottom_border["color"]))
                )

                highlight_bar = ft.Container(
                    width=width,
                    height=highlight_height,
                    bgcolor=ft.colors.BLUE_600 if is_selected_border(row_idx, col_idx, "top") else ft.colors.TRANSPARENT,
                    opacity=0.6
                )

                cell = ft.GestureDetector(
                    on_tap=select_border(row_idx, col_idx, "top"),
                    content=ft.Container(
                        width=width,
                        height=36,
                        padding=ft.padding.only(top=0),
                        bgcolor=ft.colors.WHITE,
                        border=border,
                        alignment=ft.alignment.top_center,
                        content=ft.Column([
                            highlight_bar,
                            ft.Text(val, size=12)
                        ])
                    )
                )

                cells.append(cell)
            rows.append(ft.Row(controls=cells, spacing=0))
        return rows

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

    table_column.controls = build_table_rows()

    return ft.View(
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("📋 APA Table Editor", size=26, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_400),
            ft.Container(height=12),
            ft.Container(
                content=table_column,
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
