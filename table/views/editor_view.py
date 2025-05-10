# 📄 table_editor_view.py
# StatStas 테이블 편집기의 메인 뷰를 구성하는 파일입니다.
# 테이블 렌더링, 편집 모드 버튼, 행/열 조작 도구, 상태 표시 바 등을 화면에 배치합니다.



import flet as ft
# 테이블을 Word 문서로 내보내는 함수
from table.core.exporter import export_table_to_word
# 테이블 에디터의 상태를 담는 클래스 (예: 어떤 셀이 선택됐는지, 모드 등)
from table.logic.state import TableEditorState
# 사용자가 어떤 버튼을 눌렀을 때 실행되는 함수들
from table.logic.handlers import (
    enable_text_mode, enable_structure_mode, handle_border_toggle, make_on_change
)
# 실제 테이블을 화면에 그려주는 함수
from table.logic.table_renderer import build_table_rows
# 편집 모드 버튼을 만들어주는 함수
from table.views.mode_buttons import build_mode_buttons
# 화면 하단의 정보 표시 줄 등을 만들어주는 함수
from table.views.footer import footer_section
# 행/열 추가, 삭제, 굵은 선 토글 기능 등을 담당하는 함수들
from table.logic.structure import (
    handle_add_row,
    handle_delete_row,
    handle_add_column,
    handle_delete_column,
    handle_toggle_bold
)

def table_editor_view(page: ft.Page):
    # 테이블 편집기의 상태를 생성 (초기화)
    state = TableEditorState()

    # UI에 들어갈 요소들을 미리 만들어두는 공간 (딕셔너리 형태)
    ui = {
        "table_column": ft.Column(spacing=0),  # 실제 테이블이 들어가는 컬럼
        "mode_buttons": ft.Container()         # 보기/편집 모드를 선택하는 버튼들
    }

    # 화면을 다시 그리는 함수 (모드 변경이나 편집 후 실행됨)
    def rebuild():
        # 모드 전환 버튼을 생성하여 화면에 추가
        ui["mode_buttons"].content = build_mode_buttons(
            state.editing_mode,                           # 현재 편집 모드
            enable_text_mode(state, ui, page),           # 텍스트 모드 전환 함수
            enable_structure_mode(state, ui, page)       # 구조 모드 전환 함수
        )
        # 테이블을 다시 생성하여 화면에 표시
        ui["table_column"].controls = build_table_rows(
            state,             # 현재 테이블 상태
            ui,                # UI 요소들
            page,              # 페이지 객체 (Flet에서 화면 전체 정보)
            handle_border_toggle,  # 테두리 변경 함수
            make_on_change         # 셀 내용 변경 감지 함수
        )

    # 처음 진입 시 한 번 화면을 렌더링
    rebuild()

    # 구조 편집 모드일 때만 보여줄 버튼들(행/열 추가/삭제 등)을 만드는 함수
    def build_tools():
        if state.editing_mode != "structure":
            return []  # 구조 모드가 아니면 아무것도 안 보여줌

        # 버튼 하나를 만드는 함수 (예: "Add Row" 누르면 행이 추가됨)
        def row_action(label, handler_func):
            return ft.ElevatedButton(
                label,
                on_click=lambda e: handler_func(
                    state.table_data,        # 현재 테이블 데이터
                    state.selected_cell,     # 현재 선택된 셀
                    ui["table_column"],      # 테이블이 그려지는 컬럼
                    lambda: build_table_rows( # 테이블 다시 그리는 함수 전달
                        state,
                        ui,
                        page,
                        handle_border_toggle,
                        make_on_change
                    ),
                    page
                ) if state.selected_cell else None  # 셀이 선택되지 않았으면 실행 안 함
            )

        # 행 추가/삭제 관련 버튼들을 정렬한 Row
        structure_row = ft.Row([
            row_action("➕ Add Row", handle_add_row),
            row_action("➖ Delete Row", handle_delete_row),
            ft.ElevatedButton("↩️ Undo", on_click=lambda e: None),  # 취소 기능은 아직 구현 안 됨
        ], spacing=10)

        # 열 추가/삭제 및 굵은 선 토글 관련 버튼들을 정렬한 Row
        column_row = ft.Row([
            row_action("➕ Add Column", handle_add_column),
            row_action("➖ Delete Column", handle_delete_column),
            ft.ElevatedButton("🔄 Reverse Undo", on_click=lambda e: None),  # 취소 복구 (아직 구현 안 됨)
            row_action("🔳 Toggle Bold Line", handle_toggle_bold),
        ], spacing=10)

        # 행과 열 버튼들을 세로로 정렬하여 반환
        return [ft.Column([structure_row, column_row], spacing=10)]

    # 실제 화면에 보여줄 View 구성 (Flet의 View 컴포넌트 사용)
    return ft.View(
        route="/table",  # 이 화면의 라우팅 주소 (앱 내부용 경로)
        scroll=ft.ScrollMode.AUTO,  # 세로 스크롤 허용
        controls=[
            # 제목 텍스트
            ft.Text("APA Table Editor", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_400),

            # 안내문 텍스트 (서식 기능은 Word에서 완성하라고 설명)
            ft.Text(
                "StatStas does not support font settings or text alignment. Please export your table to Word and complete the final formatting there. Lines that look slightly misaligned in the editor will be cleanly aligned in the exported document.",
                size=12, color=ft.colors.GREY_600, italic=True
            ),

            ft.Container(height=12),  # 여백용

            ui["mode_buttons"],      # 편집 모드 버튼 표시
            *build_tools(),          # 구조 모드일 경우만 나오는 도구 버튼들

            # 실제 테이블이 들어가는 영역 (배경색, 테두리 포함)
            ft.Container(
                content=ui["table_column"],
                padding=6,
                bgcolor=ft.colors.WHITE,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=6
            ),

            ft.Container(height=24),  # 여백용

            # 화면 하단의 상태 표시줄, 내보내기 버튼 등
            footer_section(page, state.table_data)
        ]
    )