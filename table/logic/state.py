from table.logic.template import get_default_table

TEXT_MODE = "text"
STRUCTURE_MODE = "structure"

class TableEditorState:
    def __init__(self):
        self.table_data = get_default_table()
        self.editing_mode = STRUCTURE_MODE
        self.selected_cell = None