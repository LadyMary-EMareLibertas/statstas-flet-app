from core.table_logic import cell

def get_default_table():
    table = []
    counter = 1

    for row_index in range(6):  # 상위 6줄
        row = []
        for _ in range(7):
            row.append(cell(str(counter), align="left", top=True))
            counter += 1
        table.append(row)

    # 마지막 7번째 줄 (APA 주석)
    last_row = [cell("***p < .01.", "left", editable=True, width=680, top=True)] + \
               [cell("", editable=False, visible=False, top=True) for _ in range(6)]
    table.append(last_row)

    return table