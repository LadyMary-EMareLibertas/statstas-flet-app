import flet as ft

# 홈 페이지
from home import home_view

# 통계 메뉴 페이지
from stats.statistics import statistics_view

# t-test 분석 도구 (Paired t-test)
from stats.tools.t_test.paired_two import paired_view

# 테이블 편집기 (APA 기본 템플릿)
from table.table_editor import table_editor_view

def main(page: ft.Page):
    # 페이지 제목 설정 (브라우저 탭이나 앱 상단에 표시됨)
    page.title = "StatStas"

    # 경로(route)가 바뀔 때 실행되는 콜백 함수 정의
    def route_change(e):
        # e가 route 속성을 가지고 있으면 route 값을 꺼내고,
        # 없으면 e 자체를 route로 간주 (처음 실행 시 대응)
        route = e.route if hasattr(e, "route") else e

        # 현재 페이지 뷰를 모두 초기화
        page.views.clear()

        # 경로에 따라 각 뷰 함수 호출
        if route == "/":
            page.views.append(home_view(page))          # 홈 화면
        elif route == "/statistics":
            page.views.append(statistics_view(page))    # 통계 도구 검색 화면
        elif route == "/paired_two":
            page.views.append(paired_view(page))        # Paired t-test 실행 화면
        elif route == "/table":
            page.views.append(table_editor_view(page))   # 테이블 편집기 화면 (APA 템플릿 고정)

    # 페이지에 라우트 변경 이벤트 핸들러 연결
    page.on_route_change = route_change

    # 초기 경로 설정 → 앱이 처음 열릴 때 보여줄 화면 결정
    route_change(page.route)

    # 실제 라우팅을 시작 (첫 화면으로 진입)
    page.go(page.route)

# Flet 앱 실행: main 함수가 entry point 역할
ft.app(target=main)
