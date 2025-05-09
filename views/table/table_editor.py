import flet as ft

# 상태 변수
active_cell = None  # 현재 텍스트 편집 중인 셀 (row, col)
selected_borders = []  # 선택된 구조선 리스트

def is_selected_border(i, j, direction):
    return {"row": i, "col": j, "direction": direction} in selected_borders

def border_key(i, j, direction):
    return {"row": i, "col": j, "direction": direction}

def table_editor_view(page: ft.Page):
    global active_cell
    table_data = [[{"value": f"R{r}C{c}"} for c in range(5)] for r in range(5)]
    table_column = ft.Column(spacing=0)

    def toggle_cell_action(i, j):
        def handler(e):
            global active_cell
            if active_cell == (i, j):
                key = border_key(i, j, "top")
                if key in selected_borders:
                    selected_borders.remove(key)
                else:
                    selected_borders.append(key)
                active_cell = None
            else:
                active_cell = (i, j)
            table_column.controls = build_table_rows()
            page.update()
        return handler

    def make_on_change(i, j):
        def handler(e):
            table_data[i][j]["value"] = e.control.value
        return handler

    def build_table_rows():
        rows = []
        for i, row in enumerate(table_data):
            cells = []
            for j, cell in enumerate(row):
                val = cell.get("value", "")
                width = 85

                key = border_key(i, j, "top")
                if is_selected_border(i, j, "top"):
                    border = ft.border.only(top=ft.BorderSide(width=1, color=ft.colors.BLUE_600))
                else:
                    border = ft.border.only(top=ft.BorderSide(width=0, color=ft.colors.TRANSPARENT))

                if active_cell == (i, j):
                    content = ft.TextField(
                        value=val,
                        text_size=12,
                        height=24,
                        content_padding=ft.padding.symmetric(horizontal=4, vertical=2),
                        border=ft.InputBorder.NONE,
                        bgcolor=ft.colors.TRANSPARENT,
                        on_change=make_on_change(i, j),
                        autofocus=True
                    )
                else:
                    content = ft.Text(val, size=12)

                cell = ft.GestureDetector(
                    on_tap=toggle_cell_action(i, j),
                    content=ft.Container(
                        width=width,
                        height=42,
                        bgcolor=ft.colors.WHITE,
                        border=border,
                        alignment=ft.alignment.center,
                        content=content
                    )
                )
                cells.append(cell)
            rows.append(ft.Row(controls=cells, spacing=0))
        return rows

    table_column.controls = build_table_rows()

    return ft.View(
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("\ud83d\udccb APA Table Editor (토글 방식)", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=12),
            ft.Container(
                content=table_column,
                padding=6,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=6
            )
        ]
    )
