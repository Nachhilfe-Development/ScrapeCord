import jinja2
from pathlib import Path
from datetime import datetime


def render_to_html(data: dict) -> str:
    def format_timestamp(timestamp: float) -> str:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def int_color_to_hey(color: int | None) -> str:
        if not color:
            return "#007BF7"
        return f"#{color:06x}"

    def filter_ui_components(components: list[dict], action_row: bool = False) -> list[dict]:
        return list(filter(lambda c: c["type"] == "action_row" and action_row, components))

    def convert_button_type_to_css_class(button_type: int) -> str:
        return {
            1: "ui_button_primary",
            2: "ui_button_secondary",
            3: "ui_button_success",
            4: "ui_button_danger",
            5: "ui_button_link",
        }[button_type]

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(Path(__file__).parent / "templates"),
        autoescape=jinja2.select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = env.get_template("channel.html")
    return template.render(
        {
            **data,
            "utils": {
                "format_timestamp": format_timestamp,
                "int_color_to_hey": int_color_to_hey,
                "filter_ui_components": filter_ui_components,
                "convert_button_type_to_css_class": convert_button_type_to_css_class
            },
        }

    )
