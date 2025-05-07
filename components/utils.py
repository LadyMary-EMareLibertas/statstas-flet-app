def parse_input(text: str):
    try:
        return [float(x.strip()) for x in text.split(",")]
    except Exception:
        return []