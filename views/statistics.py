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
    # 사용자가 검색창에 입력할 때마다 추천 리스트 갱신
    def search_handler(e):
        query = e.control.value.strip().lower()  # 입력값 정리
        suggestions.controls.clear()  # 추천 리스트 초기화

        if query == "":
            page.update()
            return  # 입력이 없으면 추천 안 띄움

        # 전체 라벨 목록에서 유사도 기반으로 유사 라벨 탐색
        labels = [t["label"] for t in stat_tests]
        matches = difflib.get_close_matches(query, labels, n=5, cutoff=0.2)

        # 유사도 기반 결과가 없으면 부분 문자열 포함 여부로 강제 매칭
        if not matches:
            matches = [label for label in labels if query in label.lower()]

        # 매칭된 라벨에 해당하는 라우트를 찾아 TextButton으로 출력
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
        "- One-sample t-test (one-tailed)",
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
                # bgcolor나 side는 명시하지 않아야 홈과 같은 입체감 유지됨
            ),
            on_click=on_click
        )

    # 전체 도구 리스트를 클립보드로 복사하는 버튼
    copy_button = home_style_button(
        "Copy Tool List",
        ft.icons.CONTENT_COPY,
        lambda e: page.set_clipboard(clipboard_text)
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
    request_section = ft.Column([
        ft.Divider(),  # 시각적 구분선
        ft.Text(
            "Need a tool that's not listed? Got a question?",
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_GREY_800
        ),
        ft.Text(
            "Let us know! We'll add more tools based on your needs.",
            size=14,
            color=ft.colors.GREY_600
        ),
        ft.Row([
            ft.Text("Email: ", size=14, color=ft.colors.GREY_700),
            ft.Text(
                "eugenemariastas@gamil.com",
                size=14,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.BLUE_700
            ),
            copy_email_button
        ])
    ])

    # 전체 도구 설명을 펼칠 수 있는 접이식 리스트
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
                    controls=[
                        ft.Text(item, size=13, color=ft.colors.GREY_700)
                        for item in tool_descriptions
                    ],
                    spacing=5,
                    height=250,
                    expand=False
                )
            )
        ]
    )

    # View 객체 반환: 이 뷰는 "/statistics" 라우트에 연결됨
    return ft.View(
        route="/statistics",
        scroll=ft.ScrollMode.AUTO,  # 세로 스크롤 자동 활성화
        controls=[
            # 페이지 상단 제목
            ft.Text(
                "Statistics",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_400
            ),
            search_input,      # 검색창
            suggestions,       # 추천 결과 리스트
            static_description,  # 접이식 전체 도구 목록
            copy_button,       # 도구 목록 복사 버튼
            request_section,   # 이메일 안내
            ft.Divider(),      # 시각 구분선
            back_button        # 뒤로가기 버튼
        ]
    )