from table.table_logic import cell

def get_default_table():
    return [
        [cell("Variable", align="left", top=True),
         cell("Visual", align="left", top=True),
         cell("", align="left", top=True),
         cell("Infrared", align="left", top=True),
         cell("", align="left", top=True),
         cell("F", align="left", top=True),
         cell("η", align="left", top=True)],

        [cell("", align="left", top=False),
         cell("M", align="left", top=True),
         cell("SD", align="left", top=True),
         cell("M", align="left", top=True),
         cell("SD", align="left", top=True),
         cell("", align="left", top=False),
         cell("", align="left", top=False)],

        [cell("Row 1", align="left", top=True),
         cell("3.6", align="left", top=True),
         cell(".49", align="left", top=True),
         cell("9.3", align="left", top=True),
         cell("1.02", align="left", top=True),
         cell("69.9***", align="left", top=True),
         cell(".12", align="left", top=True)],

        [cell("Row 2", align="left", top=False),
         cell("2.4", align="left", top=False),
         cell(".67", align="left", top=False),
         cell("10.1", align="left", top=False),
         cell(".08", align="left", top=False),
         cell("42.7***", align="left", top=False),
         cell(".23", align="left", top=False)],

        [cell("Row 3", align="left", top=False),
         cell("1.2", align="left", top=False),
         cell(".78", align="left", top=False),
         cell("3.6", align="left", top=False),
         cell(".46", align="left", top=False),
         cell("53.9***", align="left", top=False),
         cell(".34", align="left", top=False)],

        [cell("Row 4", align="left", top=False),
         cell("0.8", align="left", top=False),
         cell("93", align="left", top=False),
         cell("4.7", align="left", top=False),
         cell(".71", align="left", top=False),
         cell("21.1***", align="left", top=False),
         cell(".45", align="left", top=False)],

        [cell("***p < .01.", "left", editable=True, width=680, top=True)] +
            [cell("", editable=False, visible=False, top=True) for _ in range(6)]
    ]