from flask import Flask, render_template
from dotenv import load_dotenv
load_dotenv()
import config
from extensions import limiter
from api.routes import api_bp

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH
app.config["SECRET_KEY"] = config.SECRET_KEY

limiter.init_app(app)
app.register_blueprint(api_bp)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template("404.html"), 500


if __name__ == "__main__":
    app.run(debug=config.DEBUG)
