import flet as ft
import difflib
from data.stat_tests import stat_tests  # 통계 테스트 정의된 리스트 불러오기

def statistics_view(page: ft.Page):
    suggestions = ft.Column()  # 검색 결과 버튼 리스트가 여기에 동적으로 추가됨

    def go_to_route(route):
        def handler(e):
            page.go(route)
        return handler

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

    # ✅ 시그마 로고 (검색창 왼쪽에 배치)
    sigma_logo = ft.Text(
        "Σ",
        size=36,
        weight=ft.FontWeight.BOLD,
        color=ft.colors.CYAN_600
    )

    # ✅ 검색 입력창
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

    # ✅ 검색창과 시그마 로고를 함께 정렬
    search_row = ft.Row(
        controls=[sigma_logo, search_input],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12
    )

    # ✅ 전체 검색 영역 컨테이너
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

    # ✅ 도구 설명 리스트 (표시 및 복사용)
    tool_descriptions = [
        "- Paired t-test (two-tailed)",
        "- Paired t-test (one-tailed)",
        "- Independent t-test (two-tailed)",
        "- Independent t-test (one-tailed)",
        "- One-sample t-test (two-tailed)",
        "- One-sample t-test (one-tailed)"
    ]
    clipboard_text = "\n".join(tool_descriptions)

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

    copy_email_button = home_style_button(
        "Copy Email",
        ft.icons.CONTENT_COPY,
        lambda e: page.set_clipboard("eugenemariastas@gmail.com")
    )

    back_button = home_style_button(
        "Back",
        ft.icons.ARROW_BACK,
        lambda e: page.go("/")
    )

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

    static_description = ft.ExpansionTile(
        title=ft.Text(
            "Currently available statistical tools",
            weight=ft.FontWeight.BOLD,
            color=ft.colors.CYAN_400  # ✅ CYAN 톤 강조
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
            search_container,
            suggestions,
            static_description,
            ft.Divider(),
            back_button
        ]
    )