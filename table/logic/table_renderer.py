import flet as ft
from table.logic.style import get_border_style, get_text_alignment
from table.logic.state import TEXT_MODE, STRUCTURE_MODE

def render_cell(cell, i, j, state, ui, page, handle_border_toggle, make_on_change):
    if not cell.get("visible", True):
        if state.editing_mode == TEXT_MODE and cell.get("editable", False):
            pass
        else:
            return ft.Container(width=0, height=0)

    val = cell.get("value", "")
    width = cell.get("width", 85)
    border_top = dict(get_border_style(cell, "top"))
    border_bottom = dict(get_border_style(cell, "bottom"))
    align = cell.get("align", "left")
    editable = cell.get("editable", True)

    border = ft.border.only(
        top=ft.BorderSide(width=border_top["thickness"], color=getattr(ft.colors, border_top["color"].upper(), ft.colors.TRANSPARENT)),
        bottom=ft.BorderSide(width=border_bottom["thickness"], color=getattr(ft.colors, border_bottom["color"].upper(), ft.colors.TRANSPARENT))
    )

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
                on_change=make_on_change(state, ui, page)(i, j),
                autofocus=False
            )
        )
    else:
        is_selected = (state.editing_mode == STRUCTURE_MODE and state.selected_cell == (i, j))
        return ft.GestureDetector(
            on_tap=handle_border_toggle(state, ui, page)(i, j),
            content=ft.Container(
                width=width,
                height=42,
                bgcolor=ft.colors.BLUE_100 if is_selected else ft.colors.WHITE,
                border=border,
                alignment=ft.alignment.center_left,
                content=ft.Text(val, size=12, text_align=get_text_alignment(align))
            )
        )

def build_table_rows(state, ui, page, handle_border_toggle, make_on_change):
    rows = []
    for i, row in enumerate(state.table_data):
        cells = [
            render_cell(cell, i, j, state, ui, page, handle_border_toggle, make_on_change)
            for j, cell in enumerate(row)
        ]
        rows.append(ft.Row(controls=cells, spacing=0))
    return rows