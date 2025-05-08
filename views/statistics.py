import flet as ft  # Flet UI 프레임워크 가져오기
import difflib  # 문자열 유사도 검색용
from data.stat_tests import stat_tests  # 사전에 정의된 통계 테스트 라벨/라우트 불러오기

def statistics_view(page: ft.Page):  # 이 함수는 /statistics 경로에 대응하는 화면을 생성함
    suggestions = ft.Column()  # 검색 결과를 담을 컬럼 (자동 갱신)

    def go_to_route(route):  # 라우트 이동 핸들러 생성기
        def handler(e):  # 실제 핸들러 함수 내부
            page.go(route)  # 해당 route로 이동
        return handler

    def search_handler(e):  # 검색창 입력값 변경 시 호출됨
        query = e.control.value.strip().lower()  # 입력 텍스트 전처리
        suggestions.controls.clear()  # 기존 검색 결과 초기화

        if query == "":  # 입력이 없으면 결과 표시 안함
            page.update()
            return

        labels = [t["label"] for t in stat_tests]  # 전체 라벨 리스트 수집
        matches = difflib.get_close_matches(query, labels, n=5, cutoff=0.2)  # 유사도 기반 검색

        if not matches:
            matches = [label for label in labels if query in label.lower()]  # fallback: 부분문자열 매칭

        for match in matches:  # 매칭된 항목마다 버튼 생성
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
        page.update()  # 화면 갱신

    search_input = ft.TextField(  # 검색 입력 필드
        hint_text="Search statistical tools...",  # 사용자 안내 텍스트
        on_change=search_handler,  # 입력값 변경 시 핸들러 호출
        text_style=ft.TextStyle(size=14),  # 텍스트 크기 설정
        border_radius=12,  # 둥글게 설정
        filled=True,  # 배경 채움
        fill_color=ft.colors.WHITE,  # 배경색
        border_color=ft.colors.CYAN_600,  # 테두리 색
        border_width=1,  # 얇은 테두리
        text_align=ft.TextAlign.CENTER,  # 텍스트 중앙 정렬
        height=56,  # 입력창 높이
        width=500  # 입력창 너비
    )

    search_container = ft.Container(  # 검색창을 감싸는 외부 박스
        alignment=ft.alignment.center,  # 가운데 정렬
        padding=ft.padding.only(top=80, bottom=20),  # 위/아래 여백
        content=ft.Column(
            controls=[
                search_input,  # 검색창 본체
                ft.Text("🔍 Type a test name to begin", size=12, color=ft.colors.CYAN_800)  # 보조 안내 텍스트
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # 수평 중앙 정렬
            spacing=8  # 검색창과 안내문 사이 간격
        )
    )

    tool_descriptions = [  # 도구 설명 리스트 (표시 및 클립보드 복사용)
        "- Paired t-test (two-tailed)",
        "- Paired t-test (one-tailed)",
        "- Independent t-test (two-tailed)",
        "- Independent t-test (one-tailed)",
        "- One-sample t-test (two-tailed)",
        "- One-sample t-test (one-tailed)"
    ]
    clipboard_text = "\n".join(tool_descriptions)  # 복사 버튼용 문자열로 변환

    def home_style_button(text, icon, on_click):  # 공통 버튼 생성 함수
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

    copy_email_button = home_style_button(  # 이메일 복사 버튼
        "Copy Email",
        ft.icons.CONTENT_COPY,
        lambda e: page.set_clipboard("eugenemariastas@gmail.com")
    )

    back_button = home_style_button(  # 뒤로가기 버튼
        "Back",
        ft.icons.ARROW_BACK,
        lambda e: page.go("/")
    )

    tool_list_controls = [  # 도구 설명 리스트 (Text 컴포넌트들)
        ft.Text(label, size=13, color=ft.colors.GREY_700) for label in tool_descriptions
    ]
    tool_list_controls += [  # 리스트 끝에 요청 메시지 추가
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

    static_description = ft.ExpansionTile(  # 접이식 도구 리스트
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

    return ft.View(  # 최종적으로 View 반환
        route="/statistics",  # 이 View가 연결되는 라우트 경로
        scroll=ft.ScrollMode.AUTO,  # 세로 스크롤 허용
        controls=[  # 이 View에 포함될 구성 요소들
            ft.Text(
                "Statistics",  # 페이지 제목 텍스트
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_400
            ),
            search_container,  # 검색창 블럭 전체
            suggestions,  # 검색 결과 영역
            static_description,  # 접이식 도구 설명
            ft.Divider(),  # 시각적 구분선
            back_button  # 뒤로가기 버튼
        ]
    )
