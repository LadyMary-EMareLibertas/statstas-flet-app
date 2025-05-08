import flet as ft
from core.ttest_logic import run_paired_ttest  # t-test 계산 함수 import

# 이 함수는 "/paired_two" 경로에 해당하는 화면(View)을 구성함
# 사용자가 before/after 값을 입력하고, 유의수준(alpha)을 설정한 후 버튼을 눌러 paired t-test를 실행

def paired_view(page: ft.Page):
    # ✅ 사용자 입력 필드 설정
    before_input = ft.TextField(label="Before (comma-separated)", hint_text="e.g., 100, 102, 98")
    after_input = ft.TextField(label="After (comma-separated)", hint_text="e.g., 105, 100, 99")
    alpha_input = ft.TextField(label="Alpha", value="0.05")

    # ✅ 입력 필드들을 묶는 Column 구성 (간격 조절용)
    input_fields = ft.Column(
        controls=[
            before_input,
            after_input,
            alpha_input
        ],
        spacing=16  # 입력창 사이 간격(px 단위)
    )

    # ✅ 결과를 표시할 텍스트 필드
    result_text = ft.Text(
        "",
        no_wrap=False,
        selectable=True
    )

    # ✅ 결과 카드 (출력 텍스트 + 복사 버튼 포함)
    result_card = ft.Container(
        content=ft.Column(
            controls=[
                # 결과 텍스트는 왼쪽 정렬
                ft.Container(
                    content=result_text,
                    alignment=ft.alignment.center_left
                ),
                # 복사 버튼은 오른쪽 아래 정렬
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.CONTENT_COPY,
                                tooltip="Copy result",
                                icon_color=ft.colors.BLUE_700,
                                on_click=lambda e: page.set_clipboard(result_text.value)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.END
                    ),
                    alignment=ft.alignment.bottom_right
                )
            ],
            spacing=8,
            expand=True,  # 세로 공간 전체 사용해서 버튼을 하단에 밀어내기 위함
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        width=600,
        padding=20,
        margin=ft.margin.only(top=10),
        border_radius=8,
        bgcolor=ft.colors.GREY_50,
        border=ft.border.all(1, ft.colors.CYAN_400),
        visible=False  # 초기에 숨겨져 있음. 결과 나오면 True로 설정됨
    )

    # ✅ t-test 실행 함수 (Run 버튼 클릭 시 실행)
    def run_test(e):
        try:
            # 문자열 입력값을 숫자 리스트로 변환
            before = list(map(float, before_input.value.split(",")))
            after = list(map(float, after_input.value.split(",")))
            alpha = float(alpha_input.value)

            # t-test 계산 함수 호출
            result = run_paired_ttest(before, after, alpha)

            # 결과 텍스트 반영
            result_text.value = str(result)
            result_card.visible = True  # 결과 카드 표시

            # 결과 문자열 기반으로 테두리 색 바꾸기
            if "Not Significant" in result:
                result_card.border = ft.border.all(1, ft.colors.RED_ACCENT_400)
            else:
                result_card.border = ft.border.all(1, ft.colors.GREEN_ACCENT_400)


        except Exception as err:
            # 예외 발생 시 에러 메시지 출력
            result_text.value = f"❌ Error: {err}"
            result_card.visible = True
            result_card.border = ft.border.all(1, ft.colors.RED_ACCENT_400)

        page.update()  # 화면 갱신

    # ✅ 공통 버튼 스타일 함수 (재사용 목적)
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

    # ✅ 전체 View 구성
    return ft.View(
        route="/paired_two",  # 이 View에 해당하는 라우트 주소
        scroll=ft.ScrollMode.AUTO,  # 세로 스크롤 허용
        controls=[
            # 페이지 제목 텍스트
            ft.Text("Paired t-test (Two-tailed)", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_400),

            # 입력 필드 묶음
            input_fields,

            # Run 버튼
            ft.Row(
                controls=[
                    home_style_button("Run", ft.icons.PLAY_ARROW, run_test)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),

            # 결과 카드 출력 영역
            ft.Row(
                controls=[result_card],
                alignment=ft.MainAxisAlignment.CENTER
            ),

            # Back 버튼 (통계 메뉴로 이동)
            ft.Row(
                controls=[
                    home_style_button("Back", ft.icons.ARROW_BACK, lambda e: page.go("/statistics"))
                ],
                alignment=ft.MainAxisAlignment.START
            )
        ]
    )
