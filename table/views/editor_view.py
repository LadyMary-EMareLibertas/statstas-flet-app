import flet as ft
from table.core.exporter import export_table_to_word
from table.logic.state import TableEditorState
from table.logic.handlers import (
    enable_text_mode, enable_structure_mode, handle_border_toggle, make_on_change
)
from table.logic.table_renderer import build_table_rows
from table.views.mode_buttons import build_mode_buttons
from table.views.footer import footer_section

def table_editor_view(page: ft.Page):
    state = TableEditorState()
    ui = {
        "table_column": ft.Column(spacing=0),
        "mode_buttons": ft.Container()
    }

    def rebuild():
        ui["mode_buttons"].content = build_mode_buttons(
            state.editing_mode,
            enable_text_mode(state, ui, page),
            enable_structure_mode(state, ui, page)
        )
        ui["table_column"].controls = build_table_rows(
            state,
            handle_border_toggle(state, ui, page),
            make_on_change(state)
        )

    rebuild()

    def build_tools():
        if state.editing_mode != "structure":
            return []
        return [
            ft.Column([
                ft.Row([
                    ft.ElevatedButton("➕ Add Row", on_click=lambda e: handle_add_row(state.table_data, state.selected_cell, ui["table_column"], lambda: build_table_rows(state, handle_border_toggle(state, ui, page), make_on_change(state)), page) if state.selected_cell else None),
                    ft.ElevatedButton("➖ Delete Row", on_click=lambda e: handle_delete_row(state.table_data, state.selected_cell, ui["table_column"], lambda: build_table_rows(state, handle_border_toggle(state, ui, page), make_on_change(state)), page) if state.selected_cell else None),
                    ft.ElevatedButton("↩️ Undo", on_click=lambda e: None),
                ], spacing=10),
                ft.Row([
                    ft.ElevatedButton("➕ Add Column", on_click=lambda e: handle_add_column(state.table_data, state.selected_cell, ui["table_column"], lambda: build_table_rows(state, handle_border_toggle(state, ui, page), make_on_change(state)), page) if state.selected_cell else None),
                    ft.ElevatedButton("➖ Delete Column", on_click=lambda e: handle_delete_column(state.table_data, state.selected_cell, ui["table_column"], lambda: build_table_rows(state, handle_border_toggle(state, ui, page), make_on_change(state)), page) if state.selected_cell else None),
                    ft.ElevatedButton("🔄 Reverse Undo", on_click=lambda e: None),
                    ft.ElevatedButton("🔳 Toggle Bold Line", on_click=lambda e: handle_toggle_bold(state.table_data, state.selected_cell, ui["table_column"], lambda: build_table_rows(state, handle_border_toggle(state, ui, page), make_on_change(state)), page) if state.selected_cell else None),
                ], spacing=10)
            ], spacing=10)
        ]

    return ft.View(
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("APA Table Editor", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_400),
            ft.Text(
                "StatStas does not support font settings or text alignment. Please export your table to Word and complete the final formatting there. Lines that look slightly misaligned in the editor will be cleanly aligned in the exported document.",
                size=12, color=ft.colors.GREY_600, italic=True
            ),
            ft.Container(height=12),
            ui["mode_buttons"],
            *build_tools(),
            ft.Container(
                content=ui["table_column"],
                padding=6,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=6
            ),
            ft.Container(height=24),
            footer_section(page, state.table_data)
        ]
    )
