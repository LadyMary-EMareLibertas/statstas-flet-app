import flet as ft
from ttest_logic import run_paired_ttest

def paired_view():
    before_input = ft.TextField(label="Before", hint_text="e.g., 580, 590, 600")
    after_input = ft.TextField(label="After", hint_text="e.g., 650, 660, 640")
    alpha_input = ft.TextField(label="Alpha", value="0.05")
    result_text = ft.Text()

    def run_test(e):
        try:
            before = list(map(float, before_input.value.split(",")))
            after = list(map(float, after_input.value.split(",")))
            alpha = float(alpha_input.value)
            result = run_paired_ttest(before, after, alpha)
            result_text.value = str(result)
        except Exception as err:
            result_text.value = f"❌ Error: {err}"
        e.page.update()

    return ft.Column([
        ft.Text("Paired t-test (Two-tailed)", size=24),
        before_input,
        after_input,
        alpha_input,
        ft.ElevatedButton("Run t-test", on_click=run_test),
        result_text
    ])