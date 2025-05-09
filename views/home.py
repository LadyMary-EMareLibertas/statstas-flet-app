import flet as ft

# 홈 화면 View 정의 함수
# 페이지 객체(page)를 받아서 '/' 경로에 해당하는 첫 진입 화면을 반환함

def home_view(page: ft.Page):
    return ft.View(
        route="/",  # 이 View는 루트 경로('/')에 연결됨
        controls=[
            ft.Container(
                alignment=ft.alignment.center,  # 화면 중앙 정렬
                padding=50,  # 전체 내부 여백 50px
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # 수평 중앙 정렬
                    spacing=30,  # 위젯 간 수직 간격 30px
                    controls=[

                        # 🔷 헤더: 앱 이름 (로고 역할)
                        ft.Text(
                            "ΣTATSTAS",  # 'Σ' + 'STATSTAS' 조합, 로고 역할
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.CYAN_400,
                            font_family="Courier New"  # 프로그래밍 툴 느낌 강조
                        ),

                        # 🔹 서브헤더: 앱 설명 텍스트
                        ft.Text(
                            "Advanced Statistical Testing Suite",
                            size=16,
                            color=ft.colors.GREY_400,
                            font_family="Courier New"
                        ),

                        # 🔸 구분선
                        ft.Divider(),

                        # 🔸 안내 텍스트: 기능 선택 요청
                        ft.Text(
                            "Choose a statistical tool to begin.",
                            size=14,
                            italic=True,
                            color=ft.colors.GREY_500
                        ),

                        # 🔷 주요 기능 버튼 3개: 통계 / 테이블 / 그래프
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,  # 버튼 가운데 정렬
                            spacing=20,  # 버튼 간 간격 20px
                            controls=[

                                # ✅ 통계 분석 도구로 이동
                                ft.ElevatedButton(
                                    "Statistics",
                                    icon=ft.icons.CALCULATE,
                                    on_click=lambda e: page.go("/statistics")
                                ),

                                # ✅ 테이블 기능으로 이동 (예정)
                                ft.ElevatedButton(
                                    "Tables",
                                    icon=ft.icons.TABLE_CHART,
                                    on_click=lambda e: page.go("/tables")
                                ),

                                # ✅ 그래프 기능으로 이동 (예정)
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