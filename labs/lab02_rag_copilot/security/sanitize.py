import re
TAG_RX = re.compile(r"<[^>]+>")  # naive tag strip

def sanitize(text: str) -> str:
    # Remove simple HTML/script tags to reduce active content risks
    return TAG_RX.sub("", text)