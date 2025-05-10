import flet as ft
import numpy as np
from stats.tools.t_test.ttest_logic import run_paired_ttest, compute_sd
from stats.references import get_references_for_test

# Paired t-test 결과 화면 View 정의 함수
def paired_view(page: ft.Page):
    # 🔷 사용자 입력 필드 정의
    before_input = ft.TextField(label="Before (comma-separated)", hint_text="e.g., 100, 102, 98")
    after_input = ft.TextField(label="After (comma-separated)", hint_text="e.g., 105, 100, 99")
    alpha_input = ft.TextField(label="Alpha", value="0.05")

    # 🔷 입력 필드들을 수직으로 배치
    input_fields = ft.Column(
        controls=[before_input, after_input, alpha_input],
        spacing=16
    )

    # 🔷 결과 출력용 텍스트 정의
    result_text = ft.Text("", no_wrap=False, selectable=True)

    # 🔷 결과 카드 UI 정의 (출력 + 복사 버튼 포함)
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

    # 🔷 실행 버튼 클릭 시 통계 분석 실행 함수
    def run_test(e):
        try:
            # 입력값 파싱
            before = list(map(float, before_input.value.split(",")))
            after = list(map(float, after_input.value.split(",")))
            alpha = float(alpha_input.value)

            # t-test 실행
            result = run_paired_ttest(before, after, alpha, return_dict=True)
            sd_before = compute_sd(before)
            sd_after = compute_sd(after)

            text = ""

            # 🔸 에러 발생 시 출력 처리
            if result["error"]:
                text = result["error"] + "\n"
                if "normality" in result:
                    norm = result["normality"]
                    text += (
                        "\nNormality Test on Differences (after - before):\n"
                        "-----------------------------------------------------------------------------\n"
                        f"Shapiro-Wilk:        {'passed' if norm['shapiro_pass'] else 'failed'} (p = {norm['shapiro_p']:.4f})\n"
                        f"Kolmogorov-Smirnov:  {'passed' if norm['ks_pass'] else 'failed'} (p = {norm['ks_p']:.4f})\n"
                        f"Anderson-Darling:    {'passed' if norm['ad_pass'] else 'failed'} (stat = {norm['ad_stat']:.4f}, crit = {norm['ad_crit']:.4f})\n"
                        "-----------------------------------------------------------------------------"
                    )

                text += "\n\n" + get_references_for_test("paired")
                result_card.border = ft.border.all(1, ft.colors.RED_ACCENT_400)

            else:
                # 🔸 정상 결과 출력 조립
                test_result_label = (
                    "significant" if result["sig"] == "Significant" else "not significant"
                )

                # 🔸 판정 이유 설명 (항상 출력)
                reason = (
                    f"Reason: The t-statistic ({result['t_stat']:.3f}) "
                    f"{'exceeds' if result['sig'] == 'Significant' else 'does not exceed'} "
                    f"the critical value (±{result['crit']:.3f}).\n"
                    f"        The p-value ({result['p']:.4f}) is "
                    f"{'less' if result['sig'] == 'Significant' else 'greater'} than the alpha level (α = {result['alpha']})."
                )

                text = f"""Paired t-test ({result['tail']}-tailed) result:
==========================================================

Normality Test on Differences (after - before):
-----------------------------------------------------------------------------
Shapiro-Wilk:        {'passed' if result['normality']['shapiro_pass'] else 'failed'} (p = {result['normality']['shapiro_p']:.4f})
Kolmogorov-Smirnov:  {'passed' if result['normality']['ks_pass'] else 'failed'} (p = {result['normality']['ks_p']:.4f})
Anderson-Darling:    {'passed' if result['normality']['ad_pass'] else 'failed'} (stat = {result['normality']['ad_stat']:.4f}, crit = {result['normality']['ad_crit']:.4f})

Normality assumption met (at least 1 test passed). Proceeding to t-test...

T-test Result:
-----------------------------------------------------------------------------
Critical value = ±{result['crit']:.3f} (α = {result['alpha']})
t({result['df']}) = {result['t_stat']:.3f}
p-value = {result['p']:.4f} ({result['tail']}-tailed)
Test Result = {test_result_label}
{reason}
Cohen’s d = {result['cohen_d']} ({result['cohen_d_interp']})
SD(before) = {sd_before}
SD(after) = {sd_after}
-----------------------------------------------------------------------------"""

                if result["df"] <= 1:
                    text += (
                        "\n⚠️ Note: Sample size is extremely small (df ≤ 1). "
                        "Interpretation of p-value and t-statistic may not be reliable.\n"
                        "-----------------------------------------------------------------------------"
                    )

                if np.isinf(result["t_stat"]) or np.isinf(result["cohen_d"]):
                    text += (
                        "\n⚠️ Note: All differences were identical. "
                        "Standard deviation is zero, so t and Cohen's d are undefined (∞). "
                        "Interpretation requires caution.\n"
                        "-----------------------------------------------------------------------------"
                    )

                text += "\n\n" + get_references_for_test("paired")

                if result["sig"] == "Not Significant":
                    result_card.border = ft.border.all(1, ft.colors.RED_ACCENT_400)
                else:
                    result_card.border = ft.border.all(1, ft.colors.GREEN_ACCENT_400)

            result_text.value = text
            result_card.visible = True

        except Exception as err:
            result_text.value = f"❌ Error: {err}"
            result_card.visible = True
            result_card.border = ft.border.all(1, ft.colors.RED_ACCENT_400)

        page.update()

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

    # 🔷 최종 View 반환
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
            ft.Container(padding=ft.padding.only(bottom=40)),
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
