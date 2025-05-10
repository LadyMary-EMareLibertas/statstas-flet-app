import flet as ft
from table.logic.table_renderer import build_table_rows
from table.logic.state import TEXT_MODE, STRUCTURE_MODE

def enable_text_mode(state, ui, page):
    def handler(e):
        from table.views.mode_buttons import build_mode_buttons
        from table.logic.handlers import enable_structure_mode

        state.editing_mode = TEXT_MODE
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
        page.update()
    return handler

def enable_structure_mode(state, ui, page):
    def handler(e):
        from table.views.mode_buttons import build_mode_buttons
        from table.logic.handlers import enable_text_mode

        state.editing_mode = STRUCTURE_MODE
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
        page.update()
    return handler

def handle_border_toggle(state, ui, page):
    def wrapper(i, j):
        def handler(e):
            if state.editing_mode != STRUCTURE_MODE:
                return
            state.selected_cell = (i, j)
            from table.logic.structure import toggle_border_color
            toggle_border_color(state.table_data, i, j, direction="top")
            ui["table_column"].controls = build_table_rows(
                state,
                handle_border_toggle(state, ui, page),
                make_on_change(state)
            )
            page.update()
        return handler
    return wrapper

def make_on_change(state):
    def wrapper(i, j):
        def handler(e):
            from table.logic.structure import update_cell
            update_cell(state.table_data, i, j, e.control.value)
        return handler
    return wrapper
