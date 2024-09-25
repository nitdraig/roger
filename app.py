from flask import Flask
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from routes.main import main_bp
    from routes.analysis import analysis_bp
    from routes.autocomplete import autocomplete_bp
    from routes.investment_calculator import investment_calculator_bp
    from routes.sentiment import sentiment_bp
    from routes.comparison import comparison_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(autocomplete_bp)
    app.register_blueprint(investment_calculator_bp)
    app.register_blueprint(sentiment_bp)
    app.register_blueprint(comparison_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    # local:
    # app.run(host="0.0.0.0", port=5000, debug=True)
    # prod
    app.run(host="0.0.0.0", port=5000)
