import flet as ft
import difflib
from stats.stat_tests import stat_tests  # 통계 테스트 정의된 리스트 불러오기

# 통계 도구 선택 화면 View 정의 함수
def statistics_view(page: ft.Page):
    # 🔷 검색 결과로 보여줄 버튼 리스트 담을 컬럼
    suggestions = ft.Column()

    # 🔷 라우트 이동용 핸들러 생성 함수
    def go_to_route(route):
        def handler(e):
            page.go(route)
        return handler

    # 🔷 검색창 입력 시 호출되는 핸들러 함수
    def search_handler(e):
        query = e.control.value.strip().lower()
        suggestions.controls.clear()  # 기존 검색 결과 초기화

        if query == "":
            page.update()
            return

        labels = [t["label"] for t in stat_tests]  # 전체 검색 가능한 라벨 리스트
        matches = difflib.get_close_matches(query, labels, n=5, cutoff=0.2)

        if not matches:
            matches = [label for label in labels if query in label.lower()]

        # 검색 결과에 맞는 버튼 동적으로 생성
        for match in matches:
            test = next((t for t in stat_tests if t["label"] == match), None)
            if test:
                suggestions.controls.append(
                    ft.TextButton(
                        text=test["label"],
                        style=ft.ButtonStyle(
                            color=ft.colors.BLUE_700,
                            padding=10,
                        ),
                        on_click=go_to_route(test["route"])
                    )
                )
        page.update()

    # 🔶 시그마 로고 (검색창 왼쪽에 배치)
    sigma_logo = ft.Text(
        "Σ",  # 그리스 문자 시그마, 수학/통계 상징
        size=36,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.CYAN_600
    )

    # 🔶 검색 입력 필드 정의
    search_input = ft.TextField(
        hint_text="Search statistical tools...",
        on_change=search_handler,
        text_style=ft.TextStyle(size=14),
        border_radius=12,
        filled=True,
        fill_color=ft.colors.WHITE,
        border_color=ft.colors.CYAN_600,
        border_width=1,
        text_align=ft.TextAlign.CENTER,
        height=56,
        width=460
    )

    # 🔶 로고와 입력 필드를 가로로 배치한 Row
    search_row = ft.Row(
        controls=[sigma_logo, search_input],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12
    )

    # 🔶 검색창 전체를 감싸는 컨테이너
    search_container = ft.Container(
        alignment=ft.alignment.center,
        padding=ft.padding.only(top=80, bottom=20),
        content=ft.Column(
            controls=[
                search_row,
                ft.Text("🔍 Type a test name to begin", size=12, color=ft.colors.CYAN_800)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8
        )
    )

    # 🔷 도구 설명 문자열 리스트
    tool_descriptions = [
        "- Paired t-test (two-tailed)",
        "- Paired t-test (one-tailed)",
        "- Independent t-test (two-tailed)",
        "- Independent t-test (one-tailed)",
        "- One-sample t-test (two-tailed)",
        "- One-sample t-test (one-tailed)"
    ]
    clipboard_text = "\n".join(tool_descriptions)  # 복사용 텍스트

    # 🔷 공통 버튼 생성 함수
    def home_style_button(text, icon, on_click):
        return ft.ElevatedButton(
            text=text,
            icon=icon,
            style=ft.ButtonStyle(
                color=ft.colors.BLUE_GREY_800,
                overlay_color=ft.colors.BLUE_GREY_50,
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                shape=ft.RoundedRectangleBorder(radius=20),
            ),
            on_click=on_click
        )

    # 🔷 복사 버튼 생성
    copy_email_button = home_style_button(
        "Copy Email",
        ft.icons.CONTENT_COPY,
        lambda e: page.set_clipboard("eugenemariastas@gmail.com")
    )

    # 🔷 뒤로 가기 버튼 생성
    back_button = home_style_button(
        "Back",
        ft.icons.ARROW_BACK,
        lambda e: page.go("/")
    )

    # 🔷 도구 설명 텍스트 리스트 컴포넌트 생성
    tool_list_controls = [ft.Text(label, size=13, color=ft.colors.GREY_700) for label in tool_descriptions]
    tool_list_controls += [
        ft.Divider(),
        ft.Text(
            "Can't find what you need? You can email me!",
            size=14,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.RED_ACCENT_400
        ),
        ft.Row([
            ft.Text("E-mail:", size=14),
            ft.Text("eugenemariastas@gamil.com", size=13, color=ft.colors.GREY_700),
            copy_email_button
        ])
    ]

    # 🔷 도구 설명 접이식 패널 정의
    static_description = ft.ExpansionTile(
        title=ft.Text(
            "Currently available statistical tools",
            weight=ft.FontWeight.BOLD,
            color=ft.colors.CYAN_400
        ),
        subtitle=ft.Text(
            "Click to expand full list",
            size=12,
            color=ft.colors.GREY_500
        ),
        initially_expanded=False,
        controls=[
            ft.Container(
                content=ft.ListView(
                    controls=tool_list_controls,
                    spacing=5,
                    height=250,
                    expand=False
                )
            )
        ]
    )

    # 🔷 최종 View 구성 반환
    return ft.View(
        route="/statistics",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text(
                "Statistics",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_400
            ),
            search_container,
            suggestions,
            static_description,
            ft.Divider(),
            back_button
        ]
    )
