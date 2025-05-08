import flet as ft

def home_view(page: ft.Page):
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                alignment=ft.alignment.center,
                padding=50,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        # 헤더
                        ft.Text(
                            "ΣTATSTAS",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.CYAN_400,
                            font_family="Courier New"  # IDE 느낌
                        ),
                        ft.Text(
                            "Advanced Statistical Testing Suite",
                            size=16,
                            color=ft.colors.GREY_400,
                            font_family="Courier New"
                        ),
                        ft.Divider(),

                        # 안내 텍스트
                        ft.Text(
                            "Choose a statistical tool to begin.",
                            size=14,
                            italic=True,
                            color=ft.colors.GREY_500
                        ),

                        # 버튼 영역
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                            controls=[
                                ft.ElevatedButton(
                                    "Statistics",
                                    icon=ft.icons.CALCULATE,
                                    on_click=lambda e: page.go("/statistics")
                                ),
                                ft.ElevatedButton(
                                    "Tables",
                                    icon=ft.icons.TABLE_CHART,
                                    on_click=lambda e: page.go("/tables")
                                ),
                                ft.ElevatedButton(
                                    "Graphs",
                                    icon=ft.icons.INSERT_CHART,
                                    on_click=lambda e: page.go("/graphs")
                                ),
                            ]
                        )
                    ]
                )
            )
        ]
    )