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

        def row_action(label, handler_func):
            return ft.ElevatedButton(
                label,
                on_click=lambda e: handler_func(
                    state.table_data,
                    state.selected_cell,
                    ui["table_column"],
                    lambda: build_table_rows(
                        state,
                        handle_border_toggle(state, ui, page),
                        make_on_change(state)
                    ),
                    page
                ) if state.selected_cell else None
            )

        structure_row = ft.Row([
            row_action("➕ Add Row", handle_add_row),
            row_action("➖ Delete Row", handle_delete_row),
            ft.ElevatedButton("↩️ Undo", on_click=lambda e: None),
        ], spacing=10)

        column_row = ft.Row([
            row_action("➕ Add Column", handle_add_column),
            row_action("➖ Delete Column", handle_delete_column),
            ft.ElevatedButton("🔄 Reverse Undo", on_click=lambda e: None),
            row_action("🔳 Toggle Bold Line", handle_toggle_bold),
        ], spacing=10)

        return [ft.Column([structure_row, column_row], spacing=10)]

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