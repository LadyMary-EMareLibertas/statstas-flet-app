import flet as ft
import difflib
from data.stat_tests import stat_tests  # 통계 도구 라벨/라우트 데이터 불러오기

def statistics_view(page: ft.Page):
    # 검색 결과(추천 도구 리스트)를 담을 Column
    suggestions = ft.Column()

    # 라우트 이동 핸들러 생성 함수 (TextButton 클릭 시 해당 route로 이동)
    def go_to_route(route):
        def handler(e):
            page.go(route)
        return handler

    # 검색 입력값이 바뀔 때 실행되는 핸들러
    def search_handler(e):
        query = e.control.value.strip().lower()
        suggestions.controls.clear()

        if query == "":
            page.update()
            return

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
                        style=ft.ButtonStyle(
                            color=ft.colors.BLUE_700,
                            padding=10,
                        ),
                        on_click=go_to_route(test["route"])
                    )
                )
        page.update()

    # 검색창 입력 필드
    search_input = ft.TextField(
        label="Search for a statistical test...",
        on_change=search_handler,
        text_style=ft.TextStyle(size=14),
        border_radius=8,
        filled=True,
        fill_color=ft.colors.WHITE,
        border_color=ft.colors.BLUE_GREY_200
    )

    # 전체 통계 도구 라벨 리스트 (접이식 뷰 및 클립보드용)
    tool_descriptions = [
        "- Paired t-test (two-tailed)",
        "- Paired t-test (one-tailed)",
        "- Independent t-test (two-tailed)",
        "- Independent t-test (one-tailed)",
        "- One-sample t-test (two-tailed)",
        "- One-sample t-test (one-tailed)"
    ]
    clipboard_text = "\n".join(tool_descriptions)

    # 홈 뷰와 동일한 디자인의 버튼 생성 함수
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

    # 이메일 주소 복사 버튼
    copy_email_button = home_style_button(
        "Copy Email",
        ft.icons.CONTENT_COPY,
        lambda e: page.set_clipboard("eugenemariastas@gmail.com")
    )

    # 홈으로 돌아가는 뒤로가기 버튼
    back_button = home_style_button(
        "Back",
        ft.icons.ARROW_BACK,
        lambda e: page.go("/")
    )

    # 사용자가 원하는 도구가 없을 때 요청을 유도하는 안내 텍스트 + 이메일
    tool_list_controls = [
        ft.Text(label, size=13, color=ft.colors.GREY_700) for label in tool_descriptions
    ]
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

    static_description = ft.ExpansionTile(
        title=ft.Text(
            "Currently available statistical tools",
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_GREY_700
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
            search_input,
            suggestions,
            static_description,
            ft.Divider(),
            back_button
        ]
    )
