import flet as ft
from core.ttest_logic import run_paired_ttest  # t-test 계산 함수 import

# 이 함수는 "/paired_two" 경로에 해당하는 화면을 구성함
def paired_view(page: ft.Page):
    # 사용자 입력을 위한 입력창 생성
    # before: 실험 전 측정값 리스트
    # after: 실험 후 측정값 리스트
    # alpha: 유의수준 (0.05 기본값)
    before_input = ft.TextField(label="Before (comma-separated)", hint_text="e.g., 100, 102, 98")
    after_input = ft.TextField(label="After (comma-separated)", hint_text="e.g., 105, 100, 99")
    alpha_input = ft.TextField(label="Alpha", value="0.05")

    # 결과를 출력할 텍스트 객체
    result_text = ft.Text(
        "",
        no_wrap=False,
        selectable=True
    )

    # 결과 출력을 감싸는 카드 스타일 컨테이너
    result_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(  # 텍스트는 왼쪽 정렬
                    content=result_text,
                    alignment=ft.alignment.center_left
                ),
                ft.Container(  # 복사 버튼은 오른쪽 하단 정렬
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
            expand=True,  # 하단 정렬을 위해 전체 높이 사용
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN  # 텍스트 위, 버튼 아래 배치
        ),
        width=600,
        height=200,  # 필요 시 높이 지정
        padding=20,
        margin=ft.margin.only(top=10),
        border_radius=8,
        bgcolor=ft.colors.GREY_50,
        border=ft.border.all(1, ft.colors.CYAN_400),
        visible=False
    )

    # t-test 실행 함수 (Run 버튼을 누르면 실행됨)
    def run_test(e):
        try:
            # 입력값을 숫자 리스트로 변환
            before = list(map(float, before_input.value.split(",")))
            after = list(map(float, after_input.value.split(",")))
            alpha = float(alpha_input.value)

            # core.ttest_logic에서 계산 함수 호출
            result = run_paired_ttest(before, after, alpha)

            # 결과를 문자열로 바꿔 출력
            result_text.value = str(result)
            result_card.visible = True  # ← 결과 카드 보이도록 설정

        except Exception as err:
            # 에러 발생 시 에러 메시지 출력
            result_text.value = f"❌ Error: {err}"
            result_card.visible = True  # ← 에러도 결과니까 표시

        page.update()  # 화면 갱신

    # 홈/통계 뷰와 동일한 버튼 스타일 함수
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

    # 전체 화면(View) 구성
    return ft.View(
        route="/paired_two",
        scroll=ft.ScrollMode.AUTO,  # 세로 스크롤 허용
        controls=[
            ft.Text("Paired t-test (Two-tailed)", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_400),

            before_input,   # 입력창: before
            after_input,    # 입력창: after
            alpha_input,    # 입력창: alpha

            ft.Row(
                controls=[
                    home_style_button("Run", ft.icons.PLAY_ARROW, run_test)
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),

            ft.Row(
                controls=[result_card],
                alignment=ft.MainAxisAlignment.CENTER
            ),

            ft.Row(
                controls=[
                    home_style_button("Back", ft.icons.ARROW_BACK, lambda e: page.go("/statistics"))
                ],
                alignment=ft.MainAxisAlignment.START
            )
        ]
    )