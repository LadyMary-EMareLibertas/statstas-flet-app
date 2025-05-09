from copy import deepcopy
from core.table_logic import (
    add_row,
    add_column,
    toggle_border_thickness,
)

def handle_add_row(table_data, selected_cell, table_column, build_table_rows, page):
    if selected_cell:
        i, _ = selected_cell
        template_row = table_data[i]
    else:
        i = len(table_data) - 1
        template_row = table_data[i]
    add_row(table_data, i, template_row=template_row)
    table_column.controls = build_table_rows()
    page.update()

def handle_delete_row(table_data, selected_cell, table_column, build_table_rows, page):
    if not selected_cell:
        return
    i, _ = selected_cell
    if 0 <= i < len(table_data):
        table_data.pop(i)
    table_column.controls = build_table_rows()
    page.update()

def handle_add_column(table_data, selected_cell, table_column, build_table_rows, page):
    if selected_cell:
        _, j = selected_cell
        template_column = [row[j] for row in table_data]
    else:
        j = len(table_data[0]) - 1 if table_data else 0
        template_column = [row[j] for row in table_data]
    add_column(table_data, j, template_column=template_column)
    table_column.controls = build_table_rows()
    page.update()

def handle_delete_column(table_data, selected_cell, table_column, build_table_rows, page):
    if not selected_cell:
        return
    _, j = selected_cell
    if 0 <= j < len(table_data[0]):
        for row in table_data:
            row.pop(j)
    table_column.controls = build_table_rows()
    page.update()

def handle_toggle_bold(table_data, selected_cell, table_column, build_table_rows, page):
    if not selected_cell:
        return
    i, j = selected_cell
    toggle_border_thickness(table_data, i, j, direction="top")
    table_column.controls = build_table_rows()
    page.update()