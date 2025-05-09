import flet as ft
from core.table_logic import (
    get_default_table,
    update_cell,
    toggle_border_color,
)
from views.table.table_style import (
    get_border_style,
    get_text_alignment,
)

def table_editor_view(page: ft.Page):
    table_data = get_default_table()
    table_column = ft.Column(spacing=0)
    mode_buttons = ft.Container()
    editing_mode = "structure"
    selected_cell = None

    def enable_text_mode(e):
        nonlocal editing_mode
        editing_mode = "text"
        mode_buttons.content = build_mode_buttons()
        table_column.controls = build_table_rows()
        page.update()

    def enable_structure_mode(e):
        nonlocal editing_mode
        editing_mode = "structure"
        mode_buttons.content = build_mode_buttons()
        table_column.controls = build_table_rows()
        page.update()

    def handle_border_toggle(i, j):
        def handler(e):
            nonlocal selected_cell
            if editing_mode != "structure":
                return
            selected_cell = (i, j)
            toggle_border_color(table_data, i, j, direction="top")
            table_column.controls = build_table_rows()
            page.update()
        return handler

    def make_on_change(i, j):
        def handler(e):
            update_cell(table_data, i, j, e.control.value)
        return handler

    def build_table_rows():
        rows = []
        for i, row in enumerate(table_data):
            cells = []
            for j, cell in enumerate(row):
                if not cell.get("visible", True):
                    if editing_mode == "text" and cell.get("editable", False):
                        pass  # 예외: 텍스트 수정 모드에서 수정 가능하면 보여줌
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

    def build_mode_buttons():
        return ft.Row([
            ft.ElevatedButton(
                "📝 텍스트 수정하기",
                on_click=enable_text_mode,
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_100 if editing_mode == "text" else ft.colors.GREY_200)
            ),
            ft.ElevatedButton(
                "🖐️ 구조 수정하기",
                on_click=enable_structure_mode,
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_100 if editing_mode == "structure" else ft.colors.GREY_200)
            )
        ], spacing=10)

    mode_buttons.content = build_mode_buttons()
    table_column.controls = build_table_rows()

    return ft.View(
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("📋 APA Table Editor", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=12),
            mode_buttons,
            ft.Container(
                content=table_column,
                padding=6,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=6
            )
        ]
    )