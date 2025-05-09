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
        [  # 헤더 (병합 시뮬레이션)
            cell("Variable", "left"),
            cell("", visible=False),
            cell("Visual", bottom=True, top=True, width=170),
            cell("", visible=False),
            cell("Infrared", bottom=True, top=True, width=170),
            cell("", visible=False),
            cell("F"),
            cell("η")
        ],
        [  # M / SD 라벨 행
            cell("", "left"),
            cell("", visible=False),
            cell("M", top=True, bottom=True),
            cell("SD", top=True, bottom=True),
            cell("M", top=True, bottom=True),
            cell("SD", top=True, bottom=True),
            cell("", top=True),
            cell("", bottom=True)
        ],
        [  # 데이터 시작
            cell("Row 1", "left"), cell(""),
            cell("3.6", "right"), cell(".49", "right"),
            cell("9.2", "right"), cell("1.02", "right"),
            cell("69.9***", "right"), cell(".12", "right")
        ],
        [
            cell("Row 2", "left"), cell(""),
            cell("2.4", "right"), cell(".67", "right"),
            cell("10.1", "right"), cell(".08", "right"),
            cell("42.7***", "right"), cell(".23", "right")
        ],
        [
            cell("Row 3", "left"), cell(""),
            cell("1.2", "right"), cell(".78", "right"),
            cell("3.6", "right"), cell(".46", "right"),
            cell("53.9***", "right"), cell(".34", "right")
        ],
        [
            cell("Row 4", "left"), cell(""),
            cell("0.8", "right"), cell(".93", "right"),
            cell("4.7", "right"), cell(".71", "right"),
            cell("21.1***", "right"), cell(".45", "right")
        ],
        [  # 각주 (마지막 줄 병합)
            cell("***p < .01.", "left", editable=False, width=680),
            *[cell("", editable=False, visible=False) for _ in range(7)]
        ]
    ]

def update_cell(data, row, col, new_value):
    data[row][col]["value"] = new_value
    return data