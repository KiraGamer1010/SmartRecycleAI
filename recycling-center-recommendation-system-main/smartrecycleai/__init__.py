from __future__ import annotations

from pathlib import Path

from flask import Flask


def create_app() -> Flask:
    project_root = Path(__file__).resolve().parents[1]
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder=str(project_root / "templates"),
        static_folder=str(project_root / "static"),
    )
    app.config.update(
        SECRET_KEY="smartrecycleai-local-secret",
        TEMPLATES_AUTO_RELOAD=True,
    )

    from .routes import main_bp

    app.register_blueprint(main_bp)

    @app.template_filter("number")
    def number_filter(value):
        try:
            return f"{float(value):,.0f}"
        except (TypeError, ValueError):
            return value

    @app.template_filter("decimal")
    def decimal_filter(value):
        try:
            return f"{float(value):,.2f}"
        except (TypeError, ValueError):
            return value

    return app
