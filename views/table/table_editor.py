import flet as ft

# 🔷 APA 스타일 표 데이터 (이미지 기반 구조 반영)
safe_table_data = [
    ["Variable", "", "Visual", "", "Infrared", "", "F", "η"],
    ["", "", "M", "SD", "M", "SD", "", ""],
    ["Row 1", "", "3.6", ".49", "9.2", "1.02", "69.9***", ".12"],
    ["Row 2", "", "2.4", ".67", "10.1", ".08", "42.7***", ".23"],
    ["Row 3", "", "1.2", ".78", "3.6", ".46", "53.9***", ".34"],
    ["Row 4", "", "0.8", ".93", "4.7", ".71", "21.1***", ".45"],
    ["", "", "", "", "", "", "", ""]
]

def table_editor_view(page: ft.Page):
    def build_safe_table():
        rows = []
        for row_idx, row in enumerate(safe_table_data):
            cells = []
            for col_idx, val in enumerate(row):
                align = ft.TextAlign.CENTER
                if row_idx == 0 and col_idx in {2, 4}:
                    weight = ft.FontWeight.BOLD
                elif row_idx == 1:
                    weight = ft.FontWeight.NORMAL
                elif col_idx == 0:
                    align = ft.TextAlign.START
                    weight = ft.FontWeight.NORMAL
                else:
                    align = ft.TextAlign.END
                    weight = ft.FontWeight.NORMAL

                text = ft.Text(val, text_align=align, weight=weight, size=13)

                # ✅ Visual(0,2), Infrared(0,4)에만 하단선
                if row_idx == 0 and col_idx in {2, 4}:
                    border = ft.border.only(bottom=ft.BorderSide(1, ft.colors.BLACK))
                # ✅ 줄 1과 줄 6 (헤더와 맨 마지막)에도 선
                elif row_idx == 1 or row_idx == 6:
                    border = ft.border.only(bottom=ft.BorderSide(1, ft.colors.BLACK))
                else:
                    border = None

                cells.append(
                    ft.Container(
                        content=text,
                        padding=ft.padding.symmetric(horizontal=6, vertical=4),
                        width=95,
                        bgcolor=ft.colors.WHITE,
                        border=border
                    )
                )

            row_container = ft.Container(
                content=ft.Row(controls=cells, spacing=0)
            )
            rows.append(row_container)

        # 🔻 별도 주석 텍스트 (표 바깥)
        rows.append(
            ft.Container(
                content=ft.Text("***p < .01.", size=12, italic=True),
                padding=ft.padding.only(top=6)
            )
        )

        return ft.Column(controls=rows, spacing=0)

    return ft.View(
        route="/table",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text("📋 APA Table Template", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_400),
            ft.Container(height=20),
            ft.Container(
                content=build_safe_table(),
                padding=10,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=6
            )
        ]
    )