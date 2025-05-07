import flet as ft
import functools  
import difflib    

def main(page: ft.Page):
    page.title = "StatStas"

    def route_change(e):
        route = e.route if hasattr(e, "route") else e
        print(f"Route changed to: {route}")
        page.views.clear()

        #여기만 수정하세요
        if route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Container(
                            content=ft.Column([
                                # 메인 페이지
                                #첫 화면 (소개 페이지)
                                # - 기능 설명
                                # - 버튼 → /해당 페이지로 이동
                                ft.Text("Welcome to StatStas", size=40, weight=ft.FontWeight.BOLD),
                                ft.Text("Powerful, intuitive statistical analysis tools.", size=20),
                                ft.Divider(),
                                ft.Text("Run t-tests, ANOVA, and regression analysis with ease."),
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            ft.ElevatedButton(
                                                "Statistics",
                                                icon=ft.icons.CALCULATE,
                                                style=ft.ButtonStyle(
                                                    padding=20,
                                                    text_style=ft.TextStyle(size=20)
                                                ),
                                                on_click=lambda e: page.go("/statistics")
                                            ),
                                            ft.ElevatedButton(
                                                "Tables",
                                                icon=ft.icons.TABLE_CHART,
                                                style=ft.ButtonStyle(
                                                    padding=20,
                                                    text_style=ft.TextStyle(size=20)
                                                ),
                                                on_click=lambda e: page.go("/tables")
                                            ),
                                            ft.ElevatedButton(
                                                "Graphs",
                                                icon=ft.icons.INSERT_CHART,
                                                style=ft.ButtonStyle(
                                                    padding=20,
                                                    text_style=ft.TextStyle(size=20)
                                                ),
                                                on_click=lambda e: page.go("/graphs")
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=30
                                    ),
                                    alignment=ft.alignment.center,
                                    padding=20
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15),
                            alignment=ft.alignment.center,
                            padding=40
                        )
                    ]
                )
            )

        # 메뉴 페이지
        # - 통계 도구 선택 or 검색 가능하게 할 예정
        elif route == "/statistics":

            # 검색 대상 도구 리스트
            stat_tests = [
                {"label": "Paired t-test (Two-tailed)", "route": "/paired_two"},
                {"label": "Paired t-test (One-tailed)", "route": "/paired_one"},
                {"label": "Independent t-test (Two-tailed)", "route": "/indep_two"},
                {"label": "Independent t-test (One-tailed)", "route": "/indep_one"},
                {"label": "One-sample t-test (Two-tailed)", "route": "/onesample_two"},
                {"label": "One-sample t-test (One-tailed)", "route": "/onesample_one"}
            ]

            # 추천 리스트 박스
            suggestions = ft.Column()

            # 라우트 전환용 핸들러 생성기
            def go_to_route(route):
                def handler(e):
                    page.go(route)
                return handler

            # 검색 핸들러
            def search_handler(e):
                query = e.control.value.strip().lower()
                suggestions.controls.clear()

                if query == "":
                    page.update()
                    return  # 빈 문자열이면 추천 리스트 비움

                labels = [t["label"] for t in stat_tests]
                matches = difflib.get_close_matches(query, labels, n=5, cutoff=0.2)

                if not matches:
                    matches = [label for label in labels if query in label.lower()]

                for match in matches:
                    test = next((t for t in stat_tests if t["label"] == match), None)
                    if test:
                        suggestions.controls.append(
                            ft.TextButton(
                                text=test["label"],
                                style=ft.ButtonStyle(color=ft.colors.BLUE, padding=10),
                                on_click=go_to_route(test["route"])
                            )
                        )
                page.update()

            # 검색창
            search_input = ft.TextField(
                label="Search for a statistical test...",
                on_change=search_handler
            )

            # 통계 도구 텍스트 리스트
            tool_descriptions = [
                "- Paired t-test (two-tailed)",
                "- Paired t-test (one-tailed)",
                "- Independent t-test (two-tailed)",
                "- Independent t-test (one-tailed)",
                "- One-sample t-test (two-tailed)",
                "- One-sample t-test (one-tailed)",
            ]

            # 복사할 문자열
            clipboard_text = "\n".join(tool_descriptions)

            # 복사 버튼
            copy_button = ft.ElevatedButton(
                text="Copy Tool List",
                icon=ft.icons.CONTENT_COPY,
                on_click=lambda e: page.set_clipboard(clipboard_text)
            )

            # 사용자 요청 안내 영역
            request_section = ft.Column([
                ft.Divider(),
                ft.Text("Need a tool that's not listed? Got a question?", size=16),
                ft.Text("Let us know! We'll add more tools based on your needs.", size=16),
                ft.Row([
                    ft.Text("Email: ", size=14),
                    ft.Text("eugenemariastas@gamil.com", size=14, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                    ft.ElevatedButton(
                        text="📋 Copy Email",
                        icon=ft.icons.CONTENT_COPY,
                        on_click=lambda e: page.set_clipboard("statstas@yourdomain.com")
                    )
                ])
            ])

            # 접이식 UI + 스크롤 가능한 목록
            static_description = ft.ExpansionTile(
                title=ft.Text("Currently available statistical tools", weight=ft.FontWeight.BOLD),
                subtitle=ft.Text("Click to expand full list"),
                initially_expanded=False,
                controls=[
                    ft.Container(
                        content=ft.ListView(
                            controls=[ft.Text(item) for item in tool_descriptions],
                            spacing=5,
                            height=250,
                            expand=False
                        )
                    )
                ]
            )

            # 뷰 생성
            page.views.append(
                ft.View(
                    "/statistics",
                    controls=[
                        ft.Text("🔍 Statistical Tool Search", size=24),
                        search_input,
                        suggestions,
                        static_description,
                        copy_button,
                        request_section,
                        ft.Divider(),
                        ft.ElevatedButton("⬅ Back to Home", on_click=lambda e: page.go("/"))
                    ]
                )
            )

    #여기는 건들지 마세요 
    page.on_route_change = route_change
    route_change(page.route)
    page.go(page.route)

ft.app(target=main)