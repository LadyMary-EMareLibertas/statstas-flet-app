from copy import deepcopy

def handle_add_row(table_data, selected_cell, table_column, build_rows_fn, page):
    if not table_data or selected_cell is None:
        return

    i, _ = selected_cell
    template_row = table_data[i]
    new_row = [deepcopy(cell) for cell in template_row]  # ✅ 선택된 행 복사
    table_data.insert(i + 1, new_row)
    table_column.controls = build_rows_fn()
    page.update()

def handle_delete_row(table_data, selected_cell, table_column, build_rows_fn, page):
    if selected_cell is None:
        return
    i, _ = selected_cell
    if 0 <= i < len(table_data):
        table_data.pop(i)
        table_column.controls = build_rows_fn()
        page.update()

def handle_add_column(table_data, selected_cell, table_column, build_rows_fn, page):
    from copy import deepcopy
    if selected_cell is None:
        return
    _, j = selected_cell
    for row in table_data:
        new_cell = deepcopy(row[j]) if 0 <= j < len(row) else {"value": "", "width": 85, "editable": True, "visible": True}
        row.insert(j + 1, new_cell)
    table_column.controls = build_rows_fn()
    page.update()

def handle_delete_column(table_data, selected_cell, table_column, build_rows_fn, page):
    if selected_cell is None:
        return
    _, j = selected_cell
    for row in table_data:
        if 0 <= j < len(row):
            row.pop(j)
    table_column.controls = build_rows_fn()
    page.update()

def handle_toggle_bold(table_data, selected_cell, table_column, build_rows_fn, page):
    if selected_cell is None:
        return
    i, j = selected_cell
    cell = table_data[i][j]
    border = cell.setdefault("border_top", {"thickness": 1, "color": "black"})
    border["thickness"] = 3 if border.get("thickness", 1) == 1 else 1
    table_column.controls = build_rows_fn()
    page.update()