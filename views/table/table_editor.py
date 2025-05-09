import flet as ft

def is_selected_border(i, j, direction, selected_borders):
    return {"row": i, "col": j, "direction": direction} in selected_borders

def border_key(i, j, direction):
    return {"row": i, "col": j, "direction": direction}

def table_editor_view(page: ft.Page):
    table_data = [[{"value": f"R{r}C{c}"} for c in range(5)] for r in range(5)]
    table_column = ft.Column(spacing=0)
    mode_buttons = ft.Container()
    selected_borders = []
    editing_mode = "structure"

    def enable_text_mode(e):
        nonlocal editing_mode
        editing_mode = "text"
        selected_borders.clear()
        mode_buttons.content = build_mode_buttons()
        table_column.controls = build_table_rows()
        page.update()

    def enable_structure_mode(e):
        nonlocal editing_mode
        editing_mode = "structure"
        mode_buttons.content = build_mode_buttons()
        table_column.controls = build_table_rows()
        page.update()

    def toggle_border(i, j, direction):
        def handler(e):
            key = border_key(i, j, direction)
            if key in selected_borders:
                selected_borders.remove(key)
            else:
                selected_borders.append(key)
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
                if is_selected_border(i, j, "top", selected_borders):
                    border = ft.border.only(top=ft.BorderSide(width=1, color=ft.colors.BLUE_600))
                else:
                    border = ft.border.only(top=ft.BorderSide(width=0, color=ft.colors.TRANSPARENT))

                if editing_mode == "text":
                    content = ft.TextField(
                        value=val,
                        text_size=12,
                        height=26,
                        text_align=ft.TextAlign.LEFT,
                        content_padding=ft.padding.symmetric(vertical=2, horizontal=4),
                        border=ft.InputBorder.NONE,
                        bgcolor=ft.colors.TRANSPARENT,
                        on_change=make_on_change(i, j),
                        autofocus=False
                    )
                    cell = ft.Container(
                        width=width,
                        height=42,
                        bgcolor=ft.colors.WHITE,
                        border=border,
                        alignment=ft.alignment.center_left,
                        content=content
                    )
                else:
                    content = ft.Text(val, size=12)
                    cell = ft.GestureDetector(
                        on_tap=toggle_border(i, j, "top"),
                        content=ft.Container(
                            width=width,
                            height=42,
                            bgcolor=ft.colors.WHITE,
                            border=border,
                            alignment=ft.alignment.center_left,
                            content=content
                        )
                    )
                cells.append(cell)
            rows.append(ft.Row(controls=cells, spacing=0))
        return rows

    def build_mode_buttons():
        return ft.Row([
            ft.ElevatedButton(
                "\ud83d\udcdd \ud14d\uc2a4\ud2b8 \uc218\uc815\ud558\uae30",
                on_click=enable_text_mode,
                style=ft.ButtonStyle(bgcolor=ft.colors.BLUE_100 if editing_mode == "text" else ft.colors.GREY_200)
            ),
            ft.ElevatedButton(
                "\ud83d\udd90\ufe0f \uad6c\uc870 \uc218\uc815\ud558\uae30",
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
            ft.Text("\ud83d\udccb APA Table Editor (\ubaa8\ub4dc \ubd84\ub958)", size=24, weight=ft.FontWeight.BOLD),
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
