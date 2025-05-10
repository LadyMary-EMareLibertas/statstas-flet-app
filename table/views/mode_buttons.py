import flet as ft

def build_mode_buttons(editing_mode, on_text_click, on_structure_click):
    return ft.Row([
        ft.ElevatedButton(
            "Edit Text",
            on_click=on_text_click,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE_100 if editing_mode == "text" else ft.colors.GREY_200
            )
        ),
        ft.ElevatedButton(
            "Edit Structure",
            on_click=on_structure_click,
            style=ft.ButtonStyle(
                bgcolor=ft.colors.BLUE_100 if editing_mode == "structure" else ft.colors.GREY_200
            )
        )
    ], spacing=10)