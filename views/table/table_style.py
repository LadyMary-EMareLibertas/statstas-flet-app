from flet import TextAlign, colors

def get_border_style(cell, direction):
    """셀 딕셔너리에서 테두리 스타일 반환"""
    return cell.get(f"border_{direction}", {"color": "white", "thickness": 0})

def get_text_alignment(align_str):
    """문자열로 주어진 정렬값을 Flet TextAlign 객체로 변환"""
    return getattr(TextAlign, align_str.upper(), TextAlign.LEFT)