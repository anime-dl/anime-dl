import httpx


session = httpx.Client()


def get_quality_from_name(quality: str):
    if quality.lower().replace("p", "").strip().isdigit():
        if int(quality) in (360, 480, 720, 1080):
            return int(quality)
    return None


__all__ = [
    "session"
]
