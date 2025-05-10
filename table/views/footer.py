import flet as ft
from table.core.exporter import export_table_to_word

def footer_section(page, table_data):
    return ft.Column([
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "If you have any questions or need support, feel free to email me.",
                    size=13, color=ft.colors.BLUE_GREY_700
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("E-mail:", size=13),
                        ft.Text("eugenemariastas@gmail.com", size=13, color=ft.colors.CYAN_400),
                        ft.IconButton(
                            icon=ft.icons.CONTENT_COPY,
                            tooltip="Copy email",
                            icon_color=ft.colors.GREY_600,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=6),
                                overlay_color=ft.colors.with_opacity(0.25, ft.colors.CYAN_400)
                            ),
                            on_click=lambda e: page.set_clipboard("eugenemariastas@gmail.com")
                        )
                    ]
                )
            ]
        ),
        ft.Container(height=20),
        ft.Row([
            ft.ElevatedButton("⬅️ Back", on_click=lambda e: page.go("/"), style=ft.ButtonStyle(bgcolor=ft.colors.GREY_200)),
            ft.Container(expand=True),
            ft.ElevatedButton("📤 Export to Word", on_click=lambda e: export_table_to_word(table_data), style=ft.ButtonStyle(bgcolor=ft.colors.CYAN_200))
        ])
    ])
