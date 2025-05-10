def handle_add_row(table_data, selected_cell, table_column, build_rows_fn, page):
    if not table_data:
        return
    num_columns = len(table_data[0])
    new_row = [{"value": "", "width": 85, "editable": True, "visible": True} for _ in range(num_columns)]
    table_data.append(new_row)
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
    for row in table_data:
        row.append({"value": "", "width": 85, "editable": True, "visible": True})
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