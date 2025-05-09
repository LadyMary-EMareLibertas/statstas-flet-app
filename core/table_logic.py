def cell(val, align="center", editable=True, top=False, bottom=False, width=85, visible=True):
    return {
        "value": val,
        "align": align,
        "editable": editable,
        "visible": visible,
        "width": width,
        "border_top": {
            "color": "black" if top else "white",
            "thickness": 1
        },
        "border_bottom": {
            "color": "black" if bottom else "white",
            "thickness": 1
        }
    }

def get_default_table():
    return [
        [cell("", "left"), cell("M", bottom=True), cell("SD", bottom=True), cell("M", bottom=True),
         cell("SD", bottom=True), cell("", bottom=True), cell("", bottom=True)],
        [cell("Row 1", "left"), cell("3.6"), cell(".49"), cell("9.2"), cell("1.02"), cell("69.9***"), cell(".12")],
        [cell("Row 2", "left"), cell("2.4"), cell(".67"), cell("10.1"), cell(".08"), cell("42.7***"), cell(".23")],
        [cell("Row 3", "left"), cell("1.2"), cell(".78"), cell("3.6"), cell(".46"), cell("53.9***"), cell(".34")],
        [cell("Row 4", "left"), cell("0.8"), cell(".93"), cell("4.7"), cell(".71"), cell("21.1***"), cell(".45", bottom=True)],
        [cell("***p < .01.", "left", editable=False, width=680)] + [cell("", editable=False, visible=False) for _ in range(6)]
    ]

def update_cell(data, row, col, new_value):
    data[row][col]["value"] = new_value
    return data

def toggle_border_color(data, row, col, direction="top"):
    border_key = f"border_{direction}"
    border = data[row][col].get(border_key, {"color": "white", "thickness": 1})
    current = border.get("color", "white")
    data[row][col][border_key] = {
        "color": "black" if current == "white" else "white",
        "thickness": border.get("thickness", 1)
    }
    return data

def get_border_style(cell, direction):
    return cell.get(f"border_{direction}", {"color": "white", "thickness": 0})

def get_text_alignment(align_str):
    from flet import TextAlign
    return getattr(TextAlign, align_str.upper(), TextAlign.LEFT)

def add_row(data, row_index):
    """Insert new row below the given row index."""
    num_cols = len(data[0])
    new_row = [cell("", align="left") for _ in range(num_cols)]
    data.insert(row_index + 1, new_row)
    return data

def add_column(data, col_index):
    """Insert new column to the right of the given column index."""
    for row in data:
        row.insert(col_index + 1, cell("", align="left"))
    return data

def toggle_border_thickness(data, row, col, direction="top"):
    """Toggle the thickness of a cell border between 1 and 2."""
    border_key = f"border_{direction}"
    border = data[row][col].get(border_key, {"color": "white", "thickness": 1})
    current_thickness = border.get("thickness", 1)
    data[row][col][border_key] = {
        "color": border.get("color", "white"),
        "thickness": 2 if current_thickness == 1 else 1
    }
    return data