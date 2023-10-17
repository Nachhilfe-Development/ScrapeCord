import json

import sys
from pathlib import Path
sys.path.append(Path(".").resolve().as_posix())
from src.renderer import render_to_html


if __name__ == "__main__":
    with open(Path(__file__).parent / "example.json", "r") as f:
        data = json.load(f)

    html = render_to_html(data)

    with open(Path(__file__).parent / "example.html", "w", encoding="utf-8") as f:
        f.write(html)
