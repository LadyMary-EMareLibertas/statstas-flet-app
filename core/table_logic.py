def get_default_table():
    def cell(val, align="center", editable=True, top=False, bottom=False):
        return {
            "value": val,
            "align": align,
            "editable": editable,
            "border_top": top,
            "border_bottom": bottom
        }

    return [
        [cell("Variable", "left"), cell(""), cell("Visual", bottom=True, top=True), cell(""), cell("Infrared", bottom=True, top=True), cell(""), cell("F"), cell("η")],
        [cell(""), cell(""), cell("M", top=True, bottom=True), cell("SD", top=True, bottom=True), cell("M", top=True, bottom=True), cell("SD", top=True, bottom=True), cell(""), cell("", bottom=True)],
        [cell("Row 1", "left"), cell(""), cell("3.6", "right"), cell(".49", "right"), cell("9.2", "right"), cell("1.02", "right"), cell("69.9***", "right"), cell(".12", "right")],
        [cell("Row 2", "left"), cell(""), cell("2.4", "right"), cell(".67", "right"), cell("10.1", "right"), cell(".08", "right"), cell("42.7***", "right"), cell(".23", "right")],
        [cell("Row 3", "left"), cell(""), cell("1.2", "right"), cell(".78", "right"), cell("3.6", "right"), cell(".46", "right"), cell("53.9***", "right"), cell(".34", "right")],
        [cell("Row 4", "left"), cell(""), cell("0.8", "right"), cell(".93", "right"), cell("4.7", "right"), cell(".71", "right"), cell("21.1***", "right"), cell(".45", "right")],
        [cell("***p < .01.", "left", editable=False), cell("", editable=False), cell("", editable=False), cell("", editable=False), cell("", editable=False), cell("", editable=False), cell("", editable=False), cell("", editable=False)]
    ]

# ✅ 셀 하나 수정

def update_cell(data, row, col, new_value):
    data[row][col]["value"] = new_value
    return data
