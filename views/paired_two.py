import flet as ft
import numpy as np
from core.ttest_logic import run_paired_ttest  # 핵심 계산 함수

def paired_view(page: ft.Page):
    # ✅ 입력 필드 정의
    before_input = ft.TextField(label="Before (comma-separated)", hint_text="e.g., 100, 102, 98")
    after_input = ft.TextField(label="After (comma-separated)", hint_text="e.g., 105, 100, 99")
    alpha_input = ft.TextField(label="Alpha", value="0.05")

    input_fields = ft.Column(
        controls=[before_input, after_input, alpha_input],
        spacing=16
    )

    # ✅ 결과 텍스트 및 카드
    result_text = ft.Text("", no_wrap=False, selectable=True)

    result_card = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=result_text, alignment=ft.alignment.center_left),
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
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        width=600,
        padding=20,
        margin=ft.margin.only(top=10),
        border_radius=8,
        bgcolor=ft.colors.GREY_50,
        border=ft.border.all(1, ft.colors.CYAN_400),
        visible=False
    )

    # ✅ Run 버튼 클릭 시 실행 함수
    def run_test(e):
        try:
            before = list(map(float, before_input.value.split(",")))
            after = list(map(float, after_input.value.split(",")))
            alpha = float(alpha_input.value)

            result = run_paired_ttest(before, after, alpha, return_dict=True)

            if result["error"]:
                result_text.value = result["error"]
                result_card.border = ft.border.all(1, ft.colors.RED_ACCENT_400)
            else:
                # ✅ 출력 조립
                text = (
                    f"🔍 Paired T-test ({result['tail']}-tailed)\n"
                    + (f"- Direction: {result['direction']}\n" if result["direction"] else "")
                    + f"- t({result['df']}) = {result['t_stat']:.3f}\n"
                    + f"- p = {result['p']:.4f}\n"
                    + f"- Critical value = {result['crit']:.3f} (α = {result['alpha']})\n"
                    + f"- Cohen's d = {result['cohen_d']} ({result['cohen_d_interp']})\n"
                    + f"- Result: {result['sig']}"
                )

                # ✅ 무한대 경고 추가
                if np.isinf(result["t_stat"]) or np.isinf(result["cohen_d"]):
                    text += (
                        "\n⚠️ Note: All differences were identical. "
                        "Standard deviation is zero, so t and Cohen's d are undefined (∞). "
                        "Interpretation requires caution."
                    )

                result_text.value = text

                # ✅ 테두리 색상 조정
                if "Not Significant" in result["sig"]:
                    result_card.border = ft.border.all(1, ft.colors.RED_ACCENT_400)
                else:
                    result_card.border = ft.border.all(1, ft.colors.GREEN_ACCENT_400)

            result_card.visible = True

        except Exception as err:
            result_text.value = f"❌ Error: {err}"
            result_card.visible = True
            result_card.border = ft.border.all(1, ft.colors.RED_ACCENT_400)

        page.update()

    # ✅ 공통 버튼 스타일 함수
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

    return ft.View(
        route="/paired_two",
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Text(
                "Paired t-test (Two-tailed)",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.colors.CYAN_400
            ),
            ft.Container(padding=ft.padding.only(bottom=40)),  # 헤더 아래 간격
            input_fields,
            ft.Row(
                controls=[home_style_button("Run", ft.icons.PLAY_ARROW, run_test)],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[result_card],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Row(
                controls=[home_style_button("Back", ft.icons.ARROW_BACK, lambda e: page.go("/statistics"))],
                alignment=ft.MainAxisAlignment.START
            )
        ]
    )