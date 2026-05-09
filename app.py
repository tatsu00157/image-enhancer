from flask import Flask
import config
from api.routes import api_bp

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = config.UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = config.MAX_CONTENT_LENGTH

app.register_blueprint(api_bp)

if __name__ == "__main__":
    app.run(debug=True)
