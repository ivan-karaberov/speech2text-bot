import re

import jinja2

from core import config


def render_template(template_name: str, data: dict | None = None) -> str:
    if data is None:
        data = {}
    template = _get_template_env().get_template(template_name)
    rendered = template.render(**data).replace("\n", " ")
    rendered = rendered.replace("<br>", "\n")
    rendered = re.sub(" +", " ", rendered).replace(" .", ".").replace(" ,", ",")
    rendered = "\n".join(line.strip() for line in rendered.split("\n"))
    rendered = rendered.replace("{FOURPACES}", "    ")
    return rendered


def _get_template_env() -> jinja2.Environment:
    if not getattr(_get_template_env, "template_env", None):
        template_loader = jinja2.FileSystemLoader(
            searchpath=config.templates_dir
        )

        env = jinja2.Environment(
            loader=template_loader,
            trim_blocks=True,
            lstrip_blocks=True,
            autoescape=True,
        )

        setattr(_get_template_env, "template_env", env)

    return _get_template_env.template_env
